from abc import ABC, abstractmethod

from src.retrieval.hybrid_retriever import RetrievedChunk


class GenerationProvider(ABC):
    """Base class for all answer generation providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider, e.g., 'anthropic:claude-opus-4-8'."""
        pass

    @abstractmethod
    def generate(
        self, query: str, chunks: list[RetrievedChunk], system_prompt: str
    ) -> str | None:
        """Generate an answer using the given chunks and system prompt.

        Returns:
            The generated text string, or None if the generation fails (to trigger fallback).
        """
        pass
