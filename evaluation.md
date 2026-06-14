# Evaluation Methodology

This document describes how the platform's quality and safety are evaluated:
hallucination mitigation, retrieval quality, RBAC correctness, citation validity, and
scalability. Where possible, evaluation is **automated in the test suite** so claims
are reproducible rather than aspirational.

## 1. Hallucination mitigation

Grounding is enforced *by construction*, then measured:

- **Extractive generation.** The default generator emits only sentences taken
  verbatim from retrieved, authorised chunks, each tagged with the citation marker of
  its source. There is no free-form generation step that could invent facts.
- **Cite-or-refuse.** If confidence is `low`/`none`, the generator returns an explicit
  *"insufficient authorised evidence"* message instead of an answer
  (`tests/test_retrieval.py::test_low_confidence_refuses`).
- **Confidence gating.** Confidence is dominated by **query-term coverage** in the
  retrieved text — an embedding-agnostic signal — so out-of-corpus questions score low
  and refuse. Example: *"airspeed velocity of an unladen swallow"* → confidence ≈ 0.03,
  refusal.
- **Metric.** *Groundedness rate* = fraction of answer sentences whose cited chunk
  contains them. Extractive generation makes this 100% by design; the test suite
  asserts every answer carries `[n]` markers and that the top citation is from the
  expected department.

## 2. Retrieval evaluation

| Dimension | Method | Signal |
|---|---|---|
| **Relevance (precision@k)** | Canonical queries with a known target document; assert it appears in the top-k. | `test_hybrid_retrieval_returns_relevant` puts the Remote Work Policy first for its query. |
| **Routing accuracy** | Each demo query has an expected department; assert the router selects it. | `test_router_classifies_departments`, `test_router_intent`. |
| **Hybrid vs. single-channel** | `HYBRID_ALPHA` blends dense+sparse; BM25 anchors exact IDs (`INC-2025-021`, `OPS-5044`) that pure-dense blurs. | Ablation: set `alpha=1.0` (dense only) vs default and compare ID-lookup recall. |
| **Cross-source coverage** | Broad queries should span >1 source type. | `source_coverage(...).is_cross_source`; `test_cross_source_coverage`. |

**Extending to labelled evaluation.** Drop a `qrels` file of *(query, relevant doc_ids)*
and compute precision@k / recall@k / MRR over the corpus. The pipeline already returns
ranked `citations` with `doc_id`, so this is a thin harness on top.

## 3. RBAC testing strategy

RBAC is the highest-weighted safety property and is tested at two levels:

- **Unit** (`tests/test_rbac.py`): department isolation, clearance enforcement,
  explicit ACLs, Admin bypass, Compliance cross-department read, and the vector
  pre-filter shape.
- **Integration** (pipeline + demo): the **leakage rate** — fraction of queries where a
  forbidden-department chunk appears in the citations — must be **0**.
  `test_pipeline_no_leakage` and `run_demo.py`'s Part 2 assert this and that denied
  documents were genuinely considered and blocked (not merely absent).

**Key metric: RBAC leakage rate = 0/N.** Any non-zero value is a hard failure.

## 4. Citation validation strategy

- **Integrity** (`test_citations_have_markers_and_snippets`): markers are 1..N,
  contiguous, each with a non-empty snippet and a reference string of the form
  `[n] Title (Department, location)`.
- **Attribution**: every citation resolves to a real `doc_id`/page from the manifest;
  snippets are slices of the indexed chunk text.
- **Answer↔citation consistency**: every `[n]` used in an answer exists in the
  citation list (guaranteed because the generator only emits markers for chunks it
  selected).

## 5. Enterprise scalability discussion

The reference deployment is intentionally laptop-scale (~20 sources, ~23 chunks). The
design scales along well-understood axes:

- **Index.** ChromaDB uses HNSW ANN — sub-linear query time into the millions of
  vectors. Beyond that, swap the `VectorStore` backend (e.g. pgvector, Qdrant, Milvus)
  behind the same interface; nothing else changes.
- **Ingestion.** Embarrassingly parallel per document; move to incremental/batched
  ingestion and a job queue. Re-index only changed documents (content-hash the
  manifest).
- **BM25.** The in-process index suits this corpus; at scale use an inverted-index
  service (e.g. OpenSearch) and fuse its scores in the same `HybridRetriever`.
- **RBAC.** The vector pre-filter keeps authorization cheap (metadata filter at query
  time). For very large policies, push ACLs into the store's filter and cache role →
  department maps.
- **Generation.** Extractive is O(retrieved chunks). Enabling the LLM backend adds one
  bounded, context-only call; cache by `(query, role, retrieved-set)`.
- **Cost & latency.** Dominated by embedding + ANN search; both are horizontally
  scalable and independent of corpus prose length once indexed.

## 6. Limitations (stated honestly)

- The synthetic corpus is small and self-authored; absolute retrieval numbers are
  illustrative, not benchmarked against a public dataset.
- Offline runs use a hashing embedder, which is weaker than a transformer; semantic
  recall improves materially with `all-MiniLM-L6-v2` weights available.
- Routing is keyword-based; it is transparent and auditable but will trail a learned
  classifier on ambiguous phrasing.
- Structured-source RBAC is document-level; column/row masking is future work.
