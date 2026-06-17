## 2024-05-18 - [Batch Vector Search for Expanded Queries]
**Learning:** Sequential vector searches during query expansion cause significant latency bottlenecks due to repeated transformer embedding operations.
**Action:** Always batch expanded queries using `query_texts` (or vector DB equivalent list properties) to evaluate all embeddings simultaneously, especially when using sentence transformers and ChromaDB.
