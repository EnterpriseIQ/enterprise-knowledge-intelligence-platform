## 2024-05-18 - Optimized pure-Python BM25 implementation using Inverted Index
**Learning:** The fallback pure-Python BM25 loop was extremely slow because it iterated `O(|query| * N)` over all documents, causing massive delays on larger document sets.
**Action:** Always check if scoring formulas over large collections can be optimized using inverted indices. I implemented one which brought the performance down from O(N) to O(M) where M << N, drastically speeding up search times while avoiding external dependencies.

## 2024-06-25 - Optimized `diversify` chunk check
**Learning:** Found an O(n²) bottleneck in `src/retrieval/cross_source.py` where a list check `if c not in selected:` iterated over the `selected` list for every remaining chunk when topping up diversity. For large contexts, this causes an unnecessary spike in retrieval latency.
**Action:** Replaced the list `in` check with a set of `chunk_id` properties (`{c.chunk_id for c in selected}`) allowing an O(1) membership test and reducing the fallback top-up to O(n). Using specific properties (like ID) for sets is safer than memory addresses, ensuring identical values correctly deduplicate. Always use sets for membership testing.
