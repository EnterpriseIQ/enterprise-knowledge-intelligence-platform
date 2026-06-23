## 2024-05-18 - Optimized pure-Python BM25 implementation using Inverted Index
**Learning:** The fallback pure-Python BM25 loop was extremely slow because it iterated `O(|query| * N)` over all documents, causing massive delays on larger document sets.
**Action:** Always check if scoring formulas over large collections can be optimized using inverted indices. I implemented one which brought the performance down from O(N) to O(M) where M << N, drastically speeding up search times while avoiding external dependencies.
## 2025-05-18 - Avoid full list sort for Top-K items in Python
**Learning:** Python's built-in `sorted(list)` is O(N log N) which is extremely slow on large document score arrays. Finding the top K elements can be efficiently done in O(N log K) time using `heapq.nlargest`.
**Action:** Always prefer `heapq.nlargest` (or `heapq.nsmallest`) over `sorted(list)[:k]` when finding a small number of top items from a large list, particularly in retrieval scoring paths like BM25 or semantic search.
