"""Sparse (BM25) retriever.

Provides lexical retrieval that complements dense semantic search — strong on
exact identifiers, codes and rare terms (e.g. "INC-2025-021", "OPS-5044") that
embedding models can blur together. Built on ``rank-bm25`` with a pure-Python
fallback so the platform has no hard dependency on it.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict


def _tok(text: str) -> list[str]:
    return re.findall(r"[a-z0-9\-]+", text.lower())


class BM25Retriever:
    def __init__(self, records: list[dict]):
        """``records`` are {id, text, metadata} dicts from the vector store."""
        self.records = records
        self.corpus_tokens = [_tok(r["text"]) for r in records]
        self._impl = None
        self._build()

    def _build(self) -> None:
        try:
            from rank_bm25 import BM25Okapi

            self._impl = BM25Okapi(self.corpus_tokens) if self.corpus_tokens else None
            self.backend = "rank-bm25"
        except Exception:
            self._impl = None
            self.backend = "builtin-bm25"
            self._build_builtin()

    # ------------------------------------------------------------------ #
    def _build_builtin(self) -> None:
        self.N = len(self.corpus_tokens)
        self.avgdl = (sum(len(d) for d in self.corpus_tokens) / self.N) if self.N else 0.0
        self.df: Counter = Counter()
        self.inverted_index: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.doc_lens = [len(d) for d in self.corpus_tokens]

        for i, doc in enumerate(self.corpus_tokens):
            term_counts = Counter(doc)
            for term, count in term_counts.items():
                self.df[term] += 1
                self.inverted_index[term].append((i, count))

    def _builtin_scores(self, query_tokens, k1=1.5, b=0.75) -> dict[int, float]:
        # OPTIMIZATION: Instead of a dense array `[0.0] * self.N`, use a sparse dictionary.
        # This prevents O(N) allocation and scoring for massive corpora.
        scores = defaultdict(float)
        for term in query_tokens:
            if term not in self.df:
                continue
            idf = math.log(1 + (self.N - self.df[term] + 0.5) / (self.df[term] + 0.5))

            # Pre-calculate invariant terms for the inner loop
            idf_times_k1_plus_1 = idf * (k1 + 1)
            b_div_avgdl = b / (self.avgdl or 1.0)
            one_minus_b = 1 - b

            # Only iterate over documents that actually contain the term
            for i, f in self.inverted_index.get(term, []):
                dl = self.doc_lens[i]
                denom = f + k1 * (one_minus_b + b_div_avgdl * dl)
                scores[i] += (idf_times_k1_plus_1 * f) / denom
        return scores

    # ------------------------------------------------------------------ #
    def search(self, query: str, k: int) -> list[dict]:
        if not self.records:
            return []
        q_tokens = _tok(query)

        if self._impl is not None:
            scores = self._impl.get_scores(q_tokens)
            ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

            out = []
            for i in ranked[:k]:
                if scores[i] <= 0:
                    continue
                r = self.records[i]
                out.append(
                    {
                        "id": r["id"],
                        "text": r["text"],
                        "metadata": r["metadata"],
                        "bm25_score": float(scores[i]),
                    }
                )
            return out
        else:
            scores_dict = self._builtin_scores(q_tokens)
            # OPTIMIZATION: Only sort documents that actually match terms, taking O(M log M)
            # where M is the number of matched documents, instead of O(N log N) where N is all docs.
            ranked_items = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

            out = []
            for i, score in ranked_items[:k]:
                if score <= 0:
                    continue
                r = self.records[i]
                out.append(
                    {
                        "id": r["id"],
                        "text": r["text"],
                        "metadata": r["metadata"],
                        "bm25_score": float(score),
                    }
                )
            return out
