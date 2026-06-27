# Performance Tuning

To get the best performance out of EnterpriseIQ, consider the following parameters.

## `HYBRID_ALPHA`
This environment variable (default `0.6`) controls the balance between Vector Search and BM25 Search.
- Set closer to `1.0` if users ask conceptual, long-form questions.
- Set closer to `0.0` if users frequently search for exact ID numbers (e.g., ticket numbers, employee IDs).

## Worker Count
If running the API under heavy load, increase the number of Uvicorn workers.
```bash
uvicorn src.api.main:app --workers 4
```

## Embedding Model
The default `all-MiniLM-L6-v2` is fast and lightweight. If accuracy is more important than speed, you can swap this in `src/vectorstore/chroma.py` for a larger model like `bge-large-en-v1.5`, though this will significantly increase embedding and query latency unless running on a GPU.
