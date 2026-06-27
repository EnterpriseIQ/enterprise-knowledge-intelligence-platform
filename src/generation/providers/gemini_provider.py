import os

from src.retrieval.hybrid_retriever import RetrievedChunk

from .base import GenerationProvider


class GeminiProvider(GenerationProvider):
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self._model = model_name
        self._client = None

        try:
            from google import genai
            from google.genai import types

            if os.getenv("GEMINI_API_KEY"):
                self._client = genai.Client()
                self._types = types
        except ImportError:
            pass

    @property
    def name(self) -> str:
        return f"gemini:{self._model}"

    def is_available(self) -> bool:
        return self._client is not None

    def generate(self, query: str, chunks: list[RetrievedChunk], system_prompt: str) -> str | None:
        if not self.is_available():
            return None

        context = "\n\n".join(
            f"[{i}] (source: {c.metadata.get('title')}, {c.metadata.get('department')}) {c.text}"
            for i, c in enumerate(chunks, start=1)
        )
        user_msg = f"Context passages:\n{context}\n\nQuestion: {query}"

        try:
            resp = self._client.models.generate_content(
                model=self._model,
                contents=user_msg,
                config=self._types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=1024,
                ),
            )
            return resp.text.strip() or None
        except Exception:
            return None
