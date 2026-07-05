# System Architecture Deep Dive

EnterpriseIQ is designed to be resilient, offline-capable, and highly secure.

## The Agentic RAG Pipeline

Instead of a linear pipeline, EnterpriseIQ uses a LangGraph-based agentic state machine.

```mermaid
stateDiagram-v2
    [*] --> ClassifyIntent
    ClassifyIntent --> RetrieveVector: Intent = Semantic
    ClassifyIntent --> RetrieveSparse: Intent = Exact Match
    ClassifyIntent --> HybridRetrieve: Intent = General

    RetrieveVector --> FilterRBAC
    RetrieveSparse --> FilterRBAC
    HybridRetrieve --> FilterRBAC

    FilterRBAC --> AssembleContext
    AssembleContext --> GenerateAnswer
    GenerateAnswer --> GradeConfidence
    GradeConfidence --> [*]
```

## Storage Layer

The storage layer unifies structured and unstructured data into a single semantic space.

```mermaid
erDiagram
    DOCUMENT ||--o{ CHUNK : contains
    CHUNK ||--|| VECTOR : represented_by
    CHUNK ||--|| SPARSE_TOKENS : represented_by

    DOCUMENT {
        string id
        string department
        string clearance
    }
    CHUNK {
        string chunk_id
        string text
    }
```

For more, see the [Design Decisions](design.md).
