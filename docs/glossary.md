# Glossary

- **BM25:** A bag-of-words retrieval function that estimates the relevance of documents to a given search query based on term frequencies. Used for "Sparse" retrieval in EnterpriseIQ.
- **ChromaDB:** The open-source embedding database used to store and query the dense vectors.
- **Chunk:** A semantic segment of a larger document. The fundamental unit of retrieval and access control.
- **Dense Retrieval:** Searching based on the semantic meaning of text, using vector embeddings.
- **Extractive Generation:** Constructing an answer by only copying verbatim text from the source documents, preventing hallucinations.
- **Hybrid Fusion:** Combining the results of Dense and Sparse retrieval. We use Min-Max normalization.
- **RBAC:** Role-Based Access Control.
- **Sparse Retrieval:** Searching based on exact keyword matches (BM25).
