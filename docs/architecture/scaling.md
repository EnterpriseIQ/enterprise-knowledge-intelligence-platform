# Scaling Model

The default repository is designed for single-node resilience and evaluation. When transitioning to a production enterprise environment, consider the following scaling vectors.

## 1. Stateless API Tier
The FastAPI application (`src/api`) is entirely stateless (except for the in-memory fallback indexes). You can run `N` instances behind a load balancer.

## 2. Distributed Vector Database
To scale to millions of documents, replace the local ChromaDB instance with a distributed setup.
- **Option A:** ChromaDB Client/Server mode.
- **Option B:** Swap the `VectorStore` interface in `src/vectorstore` to connect to Pinecone, Qdrant, or pgvector.

## 3. Dedicated Embedding Tier
By default, the API server loads `all-MiniLM-L6-v2` into its own memory space. For high throughput, decouple the embedding model:
- Host the embedding model on a dedicated GPU cluster using a framework like TEI (Text Embeddings Inference).
- Update the `Embedder` interface to make HTTP/gRPC calls to the dedicated cluster rather than computing vectors locally.

## 4. LLM Generation
If you enable `ERAG_LLM=1`, generation becomes I/O bound (waiting on the external API). Ensure you run FastAPI with sufficient asynchronous workers (e.g., using Gunicorn with Uvicorn workers) to prevent blocking the event loop during LLM API calls.
