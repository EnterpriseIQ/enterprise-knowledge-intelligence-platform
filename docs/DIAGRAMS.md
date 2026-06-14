# Architecture & Flow Diagrams

Six diagrams covering the platform from different angles. All render natively on
GitHub. The canonical high-level source also lives at
[`diagrams/architecture.mmd`](../diagrams/architecture.mmd).

---

## 1. High-Level Architecture

```mermaid
flowchart TB
    subgraph Sources["Enterprise Data Sources"]
        PDF["PDFs & Reports"]
        CSV["CSV Datasets"]
        SQL["SQL Database"]
        JSON["JSON Logs"]
    end
    subgraph Index["Indexing (offline)"]
        ING["Ingestion + Manifest"] --> CH["Chunking"] --> EMB["Embeddings"]
        EMB --> VEC[("ChromaDB")]
        CH --> BM["BM25 Index"]
    end
    subgraph Serve["Query-time"]
        R["Query Router"] --> H["Hybrid Retrieval"]
        H --> AC{{"RBAC Engine"}}
        AC --> CTX["Context Assembly"] --> GEN["Grounded Generation"]
        GEN --> OUT["Citations + Confidence"]
    end
    API["FastAPI / CLI"]
    AUD[("Audit Trail")]

    PDF & CSV & SQL & JSON --> ING
    H <--> VEC
    H <--> BM
    USER(["User + Role"]) --> API --> R
    OUT --> API
    AC -- decisions --> AUD
```

---

## 2. Data Flow (ingestion → index)

```mermaid
flowchart LR
    M["manifest.json<br/>dept · sensitivity · ACL"]
    subgraph L["Loaders"]
        P["pdf_loader"]
        C["csv_loader"]
        S["sql_loader"]
        J["json_loader"]
    end
    M --> L
    L --> RD["RawDocument<br/>text + security metadata"]
    RD --> CK["Chunker<br/>900c / 150 overlap / page tags"]
    CK --> CHK["Chunks<br/>(inherit doc metadata)"]
    CHK --> E["Embedder<br/>MiniLM / hashing fallback"]
    E --> VS[("Vector Store<br/>text+vector+metadata")]
    CHK --> B["BM25 sparse index"]
```

---

## 3. Retrieval Flow (hybrid fusion)

```mermaid
flowchart TB
    Q["Query"] --> PF["RBAC vector pre-filter<br/>(department scope)"]
    PF --> D["Dense search<br/>(ChromaDB cosine)"]
    Q --> SP["Sparse search<br/>(BM25)"]
    D --> POOL["Candidate pool<br/>(union by chunk id)"]
    SP --> POOL
    POOL --> NRM["Min-max normalise<br/>each channel"]
    NRM --> FUSE["Weighted fusion<br/>alpha·dense + (1-alpha)·sparse"]
    FUSE --> BOOST["Router department boost"]
    BOOST --> CHK2{{"Per-result RBAC re-check<br/>clearance + ACL"}}
    CHK2 -- allowed --> RANK["Rank + diversify<br/>(cap per doc)"]
    CHK2 -- denied --> DROP["Dropped + audited"]
    RANK --> TOPK["Top-k context"]
```

---

## 4. Query Processing (end-to-end request)

```mermaid
sequenceDiagram
    actor U as User (role)
    participant API as FastAPI /query
    participant P as RAGPipeline
    participant RT as Router
    participant HR as HybridRetriever
    participant AC as RBACEngine
    participant G as Generator
    participant AU as Audit

    U->>API: {query, role|user_id}
    API->>P: query(...)
    P->>AC: resolve_role()
    P->>RT: classify(query)
    RT-->>P: intent + departments
    P->>HR: retrieve(query, role)
    HR->>AC: check() per candidate
    AC-->>HR: allow / deny (+reason)
    HR-->>P: authorised chunks
    P->>G: generate(query, chunks, confidence)
    G-->>P: grounded answer + [n]
    P->>AU: log query + decisions
    P-->>API: answer, citations, confidence, routing, access_summary
    API-->>U: JSON response
```

---

## 5. RBAC Authorization (decision logic)

```mermaid
flowchart TD
    START["Candidate chunk + role"] --> ADM{"Role = Admin?"}
    ADM -- yes --> ALLOW["ALLOW"]
    ADM -- no --> DEPT{"doc.department in<br/>role.departments?"}
    DEPT -- no --> DENY["DENY<br/>reason: department scope"]
    DEPT -- yes --> CLR{"doc.sensitivity ≤<br/>role.clearance?"}
    CLR -- no --> DENY2["DENY<br/>reason: clearance"]
    CLR -- yes --> ACL{"doc has allowed_roles<br/>and role not listed?"}
    ACL -- yes --> DENY3["DENY<br/>reason: explicit ACL"]
    ACL -- no --> ALLOW
    ALLOW --> AUD["AccessDecision -> audit"]
    DENY --> AUD
    DENY2 --> AUD
    DENY3 --> AUD
```

---

## 6. Security Flow (defence in depth)

```mermaid
flowchart LR
    Q["Query + role"] --> L1["Layer 1<br/>vector pre-filter<br/>(department)"]
    L1 --> CAND["Candidate set<br/>(dense + sparse)"]
    CAND --> L2["Layer 2<br/>per-result RBAC<br/>(clearance + ACL)"]
    L2 -- allowed --> CTX["Context window<br/>(authorised only)"]
    L2 -- denied --> X["Never enters context"]
    CTX --> ANS["Grounded answer<br/>(cite or refuse)"]
    L1 -. decision .-> AUD[("Audit trail")]
    L2 -. decision .-> AUD
    X -. denial+reason .-> AUD
```

> **Why two layers?** BM25 runs over the full corpus and is *not* department
> pre-filtered, so Layer 2's per-result check is the authoritative chokepoint that
> guarantees no unauthorised chunk — from either channel — ever reaches generation.
