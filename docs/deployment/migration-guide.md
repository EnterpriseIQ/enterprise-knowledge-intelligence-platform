# Migration Guide

This guide details how to upgrade from older versions of the RAG platform to the unified EnterpriseIQ 1.0.0 release.

## From Pre-1.0 to 1.0.0

The 1.0.0 release introduces significant structural changes, particularly around RBAC and hybrid retrieval.

### Data Migration

The previous versions used a flat file structure for ChromaDB. The 1.0.0 release relies on a unified index with metadata tagging.

**You cannot migrate the old vector database directly.**

You must regenerate the index using the new ingestion pipeline:
1. Ensure your raw documents are in the new `data/` structure (`documents/`, `structured/`, `logs/`).
2. Run `python -m data.generate_data` to build the new unified ChromaDB collection and the paired BM25 index.

### API Changes

- The `/query` endpoint now requires a `role` or `user_id` in the JSON payload. Requests without these will default to `anonymous`, which likely has no access rights.
- The `X-API-Key` header is now strictly enforced if `API_KEY` is set in the environment.

### Codebase Refactoring

- If you had custom ingestion scripts, they must be updated to use the new `Document` and `Chunk` objects from `src/ingestion/parsers.py`, ensuring `department`, `clearance`, and `allowed_roles` are populated.
