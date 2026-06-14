"""Citation Engine.

Turns retrieved chunks into numbered, de-duplicated citations. Every fact in a
generated answer references one of these markers so the response is auditable back
to a specific document, page and chunk — the core of grounding and explainability.
"""
from __future__ import annotations

from src.retrieval.hybrid_retriever import RetrievedChunk


def build_citations(chunks: list[RetrievedChunk]) -> list[dict]:
    """Return ordered citation records with a stable 1-based ``marker``."""
    citations: list[dict] = []
    for i, c in enumerate(chunks, start=1):
        cite = c.to_citation()
        cite["marker"] = i
        loc = f"p.{cite['page']}" if cite.get("page") else cite["source_type"]
        cite["reference"] = f"[{i}] {cite['title']} ({cite['department']}, {loc})"
        cite["snippet"] = (c.text[:240] + "…") if len(c.text) > 240 else c.text
        citations.append(cite)
    return citations
