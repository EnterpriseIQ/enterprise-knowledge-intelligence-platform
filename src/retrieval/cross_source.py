"""Cross-Source Retrieval helper.

The hybrid engine already retrieves across all source types from a single fused
index. This module adds *coverage-aware* selection: given the fused candidates it
ensures the final context spans multiple sources/departments where relevant, so a
cross-cutting question ("recent platform incidents") can draw on both the incident
PDF and the operations SQL tickets rather than collapsing onto one source.
"""

from __future__ import annotations

from src.retrieval.hybrid_retriever import RetrievedChunk


def diversify(
    chunks: list[RetrievedChunk], top_k: int, max_per_doc: int = 2
) -> list[RetrievedChunk]:
    """Greedy selection that caps how many chunks come from any single document,
    promoting source diversity while preserving the fused ranking order."""
    selected: list[RetrievedChunk] = []
    per_doc: dict[str, int] = {}
    for c in chunks:
        doc = c.metadata.get("doc_id", "")
        if per_doc.get(doc, 0) >= max_per_doc:
            continue
        selected.append(c)
        per_doc[doc] = per_doc.get(doc, 0) + 1
        if len(selected) >= top_k:
            break
    # If capping left us short, top up with the remaining best chunks.
    if len(selected) < top_k:
        for c in chunks:
            if c not in selected:
                selected.append(c)
            if len(selected) >= top_k:
                break
    return selected


def source_coverage(chunks: list[RetrievedChunk]) -> dict:
    """Summarise which departments and source types the context spans."""
    depts: dict[str, int] = {}
    sources: dict[str, int] = {}
    for c in chunks:
        d = c.metadata.get("department", "?")
        s = c.metadata.get("source_type", "?")
        depts[d] = depts.get(d, 0) + 1
        sources[s] = sources.get(s, 0) + 1
    return {
        "departments": depts,
        "source_types": sources,
        "is_cross_source": len(sources) > 1 or len(depts) > 1,
    }
