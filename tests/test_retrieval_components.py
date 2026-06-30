import pytest
from unittest.mock import patch, MagicMock

from src.retrieval.reranker import Reranker, CrossEncoderReranker, BGEReranker
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.bm25_retriever import BM25Retriever

# ---------------- Reranker ----------------

def test_reranker_base_not_available():
    # Force CrossEncoder to fail initialization
    with patch("src.retrieval.reranker.CrossEncoder", side_effect=Exception("Failed")):
        reranker = Reranker("dummy")
        assert reranker.is_available is False
        assert reranker.rerank("query", ["t1", "t2"]) == [0.0, 0.0]

def test_reranker_base_empty_texts():
    with patch("src.retrieval.reranker.CrossEncoder"):
        reranker = Reranker("dummy")
        assert reranker.is_available is True
        assert reranker.rerank("query", []) == []

def test_reranker_base_success():
    with patch("src.retrieval.reranker.CrossEncoder") as mock_ce:
        mock_instance = MagicMock()
        mock_instance.predict.return_value = [0.9, 0.1]
        mock_ce.return_value = mock_instance

        reranker = Reranker("dummy")
        assert reranker.rerank("query", ["t1", "t2"]) == [0.9, 0.1]

def test_reranker_base_predict_exception():
    with patch("src.retrieval.reranker.CrossEncoder") as mock_ce:
        mock_instance = MagicMock()
        mock_instance.predict.side_effect = Exception("Prediction error")
        mock_ce.return_value = mock_instance

        reranker = Reranker("dummy")
        assert reranker.rerank("query", ["t1", "t2"]) == [0.0, 0.0]

def test_cross_encoder_reranker_init():
    with patch("src.retrieval.reranker.CrossEncoder"):
        reranker = CrossEncoderReranker()
        assert reranker.is_available is True

def test_bge_reranker_init():
    with patch("src.retrieval.reranker.CrossEncoder"):
        reranker = BGEReranker()
        assert reranker.is_available is True

# ---------------- Reciprocal Rank Fusion ----------------

def test_reciprocal_rank_fusion():
    results1 = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    results2 = [{"id": "b"}, {"id": "a"}, {"id": "d"}]

    # rank 'a': 1 in list1, 2 in list2
    # rank 'b': 2 in list1, 1 in list2
    # rank 'c': 3 in list1, none in list2
    # rank 'd': none in list1, 3 in list2

    k = 60
    fused = reciprocal_rank_fusion([results1, results2], k=k)

    expected_a = (1.0 / (k + 1)) + (1.0 / (k + 2))
    expected_b = (1.0 / (k + 2)) + (1.0 / (k + 1))
    expected_c = (1.0 / (k + 3))
    expected_d = (1.0 / (k + 3))

    assert fused["a"] == pytest.approx(expected_a)
    assert fused["b"] == pytest.approx(expected_b)
    assert fused["c"] == pytest.approx(expected_c)
    assert fused["d"] == pytest.approx(expected_d)

# ---------------- BM25 Builtin Fallback ----------------

def test_bm25_builtin_fallback():
    records = [
        {"id": "1", "text": "hello world test", "metadata": {}},
        {"id": "2", "text": "hello python", "metadata": {}},
        {"id": "3", "text": "python test test", "metadata": {}}
    ]

    # Force rank_bm25 to fail import to trigger builtin fallback
    with patch.dict("sys.modules", {"rank_bm25": None}):
        retriever = BM25Retriever(records)
        assert retriever.backend == "builtin-bm25"

        # Test searching for existing terms
        res = retriever.search("hello", k=2)
        assert len(res) == 2
        # Both doc 1 and doc 2 have 'hello'. Let's check IDs are returned.
        ids = {r["id"] for r in res}
        assert {"1", "2"} == ids

        # Test searching with empty records
        empty_retriever = BM25Retriever([])
        assert empty_retriever.search("test", k=5) == []

def test_bm25_builtin_unknown_term():
    records = [{"id": "1", "text": "hello world", "metadata": {}}]
    with patch.dict("sys.modules", {"rank_bm25": None}):
        retriever = BM25Retriever(records)
        res = retriever.search("unknown", k=1)
        assert len(res) == 0 # no matches above score 0
