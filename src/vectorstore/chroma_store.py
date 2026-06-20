"""ChromaDB vector store with a transparent in-memory fallback.

The store persists chunk embeddings, text and security metadata. RBAC pre-filtering
is pushed *into* the vector query (via Chroma ``where`` filters) so that
unauthorised content is never even scored — defence in depth rather than filtering
after the fact.

If ChromaDB is unavailable, a NumPy cosine-similarity store provides the same
interface so the platform always runs.
"""

from __future__ import annotations

from src import config


class VectorStore:
    def __init__(self, embed_fn, persist_dir=None, collection_name=None):
        self._embed = embed_fn
        self.persist_dir = str(persist_dir or config.VECTORSTORE_DIR)
        self.collection_name = collection_name or config.COLLECTION_NAME
        self.backend = "memory"
        self._client = None
        self._collection = None
        self._mem: list[dict] = []  # fallback records
        self._try_chroma()

    def _try_chroma(self) -> None:
        try:
            import chromadb
            from chromadb.config import Settings

            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False, allow_reset=True),
            )
            # Reset to keep ingestion idempotent across runs.
            try:
                self._client.delete_collection(self.collection_name)
            except Exception:
                pass
            self._collection = self._client.create_collection(
                name=self.collection_name, metadata={"hnsw:space": "cosine"}
            )
            self.backend = "chromadb"
        except Exception:
            self._client = None
            self._collection = None
            self.backend = "memory"

    # --------------------------------------------------------------------- #
    def add(self, ids, texts, metadatas, embeddings=None):
        embeddings = embeddings or self._embed(texts)
        if self.backend == "chromadb":
            self._collection.add(
                ids=list(ids),
                documents=list(texts),
                metadatas=list(metadatas),
                embeddings=list(embeddings),
            )
        else:
            for i, t, m, e in zip(ids, texts, metadatas, embeddings, strict=False):
                self._mem.append({"id": i, "text": t, "metadata": m, "embedding": e})

    def count(self) -> int:
        if self.backend == "chromadb":
            return self._collection.count()
        return len(self._mem)

    # --------------------------------------------------------------------- #
    def query(self, query_text: str, k: int, where: dict | None = None) -> list[dict]:
        """Return up to ``k`` nearest chunks, optionally RBAC-prefiltered by ``where``."""
        q_emb = self._embed([query_text])[0]
        if self.backend == "chromadb":
            res = self._collection.query(
                query_embeddings=[q_emb],
                n_results=k,
                where=_to_chroma_where(where) if where else None,
            )
            out = []
            ids = res.get("ids", [[]])[0]
            docs = res.get("documents", [[]])[0]
            metas = res.get("metadatas", [[]])[0]
            dists = res.get("distances", [[]])[0]
            for i, d, m, dist in zip(ids, docs, metas, dists, strict=False):
                out.append(
                    {"id": i, "text": d, "metadata": m, "score": 1.0 - float(dist)}
                )  # cosine distance -> similarity
            return out
        return self._mem_query(q_emb, k, where)

    def _mem_query(self, q_emb, k, where) -> list[dict]:
        def ok(meta) -> bool:
            return _match_where(meta, where) if where else True

        scored = []
        for rec in self._mem:
            if not ok(rec["metadata"]):
                continue
            scored.append((_cosine(q_emb, rec["embedding"]), rec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"id": r["id"], "text": r["text"], "metadata": r["metadata"], "score": s}
            for s, r in scored[:k]
        ]

    def all_records(self) -> list[dict]:
        """Expose all chunks (used to build the BM25 sparse index)."""
        if self.backend == "chromadb":
            got = self._collection.get(include=["documents", "metadatas"])
            return [
                {"id": i, "text": t, "metadata": m}
                for i, t, m in zip(got["ids"], got["documents"], got["metadatas"], strict=False)
            ]
        return [{"id": r["id"], "text": r["text"], "metadata": r["metadata"]} for r in self._mem]


# --------------------------------------------------------------------------- #
def _cosine(a, b) -> float:
    dot = 0.0
    na_sq = 0.0
    nb_sq = 0.0
    for x, y in zip(a, b, strict=False):
        dot += x * y
        na_sq += x * x
        nb_sq += y * y
    na = na_sq**0.5 or 1.0
    nb = nb_sq**0.5 or 1.0
    return dot / (na * nb)


def _to_chroma_where(where: dict) -> dict:
    """Translate a simple {field: value | {'$in': [...]}} filter for Chroma.

    Combine multiple conditions with ``$and`` as required by recent Chroma.
    """
    conds = []
    for key, val in where.items():
        conds.append({key: val})
    if len(conds) == 1:
        return conds[0]
    return {"$and": conds}


def _match_where(meta: dict, where: dict) -> bool:
    for key, cond in where.items():
        value = meta.get(key)
        if isinstance(cond, dict) and "$in" in cond:
            if value not in cond["$in"]:
                return False
        elif value != cond:
            return False
    return True
