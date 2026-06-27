"""JSON ingestion.

Handles JSON logs and audit trails, which are typically a list of event objects.
Each event is flattened into a single text line so individual events remain
retrievable, while the whole file stays attributable as one source document.
"""

from __future__ import annotations

import json
from pathlib import Path


def _flatten(obj, prefix: str = "") -> str:
    if isinstance(obj, dict):
        return "; ".join(f"{prefix}{k}={_flatten(v)}" for k, v in obj.items())
    if isinstance(obj, list):
        return ", ".join(_flatten(v) for v in obj)
    return str(obj)


def load_json(path: Path, max_records: int = 1000) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    lines: list[str] = [f"JSON source: {path.name}"]
    if isinstance(data, list):
        lines.append(f"Records: {len(data)}")
        lines.append("")
        for rec in data[:max_records]:
            lines.append(f"- {_flatten(rec)}")
    else:
        lines.append(_flatten(data))
    return "\n".join(lines)
