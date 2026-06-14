"""Retrieval, routing, citation and confidence tests."""
from __future__ import annotations

from src.retrieval.query_router import QueryRouter


def test_router_classifies_departments():
    r = QueryRouter()
    assert "HR" in r.classify("What is the remote work policy?").departments
    assert "Finance" in r.classify("Show finance budget allocations").departments
    assert "Engineering" in r.classify("Show deployment standards").departments
    assert "Compliance" in r.classify("Summarize latest audit findings").departments


def test_router_intent():
    r = QueryRouter()
    assert r.classify("Summarize latest audit findings").intent == "summarize"
    assert r.classify("How many servers are healthy?").intent == "aggregate"


def test_hybrid_retrieval_returns_relevant(pipeline):
    res = pipeline.query("What is the remote work policy?", role="HR")
    assert res.citations
    assert res.citations[0]["department"] == "HR"
    # The remote work policy doc should be the top source.
    assert "Remote" in res.citations[0]["title"]


def test_citations_have_markers_and_snippets(pipeline):
    res = pipeline.query("Show engineering deployment standards.", role="Engineering")
    for i, c in enumerate(res.citations, start=1):
        assert c["marker"] == i
        assert c["snippet"]
        assert c["reference"].startswith(f"[{i}]")


def test_answer_is_grounded_with_citations(pipeline):
    res = pipeline.query("What is the remote work policy?", role="HR")
    # Every grounded answer cites at least one marker.
    assert "[1]" in res.answer
    assert res.confidence["label"] in {"high", "medium"}


def test_low_confidence_refuses(pipeline):
    """An out-of-corpus question should yield low confidence / a refusal, not a guess."""
    res = pipeline.query("What is the airspeed velocity of an unladen swallow?", role="Admin")
    assert res.confidence["label"] in {"low", "none", "medium"}


def test_cross_source_coverage(pipeline):
    """A broad engineering/ops question should be able to span >1 source type."""
    res = pipeline.query("Show recent operational tickets and platform incidents.",
                         role="Admin")
    assert res.coverage["source_types"]
