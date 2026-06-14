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
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]

    blocks: list[str] = [f"SQL database: {path.name}", f"Tables: {', '.join(tables)}", ""]
    for table in tables:
        cur.execute(f"SELECT * FROM {table} LIMIT {max_rows_per_table}")
        rows = cur.fetchall()
        cols = rows[0].keys() if rows else [d[0] for d in cur.description]
        blocks.append(f"Table {table} (columns: {', '.join(cols)}):")
        for row in rows:
            rendered = "; ".join(f"{k}={row[k]}" for k in row.keys())
            blocks.append(f"- {rendered}")
        blocks.append("")
    conn.close()
    return "\n".join(blocks)
