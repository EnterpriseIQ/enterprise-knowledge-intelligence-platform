# Request Lifecycle

Every request to `/query` goes through the following lifecycle within the `RAGPipeline`:

1. **Authentication:** The FastAPI middleware verifies the `X-API-Key` (if configured).
2. **Identity Resolution:** The provided `user_id` is mapped to a role, or the explicit `role` is validated against `access_policies.json`.
3. **Intent Routing:** The `AgenticRouter` analyses the query to determine the intent (`lookup`, `summarize`, etc.) and the primary target departments to boost during search.
4. **Retrieval (Pre-filter):** ChromaDB and BM25 are queried. The `where` clause in ChromaDB applies a pre-filter restricting results to the user's allowed departments.
5. **Hybrid Fusion:** Results from both stores are min-max normalised and combined.
6. **RBAC Enforcement (Post-filter):** Every single chunk in the fused list is passed through `RBAC.can_access_document`. Any chunk failing clearance or explicit ACL checks is dropped and logged.
7. **Context Assembly:** The remaining safe chunks are ordered by relevance.
8. **Generation:** The generator formulates an answer based *only* on the safe chunks.
9. **Citation Marking:** The system scans the generated answer to ensure every sentence is grounded in the provided chunks, appending citation markers.
10. **Audit Logging:** The query, the identity, the access decisions, and the latency are written to the audit log.
11. **Response:** A `QueryResponse` object is serialised and sent to the client.
