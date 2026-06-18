## 2024-06-18 - Optimize BM25 pure-Python fallback for sparsity
**Learning:** Initializing a dense O(N) array for scores on every search query creates severe memory and computation bottlenecks on large corpora.
**Action:** Always prefer sparse mappings like `defaultdict` to track only non-zero scores when evaluating lexical overlap. Also, sorting O(M) matched items is far more efficient than O(N).
