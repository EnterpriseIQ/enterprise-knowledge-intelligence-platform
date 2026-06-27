# Core Concepts

Understanding the terminology and core concepts used within EnterpriseIQ.

## 1. Document vs. Chunk
* **Document:** A complete file, such as a PDF, a JSON log file, or a SQL table dump.
* **Chunk:** A smaller, semantically meaningful piece of a Document (usually around 500 tokens). Vector search and RBAC operate on **Chunks**, not whole Documents.

## 2. Hybrid Retrieval
Relying solely on vector embeddings often fails on exact keyword matches (e.g., searching for a specific employee ID like `EMP-9921`). EnterpriseIQ uses **Hybrid Retrieval**:
* **Dense Vectors (SentenceTransformers):** Good for conceptual or semantic matches ("how do I request time off").
* **Sparse Index (BM25):** Good for exact keyword matching.
The system runs both searches and fuses the results using a normalisation algorithm.

## 3. Two-Layer RBAC
EnterpriseIQ implements a "Defense in Depth" strategy for Role-Based Access Control.
* **Pre-Filter (Vector DB Layer):** When querying ChromaDB, a `where` clause is applied so the database only returns chunks belonging to departments the user is allowed to see.
* **Post-Filter (Application Layer):** After retrieval, the application evaluates the `clearance` level (e.g., `public` vs `restricted`) and explicit `allowed_roles` on every single returned chunk before passing it to the generator.

## 4. Grounding and Citations
**Grounding** means the generated answer must be explicitly supported by the retrieved text. EnterpriseIQ enforces this by tracking the exact chunks used to construct the answer and appending numeric markers (e.g., `[1]`, `[2]`) that correspond to a detailed citation list.

## 5. Offline Extractive Mode
By default, EnterpriseIQ does not use an LLM to generate text. Instead, it uses an "Extractive" backend. It finds the most relevant chunks and stitches them together verbatim. This mathematically guarantees zero hallucination, as the system physically cannot invent new sentences.
