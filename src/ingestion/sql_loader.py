"""SQL ingestion.

Reads every user table from a SQLite database and linearises the rows into text
records, one block per table. Schema information is included so that schema-level
questions retrieve well. Read-only access only: the loader never writes.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def load_sql(path: Path, max_rows_per_table: int = 500) -> str:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]

    if not tables:
        conn.close()
        return f"SQL database: {path.name}\nTables: \n\n"

    blocks: list[str] = [f"SQL database: {path.name}", f"Tables: {', '.join(tables)}", ""]

    cur.execute("""
        SELECT m.name as table_name, p.name as column_name
        FROM sqlite_master m
        JOIN pragma_table_info(m.name) p
        WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%'
    """)
    schemas = {}
    for t_name, c_name in cur.fetchall():
        schemas.setdefault(t_name, []).append(c_name)

    batch_size = 100
    for i in range(0, len(tables), batch_size):
        batch_tables = tables[i : i + batch_size]
        queries = []
        for table in batch_tables:
            cols = schemas.get(table, [])
            if not cols:
                continue
            concat_expr = " || '; ' || ".join(
                [f"'{c}=' || coalesce(\"{c}\", 'None')" for c in cols]
            )
            queries.append(
                f"SELECT * FROM (SELECT '{table}', {concat_expr} FROM \"{table}\" LIMIT {max_rows_per_table})"
            )

        if queries:
            union_query = " UNION ALL ".join(queries)
            cur.execute(union_query)

            table_rows = {t: [] for t in batch_tables}
            for t_name, data in cur.fetchall():
                table_rows[t_name].append(data)

            for table in batch_tables:
                cols = schemas.get(table, [])
                blocks.append(f"Table {table} (columns: {', '.join(cols)}):")
                for row_str in table_rows[table]:
                    blocks.append(f"- {row_str}")
                blocks.append("")

    conn.close()
    return "\n".join(blocks)
