# Runbook

Operational quick-reference for running, configuring and troubleshooting the
platform.

## Quick start

```bash
pip install -r requirements.txt
python -m data.generate_data      # generate corpus
python run_demo.py                # end-to-end demo + RBAC proof
uvicorn src.api.main:app --reload # API at http://localhost:8000 (docs at /docs)
pytest -q                         # 28 tests
```

### Via Make / Docker

```bash
make install          # deps (runtime + dev, editable install)
make demo             # corpus + end-to-end demo
make run              # API on :8000
make test             # test suite
make docker-build     # build container image
make docker-run       # run container (maps :8000, has HEALTHCHECK)
```

CI (`.github/workflows/ci.yml`) runs lint + tests on Python 3.10/3.11/3.12 and builds +
health-checks the Docker image on every push. Configuration is loaded from `.env`
(copy from `.env.example`) or real environment variables.

## Configuration (environment variables)

All defaults live in `src/config.py` and can be overridden:

| Variable | Default | Meaning |
|---|---|---|
| `ERAG_CHUNK_SIZE` / `ERAG_CHUNK_OVERLAP` | 900 / 150 | Chunk window (chars). |
| `ERAG_EMBEDDING_MODEL` | all-MiniLM-L6-v2 | SentenceTransformers model. |
| `ERAG_TOP_K` / `ERAG_CANDIDATE_K` | 5 / 20 | Returned vs. candidate pool size. |
| `ERAG_HYBRID_ALPHA` | 0.6 | Dense weight in fusion (1.0 = dense only). |
| `ERAG_CONF_HIGH` / `ERAG_CONF_LOW` | 0.55 / 0.30 | Confidence bucket thresholds. |
| `ERAG_LLM` | unset | `1` enables the optional LLM generator backend. |
| `ERAG_VECTORSTORE_DIR` | data/vectorstore | Chroma persistence path. |

## Backends & fallbacks

`GET /health` reports the active `embedding_backend`, `vectorstore_backend` and
`bm25_backend`.

- **Embeddings:** `sentence-transformers:*` if weights load, else `hashing-fallback`.
- **Vector store:** `chromadb` if importable, else in-memory `memory` store.
- **BM25:** `rank-bm25` if installed, else `builtin-bm25` (pure Python).

The platform runs fully offline on the fallbacks; no API keys are required.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Manifest not found` | Run `python -m data.generate_data` first. |
| `embedding_backend = hashing-fallback` | HuggingFace weights unreachable (offline). Expected; retrieval still works. Pre-download the model to enable transformer embeddings. |
| PDFs generated as `.txt` | `reportlab` not installed; `pip install reportlab` then regenerate. |
| `Unknown role` (HTTP 400) | Use one of `Admin/HR/Finance/Engineering/Compliance` or a known `user_id`. |
| Port already in use | `uvicorn ... --port 8081`. |
