"""Hybrid Retrieval Engine.

Fuses dense semantic search with sparse BM25 lexical search, applies query-router
boosts, and enforces RBAC at retrieval time. Fusion uses min-max normalisation per
channel followed by a weighted blend controlled by ``HYBRID_ALPHA`` (the dense
weight). This is the cross-source retrieval engine: because all sources share one
index and one scoring space, a single query can surface a PDF policy, a SQL row and
a JSON log side by side — all filtered to the caller's authorised scope.

RBAC is enforced in two layers (defence in depth):
1. A vector-store ``where`` pre-filter restricts dense candidates by department.
2. Every fused candidate is re-checked with the full :class:`RBACEngine` (clearance
   + explicit ACLs), and denied items are recorded for the audit trail.
"""
from __future__ import annotations

from dataclasses import dataclass

from src import config
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.query_router import RouteDecision
from src.retrieval.semantic_retriever import SemanticRetriever
from src.security.rbac import AccessDecision, RBACEngine
from src.vectorstore import VectorStore


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    metadata: dict
    semantic_score: float = 0.0
    bm25_score: float = 0.0
    fused_score: float = 0.0
    route_boost: float = 0.0

    def to_citation(self) -> dict:
        m = self.metadata
        return {
            "doc_id": m.get("doc_id"),
            "title": m.get("title"),
            "source_type": m.get("source_type"),
            "department": m.get("department"),
            "sensitivity": m.get("sensitivity"),
            "page": m.get("page", 0),
            "chunk_id": self.chunk_id,
            "relevance": round(self.fused_score, 4),
        }


def _minmax(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    lo, hi = min(values.values()), max(values.values())
    if hi - lo < 1e-9:
        return {k: 1.0 for k in values}  # all equally relevant
    return {k: (v - lo) / (hi - lo) for k, v in values.items()}


class HybridRetriever:
    def __init__(self, store: VectorStore, rbac: RBACEngine, alpha: float | None = None):
        self.store = store
        self.rbac = rbac
        self.alpha = config.HYBRID_ALPHA if alpha is None else alpha
        self.semantic = SemanticRetriever(store)
        # BM25 index is built once over the full corpus; RBAC is applied at fuse time.
        self.bm25 = BM25Retriever(store.all_records())

    # ------------------------------------------------------------------ #
    def retrieve(self, query: str, role: str, route: RouteDecision | None = None,
                 top_k: int | None = None, user_id: str = ""):
        top_k = top_k or config.TOP_K
        cand_k = config.CANDIDATE_K

        where = self.rbac.vector_prefilter(role)
        dense = self.semantic.search(query, k=cand_k, where=where)
        sparse = self.bm25.search(query, k=cand_k)

        # Collect candidates by chunk id
        pool: dict[str, dict] = {}
        for r in dense:
            pool[r["id"]] = {"text": r["text"], "metadata": r["metadata"],
                             "semantic": r.get("semantic_score", 0.0), "bm25": 0.0}
        for r in sparse:
            entry = pool.setdefault(r["id"], {"text": r["text"], "metadata": r["metadata"],
                                              "semantic": 0.0, "bm25": 0.0})
            entry["bm25"] = r.get("bm25_score", 0.0)

        # Normalise each channel independently, then blend.
        sem_norm = _minmax({cid: e["semantic"] for cid, e in pool.items()})
        bm_norm = _minmax({cid: e["bm25"] for cid, e in pool.items()})

        boosted_depts = set(route.departments) if route else set()

        results: list[RetrievedChunk] = []
        decisions: list[AccessDecision] = []
        for cid, e in pool.items():
            meta = e["metadata"]
            decision = self.rbac.check(role, meta, user_id=user_id)
            decisions.append(decision)
            if not decision.allowed:
                continue  # never surface unauthorised content

            fused = self.alpha * sem_norm.get(cid, 0.0) + (1 - self.alpha) * bm_norm.get(cid, 0.0)
            boost = 0.10 if meta.get("department") in boosted_depts else 0.0
            results.append(RetrievedChunk(
                chunk_id=cid, text=e["text"], metadata=meta,
                semantic_score=e["semantic"], bm25_score=e["bm25"],
                fused_score=min(1.0, fused + boost), route_boost=boost))

        results.sort(key=lambda c: c.fused_score, reverse=True)
        return results[:top_k], decisions
