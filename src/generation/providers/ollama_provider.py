import os

import requests

from src.retrieval.hybrid_retriever import RetrievedChunk

from .base import GenerationProvider


class OllamaProvider(GenerationProvider):
    def __init__(self, model_name: str = "llama3"):
        self._model = os.getenv("OLLAMA_MODEL", model_name)
        self._base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    @property
    def name(self) -> str:
        return f"ollama:{self._model}"

    def is_available(self) -> bool:
        # Note: We won't eagerly check the API here as it might be down on init
        # but available during query.
        return True

    def generate(self, query: str, chunks: list[RetrievedChunk], system_prompt: str) -> str | None:
        context = "\n\n".join(
            f"[{i}] (source: {c.metadata.get('title')}, {c.metadata.get('department')}) "
            f"{c.text}" for i, c in enumerate(chunks, start=1)
        )
        user_msg = f"Context passages:\n{context}\n\nQuestion: {query}"

        try:
            resp = requests.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    "stream": False,
                    "options": {
                        "num_predict": 1024
                    }
                },
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip() or None
        except Exception:
            return None
