# Architecture Overview

KnowledgeX employs a multi-agent orchestrated pipeline.

## Diagram

```mermaid
graph TD
    User([User Query]) --> Planner[Planner Agent]
    Planner --> Retriever[Retrieval Agent]
    Retriever --> Reasoner[Reasoning Agent]
    Reasoner -- Sufficient Information --> Responder[Response Agent]
    Reasoner -- Insufficient Information --> Planner

    Retriever -->|Query Expansion| QEx[Expander]
    QEx --> Dense[Semantic Vector Search]
    QEx --> Sparse[BM25 Lexical Search]

    Dense --> RRF[Reciprocal Rank Fusion]
    Sparse --> RRF

    RRF --> RBAC{RBAC Filter}
    RBAC --> Rerank[Cross-Encoder Reranker]
```

## Modularity
- **Retrieval Engine:** The `HybridRetriever` acts as a facade over `SemanticRetriever`, `BM25Retriever`, and the `CrossEncoderReranker`.
- **Generation:** The `GroundedAnswerGenerator` dynamically loads the registered Provider (e.g. `OllamaProvider`, `OpenAIProvider`).
