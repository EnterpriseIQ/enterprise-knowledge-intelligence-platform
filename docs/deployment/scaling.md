# Scaling Deployment

By default, EnterpriseIQ operates as a monolithic application where the API, vector database, and ML models reside in the same memory space. While this is excellent for resilience and ease of deployment, scaling horizontally requires decoupling.

## Horizontal Pod Autoscaling (HPA)

To run multiple replicas of the API server (e.g., in Kubernetes):

### 1. Decouple ChromaDB
You cannot have multiple API replicas writing to the same local ChromaDB SQLite files concurrently.
- Run ChromaDB as a separate service (Client/Server mode).
- Update the `VectorStore` initialization in `src/vectorstore/chroma.py` to use `HttpClient` instead of `PersistentClient`.

### 2. Shared BM25 Index
The BM25 index is currently built in-memory at startup. In a multi-replica setup, either:
- Ensure the base dataset is identical across all pods at startup.
- Replace the BM25 implementation with a distributed search engine like Elasticsearch or OpenSearch.

### 3. Load Balancing
Once decoupled, you can configure an Ingress controller or Load Balancer to round-robin requests across your API replicas.

## Vertical Scaling
If you prefer not to decouple, you can vertically scale the instance running the Docker container. Memory is the primary bottleneck, as both the ChromaDB index and the BM25 index are held in RAM for fast querying.
