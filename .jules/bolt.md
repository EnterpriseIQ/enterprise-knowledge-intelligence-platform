## 2024-05-18 - Optimized pure-Python BM25 implementation using Inverted Index
**Learning:** The fallback pure-Python BM25 loop was extremely slow because it iterated `O(|query| * N)` over all documents, causing massive delays on larger document sets.
**Action:** Always check if scoring formulas over large collections can be optimized using inverted indices. I implemented one which brought the performance down from O(N) to O(M) where M << N, drastically speeding up search times while avoiding external dependencies.

## 2024-05-18 - Optimized sequential query expansion in hybrid retrieval
**Learning:** During query expansion, running multiple dense and sparse searches sequentially in a loop blocked the main thread and caused linear scale latency ($O(K \times Q)$) which is a major bottleneck on large I/O bounds for vectorstores.
**Action:** Always consider using `concurrent.futures.ThreadPoolExecutor` when performing multiple independent retrieval queries on external services or IO-bound operations (like multi-query expansion) to execute them concurrently, significantly reducing response times.
