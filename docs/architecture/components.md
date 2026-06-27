# Component Architecture

The EnterpriseIQ backend is modularised into several distinct sub-packages, each with a single responsibility.

## `src/api`
Handles the REST interface, data validation using Pydantic, and authentication.
- `main.py`: Application entry point and lifespan management.
- `auth.py`: API Key header validation.
- `models.py`: Pydantic request/response schemas.

## `src/security`
The brain of the zero-trust architecture.
- `rbac.py`: Loads `access_policies.json` and evaluates (Department ∩ Clearance ∩ ACL) rules for every single document chunk before it is passed to the generation tier.

## `src/retrieval`
Handles the complex search logic.
- `hybrid.py`: Executes the query against both the vector store and the BM25 index, normalises the scores, and fuses them based on `HYBRID_ALPHA`.

## `src/generation`
Translates retrieved context into final answers.
- `extractive.py`: The default, offline backend that stitches chunks together directly.
- `llm.py`: An abstraction layer that packages the prompt and context for external/local LLM inference (e.g., Anthropic).
- `citations.py`: Maps the final text back to the specific chunk indices to append the `[1]` style markers.

## `src/ingestion`
Normalises diverse inputs.
- Parses PDFs, SQL rows, and structured JSON into unified `Document` objects.

## `src/vectorstore`
- `chroma.py`: Wrapper around ChromaDB, handling the graceful fallback if native components fail.
