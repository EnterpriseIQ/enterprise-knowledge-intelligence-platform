"""Central configuration for the Enterprise RAG platform.

All tunable paths and parameters live here so the rest of the codebase has a
single source of truth. Values can be overridden via environment variables,
which keeps the platform twelve-factor friendly for containerised deployment.
"""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Optionally load a local .env file so configuration is twelve-factor friendly.
# python-dotenv ships with uvicorn[standard]; if it is absent we silently rely on
# real environment variables instead.
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except Exception:  # pragma: no cover - dotenv is optional
    pass

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
DATA_DIR = Path(os.getenv("ERAG_DATA_DIR", PROJECT_ROOT / "data"))
DOCUMENTS_DIR = DATA_DIR / "documents"
STRUCTURED_DIR = DATA_DIR / "structured"
LOGS_DIR = DATA_DIR / "logs"
RBAC_DIR = DATA_DIR / "rbac"

ACCESS_POLICY_FILE = RBAC_DIR / "access_policies.json"
SQL_DB_FILE = STRUCTURED_DIR / "operations.db"
AUDIT_LOG_FILE = LOGS_DIR / "audit_trail.jsonl"

# Persistent vector store location (Chroma) — falls back to in-memory store.
VECTORSTORE_DIR = Path(os.getenv("ERAG_VECTORSTORE_DIR", DATA_DIR / "vectorstore"))
COLLECTION_NAME = os.getenv("ERAG_COLLECTION", "enterprise_corpus")

# --------------------------------------------------------------------------- #
# Chunking
# --------------------------------------------------------------------------- #
CHUNK_SIZE = int(os.getenv("ERAG_CHUNK_SIZE", "900"))        # characters
CHUNK_OVERLAP = int(os.getenv("ERAG_CHUNK_OVERLAP", "150"))  # characters

# --------------------------------------------------------------------------- #
# Embeddings
# --------------------------------------------------------------------------- #
# Preferred SentenceTransformers model. If the library or weights are not
# available (e.g. offline CI), the platform transparently falls back to a
# deterministic hashing embedder so the system always runs.
EMBEDDING_MODEL = os.getenv("ERAG_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIM_FALLBACK = int(os.getenv("ERAG_EMBEDDING_DIM", "384"))

# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #
TOP_K = int(os.getenv("ERAG_TOP_K", "5"))
CANDIDATE_K = int(os.getenv("ERAG_CANDIDATE_K", "20"))
# Weight given to dense (semantic) vs. sparse (BM25) scores during fusion.
HYBRID_ALPHA = float(os.getenv("ERAG_HYBRID_ALPHA", "0.6"))

# Confidence thresholds used to label answers for the end user.
CONFIDENCE_HIGH = float(os.getenv("ERAG_CONF_HIGH", "0.55"))
CONFIDENCE_LOW = float(os.getenv("ERAG_CONF_LOW", "0.30"))

# Departments / roles recognised by the platform.
DEPARTMENTS = ["HR", "Finance", "Engineering", "Compliance", "Operations"]
ROLES = ["Admin", "HR", "Finance", "Engineering", "Compliance"]


def ensure_dirs() -> None:
    """Create all runtime directories if they do not yet exist."""
    for d in (DATA_DIR, DOCUMENTS_DIR, STRUCTURED_DIR, LOGS_DIR, RBAC_DIR, VECTORSTORE_DIR):
        d.mkdir(parents=True, exist_ok=True)
