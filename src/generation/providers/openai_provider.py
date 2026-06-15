import os
from typing import Optional

from src.retrieval.hybrid_retriever import RetrievedChunk
from .base import GenerationProvider

class OpenAIProvider(GenerationProvider):
    def __init__(self, model_name: str = "gpt-4o"):
        self._model = model_name
        self._client = None

        try:
            import openai
            if os.getenv("OPENAI_API_KEY"):
                self._client = openai.OpenAI()

                # Setup Langfuse
                if os.getenv("LANGFUSE_PUBLIC_KEY"):
                    from langfuse.openai import auth_check
                    auth_check() # Will throw if misconfigured, ensuring fail-fast
        except ImportError:
            pass

    @property
    def name(self) -> str:
        return f"openai:{self._model}"

    def is_available(self) -> bool:
        return self._client is not None

    def generate(self, query: str, chunks: list[RetrievedChunk], system_prompt: str) -> Optional[str]:
        if not self.is_available():
            return None

        context = "\n\n".join(
            f"[{i}] (source: {c.metadata.get('title')}, {c.metadata.get('department')}) "
            f"{c.text}" for i, c in enumerate(chunks, start=1)
        )
        user_msg = f"Context passages:\n{context}\n\nQuestion: {query}"

        try:
            # Check if langfuse is enabled to use the wrapper
            if os.getenv("LANGFUSE_PUBLIC_KEY"):
                from langfuse.openai import openai as lf_openai
                client = lf_openai
            else:
                client = self._client

            resp = client.chat.completions.create(
                model=self._model,
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
            )
            return resp.choices[0].message.content.strip() or None
        except Exception:
            return None
