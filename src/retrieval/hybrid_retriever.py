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

import os
from dataclasses import dataclass

from src import config
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.query_expansion import QueryExpander
from src.retrieval.query_router import RouteDecision
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.semantic_retriever import SemanticRetriever
from src.security.rbac import AccessDecision, RBACEngine
from src.vectorstore import VectorStore


@dataclass
class RetrievalRequest:
    query: str
    role: str
    route: RouteDecision | None = None
    top_k: int | None = None
    user_id: str = ""


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

        self.expander = QueryExpander()
        self.reranker = None
        if os.getenv("ERAG_RERANKER") == "1":
            self.reranker = CrossEncoderReranker()

    # ------------------------------------------------------------------ #
    def retrieve(self, request: RetrievalRequest):
        top_k = request.top_k or config.TOP_K
        cand_k = config.CANDIDATE_K

        where = self.rbac.vector_prefilter(request.role)

        # Query expansion
        queries = self.expander.expand(request.query)

        all_dense = []
        all_sparse = []
        for q in queries:
            all_dense.append(self.semantic.search(q, k=cand_k, where=where))
            all_sparse.append(self.bm25.search(q, k=cand_k))

        # Use RRF to fuse multi-query lists if we expanded
        if len(queries) > 1:
            dense_rrf = reciprocal_rank_fusion(all_dense)
            sparse_rrf = reciprocal_rank_fusion(all_sparse)
            # Reconstruct dense and sparse lists based on RRF rank
            dense_map = {}
            for d_list in all_dense:
                for d in d_list:
                    if d["id"] not in dense_map:
                        dense_map[d["id"]] = d
            dense = []
            for cid, score in dense_rrf.items():
                if cid in dense_map:
                    d_copy = dense_map[cid].copy()
                    d_copy["semantic_score"] = score
                    dense.append(d_copy)

            sparse_map = {}
            for s_list in all_sparse:
                for s in s_list:
                    if s["id"] not in sparse_map:
                        sparse_map[s["id"]] = s
            sparse = []
            for cid, score in sparse_rrf.items():
                if cid in sparse_map:
                    s_copy = sparse_map[cid].copy()
                    s_copy["bm25_score"] = score
                    sparse.append(s_copy)
        else:
            dense = all_dense[0]
            sparse = all_sparse[0]

        # Collect candidates by chunk id
        pool: dict[str, dict] = {}
        for r in dense:
            pool[r["id"]] = {
                "text": r["text"],
                "metadata": r["metadata"],
                "semantic": r.get("semantic_score", 0.0),
                "bm25": 0.0,
            }
        for r in sparse:
            entry = pool.setdefault(
                r["id"],
                {"text": r["text"], "metadata": r["metadata"], "semantic": 0.0, "bm25": 0.0},
            )
            entry["bm25"] = r.get("bm25_score", 0.0)

        # Normalise each channel independently, then blend.
        sem_norm = _minmax({cid: e["semantic"] for cid, e in pool.items()})
        bm_norm = _minmax({cid: e["bm25"] for cid, e in pool.items()})

        boosted_depts = set(request.route.departments) if request.route else set()

        results: list[RetrievedChunk] = []
        decisions: list[AccessDecision] = []
        for cid, e in pool.items():
            meta = e["metadata"]
            decision = self.rbac.check(request.role, meta, user_id=request.user_id)
            decisions.append(decision)
            if not decision.allowed:
                continue  # never surface unauthorised content

            fused = self.alpha * sem_norm.get(cid, 0.0) + (1 - self.alpha) * bm_norm.get(cid, 0.0)
            boost = 0.10 if meta.get("department") in boosted_depts else 0.0
            results.append(
                RetrievedChunk(
                    chunk_id=cid,
                    text=e["text"],
                    metadata=meta,
                    semantic_score=e["semantic"],
                    bm25_score=e["bm25"],
                    fused_score=min(1.0, fused + boost),
                    route_boost=boost,
                )
            )

        # Optional Reranking Step
        if self.reranker and self.reranker.is_available and results:
            texts_to_rerank = [r.text for r in results]
            rerank_scores = self.reranker.rerank(request.query, texts_to_rerank)
            rerank_norm = _minmax({r.chunk_id: s for r, s in zip(results, rerank_scores, strict=True)})
            for r in results:
                # Blend reranker score and original fused score
                # 0.7 reranker, 0.3 original
                r.fused_score = min(
                    1.0,
                    0.7 * rerank_norm.get(r.chunk_id, 0.0) + 0.3 * r.fused_score + r.route_boost,
                )

        results.sort(key=lambda c: c.fused_score, reverse=True)
        return results[:top_k], decisions
