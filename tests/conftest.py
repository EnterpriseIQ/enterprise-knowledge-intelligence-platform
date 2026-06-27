"""Shared pytest fixtures.

Builds the corpus and a single warm pipeline once per test session so the suite is
fast and exercises the real end-to-end system (ingestion → index → retrieval →
RBAC → generation).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data import generate_data  # noqa: E402
from src.pipeline import RAGPipeline  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def corpus():
    """Ensure the synthetic corpus + manifest exist before any test runs."""
    if not (ROOT / "data" / "documents" / "manifest.json").exists():
        generate_data.main()
    return True


@pytest.fixture(scope="session")
def pipeline(corpus):
    p = RAGPipeline()
    p.build_index()
    return p
