"""Embedding layer.

Wraps SentenceTransformers for dense semantic embeddings. If the library or model
weights are unavailable (e.g. fully offline CI), it transparently falls back to a
deterministic hashing embedder so the platform always runs end to end. The active
backend is exposed via :attr:`Embedder.backend` for transparency in logs and the
API ``/health`` endpoint.
"""

from __future__ import annotations

import hashlib
import math

from cachetools import LRUCache

from src import config


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self._model = None
        self.backend = "hashing-fallback"
        self.dim = config.EMBEDDING_DIM_FALLBACK
        self._cache = LRUCache(maxsize=1000)
        self._try_load_sentence_transformer()

    def _try_load_sentence_transformer(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self.dim = self._model.get_sentence_embedding_dimension()
            self.backend = f"sentence-transformers:{self.model_name}"
        except Exception:
            # Stay on the deterministic fallback; never crash the pipeline.
            self._model = None

    # --------------------------------------------------------------------- #
    def embed(self, texts: list[str]) -> list[list[float]]:
        results = []
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            if text in self._cache:
                results.append(self._cache[text])
            else:
                results.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        if uncached_texts:
            if self._model is not None:
                new_vecs = self._model.encode(
                    uncached_texts, normalize_embeddings=True, show_progress_bar=False
                )
                new_vecs_list = [v.tolist() for v in new_vecs]
            else:
                new_vecs_list = [self._hash_embed(t) for t in uncached_texts]

            for i, idx in enumerate(uncached_indices):
                vec = new_vecs_list[i]
                self._cache[uncached_texts[i]] = vec
                results[idx] = vec

        return results

    # --------------------------------------------------------------------- #
    def _hash_embed(self, text: str) -> list[float]:
        """Deterministic bag-of-words hashing embedding, L2-normalised.

        Not as expressive as a transformer, but it is dependency-free, stable and
        good enough to demonstrate the full retrieval pipeline offline.
        """
        vec = [0.0] * self.dim
        tokens = [t for t in _tokenise(text)]
        for tok in tokens:
            h = int(hashlib.sha256(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if (h >> 8) & 1 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def _tokenise(text: str) -> list[str]:
    import re

    return re.findall(r"[a-z0-9]+", text.lower())
