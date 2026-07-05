# Configuration

EnterpriseIQ adheres to the Twelve-Factor App methodology. All configuration is managed via environment variables.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `ERAG_API_KEY` | `dev-secret-key` | API Key for endpoint authentication. |
| `ERAG_DATA_DIR` | `./data` | Root directory for documents and indices. |
| `ERAG_CHUNK_SIZE` | `900` | Target chunk size in characters. |
| `ERAG_HYBRID_ALPHA` | `0.6` | Weight of vector vs. sparse search (0.0 to 1.0). |
| `ERAG_LLM` | `0` | Set to `1` to enable external LLM synthesis. |

## Adjusting `HYBRID_ALPHA`

- `HYBRID_ALPHA = 1.0` : Pure dense vector search. Good for conceptual questions.
- `HYBRID_ALPHA = 0.0` : Pure BM25 sparse search. Good for exact ID lookups.
- `HYBRID_ALPHA = 0.6` : Recommended default. Balances semantics with keyword anchoring.
