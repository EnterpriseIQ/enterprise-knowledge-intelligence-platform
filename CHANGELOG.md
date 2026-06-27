# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-20

### Added
- **Hybrid Retrieval Pipeline**: Min-max fusion of Dense Vector Search (SentenceTransformers) and Sparse Search (BM25).
- **Strict RBAC Enforcement**: Two-layer security model applied pre- and post-retrieval.
- **Offline Extractive Generation**: Default generation mode that operates entirely offline, guaranteeing zero hallucinations.
- **Grounded Citations**: Explicit mapping of generated text to source chunks, complete with page numbers and snippets.
- **Explainability**: Full routing rationale and access decision logs available per query.
- **FastAPI Backend**: Complete REST API with `/query`, `/health`, `/roles`, and `/audit` endpoints.
- **React Frontend**: Built with Vite, React 19, Tailwind CSS, and Framer Motion.
- **Docker Support**: Containerized deployment with health checks.
- **Comprehensive Documentation**: Added complete `docs/` folder covering architecture, APIs, operations, and security.

### Security
- Implemented API Key authentication for all endpoints.
- Validated that RBAC prevents cross-department data leakage.
