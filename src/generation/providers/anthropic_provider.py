import os

from src.retrieval.hybrid_retriever import RetrievedChunk

from .base import GenerationProvider


class AnthropicProvider(GenerationProvider):
    def __init__(self, model_name: str = None):
        self._model = model_name or os.getenv("ERAG_LLM_MODEL", "claude-opus-4-8")
        self._client = None

        try:
            import anthropic

            if os.getenv("ANTHROPIC_API_KEY"):
                self._client = anthropic.Anthropic()
        except ImportError:
            pass

    @property
    def name(self) -> str:
        return f"anthropic:{self._model}"

    def is_available(self) -> bool:
        return self._client is not None

    def generate(
        self, query: str, chunks: list[RetrievedChunk], system_prompt: str
    ) -> str | None:
        if not self.is_available():
            return None

        context = "\n\n".join(
            f"[{i}] (source: {c.metadata.get('title')}, {c.metadata.get('department')}) {c.text}"
            for i, c in enumerate(chunks, start=1)
        )
        user_msg = f"Context passages:\n{context}\n\nQuestion: {query}"

        try:
            if os.getenv("LANGFUSE_PUBLIC_KEY"):
                from langfuse import Langfuse

                lf = Langfuse()
                trace = lf.trace(name="anthropic_generation", input=user_msg)

            resp = self._client.messages.create(
                model=self._model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_msg}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")

            if os.getenv("LANGFUSE_PUBLIC_KEY"):
                trace.update(output=text)

            return text.strip() or None
        except Exception:
            return None
