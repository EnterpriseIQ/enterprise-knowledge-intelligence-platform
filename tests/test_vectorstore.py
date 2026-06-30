import pytest
from unittest.mock import patch, MagicMock

from src.vectorstore.chroma_store import VectorStore, _cosine, _match_where


def dummy_embed(texts):
    # Dummy embedder that just returns length of text as a pseudo-embedding
    return [[float(len(t))] for t in texts]


def test_vectorstore_memory_fallback():
    # Force chromadb to fail import
    with patch.dict("sys.modules", {"chromadb": None}):
        store = VectorStore(dummy_embed)
        assert store.backend == "memory"

        # Test adding data
        store.add(
            ids=["1", "2"],
            texts=["hello", "world long"],
            metadatas=[{"dept": "HR"}, {"dept": "IT"}]
        )
        assert store.count() == 2

        # Test querying without where
        results = store.query("hello", k=2)
        assert len(results) == 2

        # Test querying with where exact match
        results = store.query("hello", k=2, where={"dept": "HR"})
        assert len(results) == 1
        assert results[0]["id"] == "1"

        # Test querying with where $in
        results = store.query("hello", k=2, where={"dept": {"$in": ["IT"]}})
        assert len(results) == 1
        assert results[0]["id"] == "2"

        # Test querying with where mismatch
        results = store.query("hello", k=2, where={"dept": "Finance"})
        assert len(results) == 0

        # Test all_records
        records = store.all_records()
        assert len(records) == 2
        assert records[0]["id"] == "1"


def test_cosine_similarity():
    assert _cosine([1, 0], [1, 0]) == 1.0
    assert _cosine([1, 0], [0, 1]) == 0.0


def test_match_where():
    meta = {"role": "Admin", "level": 2}

    # Exact match
    assert _match_where(meta, {"role": "Admin"}) is True
    assert _match_where(meta, {"role": "HR"}) is False

    # $in match
    assert _match_where(meta, {"role": {"$in": ["Admin", "HR"]}}) is True
    assert _match_where(meta, {"role": {"$in": ["HR", "Finance"]}}) is False

    # Multi-condition
    assert _match_where(meta, {"role": "Admin", "level": 2}) is True
    assert _match_where(meta, {"role": "Admin", "level": 1}) is False
