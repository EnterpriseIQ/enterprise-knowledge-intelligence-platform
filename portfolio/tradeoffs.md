# Trade-offs

1. **Reciprocal Rank Fusion vs Weighted Linear Blend**
   - *Decision:* Used both depending on the step. Blended normalized dense/sparse scores linearly, but used RRF for merging expanded queries.
   - *Trade-off:* RRF doesn't need tuning, but ignores raw semantic score confidence.

2. **Cross-Encoder Reranking vs Bi-Encoders**
   - *Decision:* Used a Cross-Encoder for the top N results.
   - *Trade-off:* Significant latency increase for higher precision. Mitigated by only reranking a small candidate pool.

3. **In-Memory Agent State vs Database Checkpoints**
   - *Decision:* Implemented `MemorySaver` in LangGraph for offline execution and stateless API requests.
   - *Trade-off:* Does not support long-running multi-day conversation persistence out of the box without changing the checkpoint backend to Postgres.
