# Authorization

Authorization (RBAC) is the core security feature of EnterpriseIQ. It governs which documents a user's query is allowed to "see" and use for generation.

## Two-Layer Enforcement

1. **Pre-Filter (Database Level):**
   When the pipeline queries ChromaDB, it applies a `where` clause restricting the vector search to the user's allowed departments. This prevents the database from wasting time ranking forbidden documents.

2. **Post-Filter (Application Level):**
   Because vector database filtering isn't always reliable (and BM25 might not support it natively depending on the implementation), the application strictly evaluates every retrieved chunk in `src/security/rbac.py`.
   - **Department Check:** Does the chunk belong to an allowed department?
   - **Clearance Check:** Is the user's clearance level `>` or `=` the chunk's sensitivity?
   - **Explicit ACL:** If the chunk has an `allowed_roles` list, is the user's role in it?

Only chunks that pass **all** checks are passed to the generator.

## Role Configuration
Roles are defined in `data/rbac/access_policies.json`.
