# Examples

Here are some real-world examples of how to query the EnterpriseIQ platform.

## CLI: Investigating a Security Incident

```bash
python run_demo.py --role Security --query "Show me the logs for INC-9932"
```

Because of hybrid retrieval, the BM25 sparse index will perfectly match `INC-9932` even if the semantic vector is weak.

## API: Checking Finance Documents

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is the Q3 CapEx budget?",
       "role": "Finance"
     }'
```

The RBAC engine ensures that only documents tagged with the `Finance` department are retrieved.
