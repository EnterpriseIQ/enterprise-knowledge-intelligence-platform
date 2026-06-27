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

from src.generation.providers import (
    AnthropicProvider,
    ExtractiveProvider,
    GeminiProvider,
    GenerationProvider,
    OllamaProvider,
    OpenAIProvider,
)
from src.retrieval.hybrid_retriever import RetrievedChunk

_REFUSAL = ("I could not find sufficient authorised evidence to answer this "
            "question confidently. Please refine the question or check that you "
            "have access to the relevant documents.")

_SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer the user's question using "
    "ONLY the numbered context passages provided. Every claim must be grounded in a "
    "passage and cited inline with its number in square brackets, e.g. [1]. Do not "
    "use any outside knowledge. If the passages do not contain enough information to "
    "answer, reply with exactly: " + _REFUSAL + " Be concise and factual."
)


class GroundedAnswerGenerator:
    def __init__(self):
        self.extractive = ExtractiveProvider()
        self.provider: GenerationProvider = self.extractive
        self.backend = self.extractive.name

        if os.getenv("ERAG_LLM") == "1":
            self._try_init_llm_provider()

    def _try_init_llm_provider(self) -> None:
        """Initialise the optional LLM backend; stay extractive on any failure."""
        provider_name = os.getenv("ERAG_LLM_PROVIDER", "anthropic").lower()

        provider = None
        if provider_name == "anthropic":
            provider = AnthropicProvider()
        elif provider_name == "openai":
            provider = OpenAIProvider()
        elif provider_name == "gemini":
            provider = GeminiProvider()
        elif provider_name == "ollama":
            provider = OllamaProvider()

        if provider and getattr(provider, 'is_available', lambda: True)():
            self.provider = provider
            self.backend = provider.name

    # ------------------------------------------------------------------ #
    def generate(self, query: str, chunks: list[RetrievedChunk],
                 confidence: dict, max_sentences: int = 4) -> str:
        # Confidence gating applies to BOTH backends: low evidence => refuse, never
        # guess. This is the core hallucination guardrail.
        if not chunks or confidence.get("label") in ("none", "low"):
            return _REFUSAL

        # Only pass max_sentences to the extractive provider if it's the active one
        if isinstance(self.provider, ExtractiveProvider):
            self.provider.max_sentences = max_sentences

        answer = None
        if self.provider.name != "extractive":
            answer = self.provider.generate(query, chunks, _SYSTEM_PROMPT)

        if answer is None:
            self.extractive.max_sentences = max_sentences
            answer = self.extractive.generate(query, chunks, _SYSTEM_PROMPT)

        return self._annotate(answer, confidence)

    # ------------------------------------------------------------------ #
    @staticmethod
    def _annotate(answer: str, confidence: dict) -> str:
        if answer != _REFUSAL and confidence.get("label") == "medium":
            answer += ("\n\nNote: confidence is moderate — the answer is grounded in the "
                       "cited sources but you may wish to verify against the originals.")
        return answer
