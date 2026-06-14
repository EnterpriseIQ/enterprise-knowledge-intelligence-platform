"""Answer-generator tests: backend selection, grounding, and LLM fallback.

These lock in that the optional LLM backend is a real, working code path (it parses
Anthropic-style responses and degrades gracefully), not a placeholder.
"""
from __future__ import annotations

from src.generation.answer_generator import _REFUSAL, GroundedAnswerGenerator
from src.retrieval.hybrid_retriever import RetrievedChunk


def _chunks():
    return [
        RetrievedChunk(chunk_id="d::0", text="The remote work policy allows three days "
                       "remote per week with VPN access.",
                       metadata={"title": "Remote Work Policy", "department": "HR",
                                 "page": 1, "source_type": "pdf", "doc_id": "hr-remote"},
                       fused_score=0.9),
    ]


HIGH = {"label": "high", "score": 0.9}
LOW = {"label": "low", "score": 0.1}


def test_default_backend_is_extractive():
    assert GroundedAnswerGenerator().backend == "extractive"


def test_low_confidence_refuses():
    gen = GroundedAnswerGenerator()
    assert gen.generate("anything", _chunks(), LOW) == _REFUSAL


def test_extractive_answer_is_grounded_and_cited():
    gen = GroundedAnswerGenerator()
    ans = gen.generate("What is the remote work policy?", _chunks(), HIGH)
    assert "[1]" in ans
    assert "remote" in ans.lower()


def test_llm_enabled_without_key_falls_back_to_extractive(monkeypatch):
    """ERAG_LLM=1 but no API key must not crash and must stay extractive."""
    monkeypatch.setenv("ERAG_LLM", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    gen = GroundedAnswerGenerator()
    assert gen.backend == "extractive"
    assert "[1]" in gen.generate("What is the remote work policy?", _chunks(), HIGH)


def test_llm_path_parses_response_and_failure_falls_back():
    """Drive the LLM code path with a stub client (no network)."""
    gen = GroundedAnswerGenerator()

    class _Block:
        type = "text"
        text = "Employees may work remotely three days per week [1]."

    class _Resp:
        content = [_Block()]

    class _OKClient:
        class messages:
            @staticmethod
            def create(**kwargs):
                # The model must receive context-only grounding input.
                assert "Context passages" in kwargs["messages"][0]["content"]
                return _Resp()

    gen._client = _OKClient()
    gen.backend = "anthropic:test"
    out = gen.generate("remote work policy", _chunks(), HIGH)
    assert out.startswith("Employees may work remotely") and "[1]" in out

    class _BadClient:
        class messages:
            @staticmethod
            def create(**kwargs):
                raise RuntimeError("api down")

    gen._client = _BadClient()
    fallback = gen.generate("What is the remote work policy?", _chunks(), HIGH)
    assert "[1]" in fallback  # gracefully fell back to extractive
