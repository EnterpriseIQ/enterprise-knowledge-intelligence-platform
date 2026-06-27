# Glossary

* **Agentic Routing:** The process of analysing a user's query to determine their intent and the optimal search parameters before actually executing the search.
* **BM25:** Best Matching 25. A bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document.
* **ChromaDB:** The open-source vector database used to store and query the dense embeddings.
* **Dense Retrieval:** Searching based on semantic meaning using vector embeddings.
* **Extractive Generation:** Constructing an answer by pulling verbatim sentences from the source material, rather than having an LLM synthesize new text.
* **Hallucination:** When an AI generates factually incorrect information or information not present in the provided context.
* **Hybrid Alpha:** A float between 0 and 1 determining the weight given to Vector Search vs BM25 Search. 1.0 means pure vector search, 0.0 means pure BM25.
* **Min-Max Fusion:** A technique to combine scores from different retrieval systems (like Vector and BM25) by normalising their scores to a 0-1 range before combining them.
* **RAG (Retrieval-Augmented Generation):** An AI framework that retrieves facts from an external knowledge base to ground large language models on the most accurate, up-to-date information.
* **RBAC (Role-Based Access Control):** Restricting system access to authorized users based on their role within an organization.
* **Sparse Retrieval:** Keyword-based search.
