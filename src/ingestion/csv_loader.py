"""CSV ingestion.

Structured tabular data is linearised into natural-language-ish row records so it
can be embedded and retrieved alongside prose. A compact schema summary is added
so that aggregate questions ("which service had the highest error rate?") have
context to match against.
"""
from __future__ import annotations

from pathlib import Path


def load_csv(path: Path, max_rows: int = 500) -> str:
    import pandas as pd

    df = pd.read_csv(path)
    lines: list[str] = [
        f"CSV dataset: {path.name}",
        f"Columns: {', '.join(map(str, df.columns))}",
        f"Row count: {len(df)}",
        "",
        "Records:",
    ]
    for _, row in df.head(max_rows).iterrows():
        rendered = "; ".join(f"{col}={row[col]}" for col in df.columns)
        lines.append(f"- {rendered}")
    return "\n".join(lines)
