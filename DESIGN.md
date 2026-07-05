# EnterpriseIQ Design Decisions

This document outlines the key technical design decisions that differentiate EnterpriseIQ from standard LangChain/LlamaIndex wrappers.

## 1. Unified Index for Heterogeneous Data

**Decision:** Store PDFs, SQL records, and JSON logs in a single ChromaDB collection.
**Rationale:** Standard RAG pipelines often silo structured and unstructured data, requiring complex multi-agent routing. By chunking structured data into self-contained descriptive text blocks, we enable a single semantic search space, reducing query latency and architectural complexity.

## 2. Min-Max Fused Hybrid Retrieval

**Decision:** Combine Dense Vector Search (SentenceTransformers) with Sparse Keyword Search (BM25) using a normalized Min-Max fusion algorithm.
**Rationale:** Vector embeddings struggle with exact entity matches (e.g., finding a specific incident ticket like `INC-1234` or a specific SKU). BM25 handles exact keyword matches perfectly. Fusing them ensures high recall across both semantic concepts and specific identifiers.

## 3. Strict Two-Layer RBAC

**Decision:** Enforce access control at two distinct layers:
-   **Pre-Filter:** Filter by department and clearance level during vector retrieval.
-   **Post-Filter:** Evaluate explicit Allow/Deny ACLs on the retrieved candidates before passing them to the generator.
**Rationale:** In an enterprise environment, leaking cross-department data is a critical security failure. The two-layer approach guarantees that the LLM/Generator *never* sees unauthorized context, mathematically preventing data leakage in the generated output.

## 4. Extractive-First Generation

**Decision:** Default to an "Offline Extractive Mode" that extracts verbatim snippets rather than synthesizing new text.
**Rationale:** Generative LLMs hallucinate. By restricting the output to exact strings found in the retrieved context, we guarantee zero hallucinations. While we support external LLMs (via the `llm` optional dependency) for nuanced synthesis, the default mode prioritizes absolute factual accuracy over conversational fluency.

## 5. Explicit Value-Based Deduplication

**Decision:** Use explicit unique identifiers (`chunk_id`) for Set operations and membership tests instead of relying on memory addresses (`id()`).
**Rationale:** Dataclasses representing retrieved chunks can easily duplicate during hybrid retrieval or diversification stages. Relying on explicit IDs prevents subtle deduplication bugs and ensures accurate citation attribution.

## 6. Graceful Degradation

**Decision:** Implement auto-fallbacks for critical components (e.g., falling back to a deterministic hashing embedder if SentenceTransformers fails).
**Rationale:** Enterprise infrastructure can be fragile, especially in air-gapped environments. The platform must prioritize availability; a degraded search is better than a complete outage.
