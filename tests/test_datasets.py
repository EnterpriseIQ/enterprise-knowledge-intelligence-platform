"""Dataset validation tests.

Verify the synthetic corpus is complete, well-formed and carries the security
metadata the rest of the platform relies on.
"""
from __future__ import annotations

import json
from pathlib import Path

from src import config
from src.ingestion import load_corpus

ROOT = Path(__file__).resolve().parent.parent


def test_manifest_exists_and_covers_all_departments():
    manifest = json.loads((config.DOCUMENTS_DIR / "manifest.json").read_text())
    depts = {m["department"] for m in manifest}
    assert {"HR", "Finance", "Engineering", "Compliance", "Operations"} <= depts


def test_all_source_types_present():
    manifest = json.loads((config.DOCUMENTS_DIR / "manifest.json").read_text())
    types = {m["source_type"] for m in manifest}
    assert {"pdf", "csv", "sql", "json"} <= types


def test_every_entry_has_security_metadata():
    manifest = json.loads((config.DOCUMENTS_DIR / "manifest.json").read_text())
    levels = set(config.ACCESS_POLICY_FILE and json.loads(
        config.ACCESS_POLICY_FILE.read_text())["sensitivity_levels"])
    for m in manifest:
        assert m["department"] in config.DEPARTMENTS
        assert m["sensitivity"] in levels
        assert Path(ROOT / m["path"]).exists(), f"missing file for {m['doc_id']}"


def test_corpus_loads_with_text():
    docs = load_corpus()
    assert len(docs) >= 18
    assert all(d.text.strip() for d in docs)
    # PDFs should extract real, queryable content.
    pdfs = [d for d in docs if d.source_type == "pdf"]
    assert pdfs and all(len(d.text) > 100 for d in pdfs)
