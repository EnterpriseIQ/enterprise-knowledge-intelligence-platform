## 2024-05-18 - Optimized pure-Python BM25 implementation using Inverted Index
**Learning:** The fallback pure-Python BM25 loop was extremely slow because it iterated `O(|query| * N)` over all documents, causing massive delays on larger document sets.
**Action:** Always check if scoring formulas over large collections can be optimized using inverted indices. I implemented one which brought the performance down from O(N) to O(M) where M << N, drastically speeding up search times while avoiding external dependencies.
