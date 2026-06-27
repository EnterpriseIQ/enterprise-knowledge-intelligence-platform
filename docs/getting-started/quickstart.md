# Quickstart Guide

Get EnterpriseIQ up and running in under 5 minutes.

## 1. Generate the Dataset
Before you can query anything, you need data. EnterpriseIQ ships with a synthetic data generator that creates a corpus of realistic enterprise documents, logs, and SQL records.

```bash
python -m data.generate_data
```
*This will populate the `data/` directory with sample files and generate the ChromaDB index.*

## 2. Run the Demo
The demo script runs a series of predefined queries to prove that the system is working and that RBAC rules are successfully blocking cross-department data leakage.

```bash
python run_demo.py
```
*Look for `RBAC enforcement: ALL SCENARIOS PASS` at the end of the output.*

## 3. Start the API Server
Launch the FastAPI application to interact with the system via HTTP.

```bash
uvicorn src.api.main:app --reload
```

## 4. Make Your First API Call
Open a new terminal window and send a curl request. We'll ask a question as a user in the **Finance** role.

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Show me the Q4 budget allocations", "role": "Finance"}'
```

You should receive a JSON response containing the answer and specific citations pointing to the generated Finance documents.
