"""Generation layer: citations, confidence scoring, grounded answers."""

from src.generation.citation import build_citations
from src.generation.confidence import score_confidence

__all__ = ["build_citations", "score_confidence"]
