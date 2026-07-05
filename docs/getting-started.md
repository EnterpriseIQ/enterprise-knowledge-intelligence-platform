# Getting Started with EnterpriseIQ

This guide will walk you through spinning up EnterpriseIQ and making your first secure query.

## 1. Prerequisites

- Python 3.10+
- Git

## 2. Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform.git
cd enterprise-knowledge-intelligence-platform
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,llm]"
```

## 3. Generate Data

EnterpriseIQ requires a corpus to query. We provide a synthetic data generator to create mock HR, Finance, and IT documents.

```bash
python -m data.generate_data
```

## 4. Run the API

Start the FastAPI backend:

```bash
uvicorn src.api.main:app --reload
```

## 5. Your First Query

With the API running, use `curl` to query the system as an HR representative:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the remote work policy?", "role": "HR"}'
```

You should receive a JSON response containing the grounded answer, citations, and routing rationale.

## Next Steps

- Explore the [Architecture](architecture.md) to understand how the pipeline works.
- See the [Configuration](configuration.md) guide to tune the hybrid retrieval.
