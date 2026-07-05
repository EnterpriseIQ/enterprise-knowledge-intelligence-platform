# EnterpriseIQ Documentation

Welcome to the official documentation for **EnterpriseIQ**, the production-grade Retrieval-Augmented Generation (RAG) platform designed explicitly for enterprise environments.

## Overview

EnterpriseIQ treats enterprise knowledge as a strictly governed asset. It fuses vector search with keyword anchoring, enforces multi-layered Role-Based Access Control (RBAC), and demands strict lexical grounding for every generated answer.

### Key Capabilities

- **Zero-Trust RBAC:** Data is filtered both during retrieval (Pre-Filter) and before generation (Post-Filter).
- **Hybrid Retrieval:** Min-Max fusion of Dense (Vector) and Sparse (BM25) search.
- **Offline Extractive Mode:** Guarantees zero hallucinations by only extracting verbatim snippets unless explicitly connected to an external LLM.

## Quick Links

- [Getting Started](getting-started.md)
- [Installation Guide](installation.md)
- [Architecture Deep Dive](architecture.md)
- [API Reference](api.md)

---
*If you find a bug or have a feature request, please open an issue on our [GitHub repository](https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform).*
