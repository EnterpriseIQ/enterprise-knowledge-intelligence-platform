import re
from typing import Optional

from src.generation.confidence import _terms
from src.retrieval.hybrid_retriever import RetrievedChunk
from .base import GenerationProvider

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_REFUSAL = ("I could not find sufficient authorised evidence to answer this "
            "question confidently. Please refine the question or check that you "
            "have access to the relevant documents.")

class ExtractiveProvider(GenerationProvider):
    """The default, fully offline, grounded extractive fallback provider."""

    def __init__(self, max_sentences: int = 4):
        self.max_sentences = max_sentences

    @property
    def name(self) -> str:
        return "extractive"

    def generate(self, query: str, chunks: list[RetrievedChunk], system_prompt: str) -> Optional[str]:
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
        chosen = scored[:self.max_sentences]
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
