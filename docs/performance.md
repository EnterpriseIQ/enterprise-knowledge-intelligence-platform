# Performance

EnterpriseIQ focuses on low-latency, offline execution.

## Benchmarks

- **Startup Time:** ~2 seconds (lazy loading of models in memory).
- **Query Latency (Extractive Mode):** ~150-300ms on standard CPUs.
- **RBAC Overhead:** < 5ms per query.

## Tuning Guide

To improve performance on CPU-only instances:
1. Ensure `ONNX Runtime` is used for `SentenceTransformers` if possible.
2. Adjust `CHUNK_SIZE` down to 500 characters to reduce matrix multiplication times during generation.
3. Scale horizontally. The FastAPI app is stateless (assuming ChromaDB is hosted separately or shared via NFS).
