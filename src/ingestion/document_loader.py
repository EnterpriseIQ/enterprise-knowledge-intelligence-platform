"""Unified corpus loader.

Reads the dataset manifest produced by ``data/generate_data.py`` and dispatches
each entry to the correct source loader. Returns a list of ``RawDocument``
objects that carry both the extracted text and the security metadata
(department, sensitivity, allowed_roles) that the RBAC engine relies on.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from src import config
from src.ingestion.csv_loader import load_csv
from src.ingestion.json_loader import load_json
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.sql_loader import load_sql


@dataclass
class RawDocument:
    doc_id: str
    title: str
    text: str
    source_type: str  # pdf | csv | sql | json
    department: str  # HR | Finance | Engineering | Compliance | Operations
    sensitivity: str  # public | internal | confidential | restricted
    allowed_roles: list[str] = field(default_factory=list)
    path: str = ""

    def metadata(self) -> dict:
        """Security + provenance metadata propagated to every chunk."""
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "source_type": self.source_type,
            "department": self.department,
            "sensitivity": self.sensitivity,
            # Stored as a comma string for vector-store metadata compatibility.
            "allowed_roles": ",".join(self.allowed_roles),
            "path": self.path,
        }


_LOADERS = {
    "pdf": load_pdf,
    "csv": load_csv,
    "sql": load_sql,
    "json": load_json,
}


def load_corpus(manifest_path: Path | None = None) -> list[RawDocument]:
    manifest_path = manifest_path or (config.DOCUMENTS_DIR / "manifest.json")
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found at {manifest_path}. Run `python -m data.generate_data` first."
        )
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))

    docs: list[RawDocument] = []
    for entry in entries:
        loader = _LOADERS.get(entry["source_type"])
        if loader is None:
            continue

        # Prevent path traversal vulnerabilities by ensuring the resolved
        # path is within the project root.
        try:
            root = config.PROJECT_ROOT.resolve()
            abs_path = (config.PROJECT_ROOT / entry["path"]).resolve()
            if not abs_path.is_relative_to(root):
                continue
        except Exception:
            continue

        if not abs_path.exists():
            continue
        text = loader(abs_path)
        if not text.strip():
            continue
        docs.append(
            RawDocument(
                doc_id=entry["doc_id"],
                title=entry["title"],
                text=text,
                source_type=entry["source_type"],
                department=entry["department"],
                sensitivity=entry["sensitivity"],
                allowed_roles=entry.get("allowed_roles", []),
                path=entry["path"],
            )
        )
    return docs
