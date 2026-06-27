# Troubleshooting

Common issues and their resolutions.

### 1. Vector DB Fallback Warning
**Symptom:** Logs show `Falling back to hashing embedder`.
**Cause:** SentenceTransformers failed to load, usually due to lack of internet access during the first run (it tries to download weights from HuggingFace).
**Resolution:** Ensure the machine has internet access on the first run, or pre-download the weights and mount them into the container.

### 2. Missing Answers / Refusals
**Symptom:** The API returns "I cannot answer this based on the provided context."
**Cause:** The confidence score was too low.
**Resolution:** Check the `/audit` log. If the relevant documents were denied by RBAC, the user doesn't have clearance. If they weren't retrieved at all, consider tuning the `HYBRID_ALPHA` or checking if the documents were ingested properly.

### 3. Port Already in Use
**Symptom:** Uvicorn fails to start with `[Errno 98] Address already in use`.
**Resolution:** Kill the process using port 8000: `kill -9 $(lsof -t -i:8000)`.
