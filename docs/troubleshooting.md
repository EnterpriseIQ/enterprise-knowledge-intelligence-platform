# Troubleshooting Guide

### Issue: "Port already in use"
When starting the FastAPI server, you might see an error that port 8000 is in use.
**Solution:** Find the process using `lsof -i :8000` and kill it, or start uvicorn on a different port:
```bash
uvicorn src.api.main:app --port 8001
```

### Issue: Missing SQLite Database
If the system complains about a missing `operations.db`, you forgot to generate the synthetic data.
**Solution:** Run `python -m data.generate_data`

### Issue: Low Confidence Scores
If all queries return low confidence, your `HYBRID_ALPHA` might be tuned poorly for your data type.
**Solution:** Adjust `ERAG_HYBRID_ALPHA` in your environment variables. Try `0.3` for log-heavy data, or `0.8` for conceptual policy documents.
