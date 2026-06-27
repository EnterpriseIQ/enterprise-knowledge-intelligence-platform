# System Architecture

EnterpriseIQ is built around a secure, multi-stage pipeline. Unlike traditional RAG systems that directly pipe vector search results to an LLM, EnterpriseIQ introduces explicit routing, hybrid fusion, and two-stage RBAC before generation.

## High-Level Architecture

```mermaid
graph TD
    subgraph Data Sources
        A1[PDFs]
        A2[SQL DBs]
        A3[JSON Logs]
    end

    subgraph Ingestion Pipeline
        B[Document Parsers]
        C[Semantic Chunker]
        D[all-MiniLM-L6-v2 Embedder]
    end

    subgraph Storage
        E[(ChromaDB Vector Store)]
        F[(BM25 Sparse Index)]
    end

    subgraph Retrieval Pipeline
        G[Intent Router]
        H[Hybrid Fusion Engine]
        I[Pre-filter RBAC]
        J[Post-filter ACL]
    end

    subgraph Generation
        K[Context Assembler]
        L[Extractive/LLM Backend]
        M[Citation & Confidence Grader]
    end

    A1 --> B
    A2 --> B
    A3 --> B
    B --> C
    C --> D
    D --> E
    B --> F

    UserQuery --> G
    G --> I
    I --> H
    H --> J
    E -.-> H
    F -.-> H
    J --> K
    K --> L
    L --> M
    M --> FinalAnswer
```

## Key Architectural Decisions

1. **Single Fused Index:** All data types share one vector space and one BM25 index. This allows a single query to retrieve a policy PDF, a SQL record, and an incident log, ranking them uniformly.
2. **Offline-First:** By default, all models run locally. The generation uses an extractive approach rather than generative to mathematically guarantee zero hallucinations.
3. **Graceful Degradation:** If SentenceTransformers fails to load, the system falls back to a deterministic hashing embedder to maintain availability.
