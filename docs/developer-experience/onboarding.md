# Developer Onboarding

Welcome to the EnterpriseIQ team! Here's how to get up to speed.

## Repository Layout
* `src/`: The core backend logic.
  * `api/`: FastAPI routes and Pydantic models.
  * `security/`: The all-important RBAC engine.
  * `retrieval/`: Where the vector and BM25 search fusion happens.
* `tests/`: Pytest suite.
* `docs/`: Markdown documentation (what you are reading now).
* `data/`: Ingestion sources and RBAC configs.
* `website/`: The React/Vite frontend.

## Local Setup
1. Clone the repo.
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -e ".[dev,llm]"`
4. Run tests: `python -m pytest`

## First Contribution
Look for issues labeled `good first issue`. A great way to start is by adding a new document parser in `src/ingestion/parsers.py` (e.g., adding support for Markdown or CSV files).
