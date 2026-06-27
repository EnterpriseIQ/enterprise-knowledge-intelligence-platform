# Advanced Examples

## Tuning Hybrid Retrieval

Sometimes a query requires more weight on exact keywords. You can tune this by passing `top_k` and modifying the `HYBRID_ALPHA` environment variable.

```bash
# In your terminal before starting the server:
export HYBRID_ALPHA=0.2  # Strongly favor BM25 sparse retrieval
uvicorn src.api.main:app
```

Now, querying for specific identifiers will be highly accurate:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "Details for incident INC-2025-021",
           "role": "Engineering",
           "top_k": 2
         }'
```

## Reviewing the Audit Log

If you want to build an internal dashboard, you can query the audit log:

```bash
curl "http://localhost:8000/audit?limit=5"
```
This returns the 5 most recent queries, showing the intent routing and how many documents were denied by the RBAC engine.
