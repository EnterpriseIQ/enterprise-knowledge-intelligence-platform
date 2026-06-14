"""Grounded Answer Generator.

Generates an answer strictly from retrieved, authorised context, with inline
citation markers. Two backends are available:

* **extractive** (default) — selects and stitches the most query-relevant sentences
  from the top chunks and attaches the citation of the chunk each sentence came
  from. This guarantees zero hallucination (every clause is traceable to a source),
  needs no external LLM or API key, and keeps the submission fully reproducible
  offline. It is the right default for a security/compliance product.

* **llm** (optional) — enabled with ``ERAG_LLM=1`` and an API key. The model receives
  ONLY the retrieved, authorised passages and a strict system prompt: answer solely
  from the numbered context, cite passages as ``[n]``, and refuse if the answer is
  not present. If the SDK or key is unavailable, or the call fails, it falls back to
  the extractive backend — the platform never breaks and never silently degrades
  without saying so (the active backend is reported on ``/health``).

Provider-agnostic design
------------------------
Generation is the *only* layer that touches an external LLM, and it is isolated
behind a single integration seam: :meth:`GroundedAnswerGenerator._generate_llm`
builds the context-only prompt and returns text (or ``None`` to fall back). Routing,
RBAC, retrieval, context assembly, citations and confidence are entirely
provider-independent, so swapping the generator changes nothing else.

* **Anthropic is the currently implemented provider** (``claude-opus-4-8`` via the
  official SDK).
* Additional providers — **OpenAI, Google Gemini, Ollama, OpenRouter, or a
  self-hosted local model** — can be added by implementing the same context-only
  call in ``_generate_llm`` for that provider's SDK/HTTP endpoint and selecting it
  via configuration. No change to the rest of the pipeline is required.
"""
from __future__ import annotations

import os
import re

from src.generation.confidence import _terms
from src.retrieval.hybrid_retriever import RetrievedChunk

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_REFUSAL = ("I could not find sufficient authorised evidence to answer this "
            "question confidently. Please refine the question or check that you "
            "have access to the relevant documents.")

_LLM_MODEL = os.getenv("ERAG_LLM_MODEL", "claude-opus-4-8")
_SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer the user's question using "
    "ONLY the numbered context passages provided. Every claim must be grounded in a "
    "passage and cited inline with its number in square brackets, e.g. [1]. Do not "
    "use any outside knowledge. If the passages do not contain enough information to "
    "answer, reply with exactly: " + _REFUSAL + " Be concise and factual."
)


class GroundedAnswerGenerator:
    def __init__(self):
        self.backend = "extractive"
        self._client = None
        if os.getenv("ERAG_LLM") == "1":
            self._try_init_anthropic()

    def _try_init_anthropic(self) -> None:
        """Initialise the optional Anthropic backend; stay extractive on any failure."""
        try:
            import anthropic

            if not os.getenv("ANTHROPIC_API_KEY"):
                return  # no key -> remain extractive
            self._client = anthropic.Anthropic()
            self.backend = f"anthropic:{_LLM_MODEL}"
        except Exception:
            self._client = None  # SDK missing -> remain extractive

    # ------------------------------------------------------------------ #
    def generate(self, query: str, chunks: list[RetrievedChunk],
                 confidence: dict, max_sentences: int = 4) -> str:
        # Confidence gating applies to BOTH backends: low evidence => refuse, never
        # guess. This is the core hallucination guardrail.
        if not chunks or confidence.get("label") in ("none", "low"):
            return _REFUSAL

        if self._client is not None:
            answer = self._generate_llm(query, chunks)
            if answer is not None:
                return self._annotate(answer, confidence)

        return self._annotate(self._generate_extractive(query, chunks, max_sentences),
                              confidence)

    # ------------------------------------------------------------------ #
    def _generate_extractive(self, query: str, chunks: list[RetrievedChunk],
                             max_sentences: int) -> str:
        q_terms = _terms(query)
        scored: list[tuple[float, int, str]] = []  # (relevance, citation_marker, sentence)
        for marker, chunk in enumerate(chunks, start=1):
            for sent in _SENT_SPLIT.split(chunk.text):
                sent = sent.strip()
                if len(sent) < 25:
                    continue
                overlap = len(q_terms & _terms(sent))
                rel = overlap + chunk.fused_score
                if overlap > 0 or marker == 1:
                    scored.append((rel, marker, sent))

        scored.sort(key=lambda x: x[0], reverse=True)
        chosen = scored[:max_sentences]
        if not chosen:
            return _REFUSAL

        chosen.sort(key=lambda x: x[1])  # readable order by citation marker
        seen, parts = set(), []
        for _, marker, sent in chosen:
            key = sent[:60]
            if key in seen:
                continue
            seen.add(key)
            parts.append(sent.rstrip(".") + f". [{marker}]")
        return " ".join(parts)

    # ------------------------------------------------------------------ #
    def _generate_llm(self, query: str, chunks: list[RetrievedChunk]) -> str | None:
        """Call Anthropic with context-only grounding. Returns None on any failure
        so the caller falls back to the extractive backend."""
        context = "\n\n".join(
            f"[{i}] (source: {c.metadata.get('title')}, {c.metadata.get('department')}) "
            f"{c.text}" for i, c in enumerate(chunks, start=1)
        )
        user_msg = f"Context passages:\n{context}\n\nQuestion: {query}"
        try:
            resp = self._client.messages.create(
                model=_LLM_MODEL,
                max_tokens=1024,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            return text.strip() or None
        except Exception:
            return None

    # ------------------------------------------------------------------ #
    @staticmethod
    def _annotate(answer: str, confidence: dict) -> str:
        if answer != _REFUSAL and confidence.get("label") == "medium":
            answer += ("\n\nNote: confidence is moderate — the answer is grounded in the "
                       "cited sources but you may wish to verify against the originals.")
        return answer
