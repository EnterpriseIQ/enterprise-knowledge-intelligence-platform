"""Confidence Scoring Engine.

Produces a calibrated-ish confidence signal for an answer from four observable
retrieval properties, without needing ground truth:

* **Top relevance** — fused score of the best supporting chunk.
* **Support** — how many chunks clear a usefulness threshold (more corroboration
  is better).
* **Agreement** — whether the top chunks agree on a source/department.
* **Query coverage** — fraction of meaningful query terms present in the context.

These are combined into a 0–1 score and bucketed into high / medium / low labels
that the API surfaces to the user. The aim is honesty: low retrieval support yields
low confidence and an explicit "insufficient evidence" answer rather than a guess.
"""
from __future__ import annotations

import re

from src import config
from src.retrieval.hybrid_retriever import RetrievedChunk

_STOP = {"the", "a", "an", "is", "are", "what", "show", "of", "to", "and", "for",
         "in", "on", "me", "our", "latest", "recent", "please", "give"}


def _terms(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in _STOP and len(t) > 2}


def score_confidence(query: str, chunks: list[RetrievedChunk]) -> dict:
    if not chunks:
        return {"score": 0.0, "label": "none",
                "explanation": "No authorised, relevant context was retrieved."}

    q_terms = _terms(query)

    # Lexical grounding is the dominant, embedding-agnostic signal: how much of the
    # question is actually answered by the retrieved text. This is what lets the
    # platform say "insufficient evidence" instead of hallucinating when the corpus
    # does not contain the answer (the fused score alone is min-max normalised and
    # would always look confident).
    chunk_terms = [_terms(c.text) for c in chunks[:5]]
    top_terms = chunk_terms[0]
    context_terms: set[str] = set()
    for terms in chunk_terms[:3]:
        context_terms |= terms

    if q_terms:
        coverage = len(q_terms & context_terms) / len(q_terms)        # over top-3
        top_coverage = len(q_terms & top_terms) / len(q_terms)        # over top-1
    else:
        coverage = top_coverage = 0.5  # vague query: stay neutral

    # Corroboration: how many of the top chunks actually mention a query term.
    support = sum(1 for terms in chunk_terms if q_terms & terms)
    support_factor = min(1.0, support / 3.0)

    top_doc = chunks[0].metadata.get("doc_id")
    agreement = sum(1 for c in chunks[:3]
                    if c.metadata.get("doc_id") == top_doc) / min(3, len(chunks))

    score = (0.50 * coverage + 0.25 * top_coverage
             + 0.15 * support_factor + 0.10 * agreement)
    score = round(min(1.0, score), 4)

    if score >= config.CONFIDENCE_HIGH:
        label = "high"
    elif score >= config.CONFIDENCE_LOW:
        label = "medium"
    else:
        label = "low"

    explanation = (
        f"query_term_coverage={round(coverage,2)}, top_chunk_coverage={round(top_coverage,2)}, "
        f"supporting_chunks={support}, source_agreement={round(agreement,2)}"
    )
    return {"score": score, "label": label, "explanation": explanation}
