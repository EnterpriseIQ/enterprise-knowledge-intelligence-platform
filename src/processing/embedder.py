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

from src import config


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self._model = None
        self.backend = "hashing-fallback"
        self.dim = config.EMBEDDING_DIM_FALLBACK
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
        if self._model is not None:
            vecs = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
            return [v.tolist() for v in vecs]
        return [self._hash_embed(t) for t in texts]

    # --------------------------------------------------------------------- #
    def _hash_embed(self, text: str) -> list[float]:
        """Deterministic bag-of-words hashing embedding, L2-normalised.

        Not as expressive as a transformer, but it is dependency-free, stable and
        good enough to demonstrate the full retrieval pipeline offline.
        """
        vec = [0.0] * self.dim
        tokens = [t for t in _tokenise(text)]
        for tok in tokens:
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if (h >> 8) & 1 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def _tokenise(text: str) -> list[str]:
    import re

    return re.findall(r"[a-z0-9]+", text.lower())
