# Deployment Architecture

EnterpriseIQ is designed to be easily containerised and deployed in modern orchestrators like Kubernetes, Docker Swarm, or AWS ECS.

## Standard Container Deployment

The provided `Dockerfile` builds a single, stateless container that encapsulates the FastAPI server, the retrieval pipeline, and the local embedding models. The Vector Database (ChromaDB) and Sparse Index (BM25) are persisted to a mounted volume.

```mermaid
graph TD
    subgraph Cloud/On-Prem Environment
        LB[Load Balancer]

        subgraph Compute
            APP1[EnterpriseIQ App Container]
            APP2[EnterpriseIQ App Container]
        end

        subgraph Storage
            VOL[(Persistent Volume: /data)]
        end

        LB --> APP1
        LB --> APP2
        APP1 --> VOL
        APP2 --> VOL
    end
```

### Constraints
- **Concurrency:** ChromaDB runs in-memory/local-file mode. If scaling horizontally (multiple app containers), you must configure ChromaDB in client/server mode and run it as a separate service, OR use sticky sessions to a single container (not recommended for HA).

## Scaled / Distributed Deployment

For high-availability enterprise environments, the components should be decoupled:

1. **API Tier:** Multiple FastAPI instances running statelessly.
2. **Vector DB Tier:** A dedicated ChromaDB cluster or enterprise vector database (e.g., Pinecone, Qdrant).
3. **LLM Tier (Optional):** Dedicated inference servers (e.g., vLLM or Ollama) or managed APIs (Anthropic/OpenAI) if not using the offline extractive mode.

```mermaid
graph TD
    LB[Load Balancer] --> API1[FastAPI Tier]
    LB --> API2[FastAPI Tier]

    API1 --> VDB[(Distributed Vector DB)]
    API2 --> VDB

    API1 --> LLM[vLLM / Inference Server]
    API2 --> LLM
```
