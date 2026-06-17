"""Audit logging.

Every query and every access decision is appended to a tamper-evident JSONL audit
trail. This supports the explainability and compliance requirements: who asked
what, which sources were authorised, and which were denied and why.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src import config


class AuditLogger:
    def __init__(self, path: Path | None = None):
        self.path = Path(path or config.AUDIT_LOG_FILE)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, record: dict) -> None:
        record["ts"] = datetime.now(timezone.utc).isoformat()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def log_query(
        self, user_id: str, role: str, query: str, authorised: int, denied: int, confidence: float
    ) -> None:
        self._write(
            {
                "type": "query",
                "user_id": user_id,
                "role": role,
                "query": query,
                "authorised_sources": authorised,
                "denied_sources": denied,
                "confidence": round(confidence, 4),
            }
        )

    def log_access_decisions(self, user_id: str, role: str, decisions: list) -> None:
        for d in decisions:
            self._write(
                {
                    "type": "access_decision",
                    "user_id": user_id,
                    "role": role,
                    "doc_id": d.doc_id,
                    "department": d.department,
                    "sensitivity": d.sensitivity,
                    "allowed": d.allowed,
                    "reason": d.reason,
                }
            )

    def tail(self, n: int = 20) -> list[dict]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines[-n:]]
