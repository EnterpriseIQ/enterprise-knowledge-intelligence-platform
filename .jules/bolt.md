## 2024-05-18 - Optimized pure-Python BM25 implementation using Inverted Index
**Learning:** The fallback pure-Python BM25 loop was extremely slow because it iterated `O(|query| * N)` over all documents, causing massive delays on larger document sets.
**Action:** Always check if scoring formulas over large collections can be optimized using inverted indices. I implemented one which brought the performance down from O(N) to O(M) where M << N, drastically speeding up search times while avoiding external dependencies.
## 2024-05-18 - Optimized cross-source diversification deduplication
**Learning:** The cross-source diversification fallback top-up logic was using an `O(N*M)` membership check (`if c not in selected:`) on lists, causing massive slowdowns on larger candidate result sets and when capping parameters frequently kick in.
**Action:** Used an `O(1)` ID set map (`selected_set = {id(c) for c in selected}`) for `O(1)` amortized lookups to optimize performance on deduplication iteration fallback checks.
