"""Dense (semantic) retriever.

A thin wrapper around the vector store that returns embedding-similarity matches.
Kept as its own module so the dense path can be swapped (e.g. a different vector
DB or a reranker) without touching the fusion logic.
"""
from __future__ import annotations

from src.vectorstore import VectorStore


class SemanticRetriever:
    def __init__(self, store: VectorStore):
        self.store = store

    def search(self, query: str, k: int, where: dict | None = None) -> list[dict]:
        results = self.store.query(query, k=k, where=where)
        for r in results:
            r["semantic_score"] = r.pop("score", 0.0)
        return results
