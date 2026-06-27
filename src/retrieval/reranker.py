import os

from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._model = None

        try:
            self._model = CrossEncoder(self._model_name)
        except Exception:
            self._model = None

    @property
    def is_available(self) -> bool:
        return self._model is not None

    def rerank(self, query: str, texts: list[str]) -> list[float]:
        if not self.is_available or not texts:
            return [0.0] * len(texts)

        try:
            pairs = [[query, text] for text in texts]
            scores = self._model.predict(pairs)
            return [float(score) for score in scores]
        except Exception:
            return [0.0] * len(texts)


class CrossEncoderReranker(Reranker):
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        super().__init__(os.getenv("RERANKER_MODEL", model_name))


class BGEReranker(Reranker):
    def __init__(self):
        super().__init__(os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base"))
