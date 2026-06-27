# Beginner Examples

These examples are designed to help you understand the basics of interacting with EnterpriseIQ.

## Asking a Simple Question via API
Using `curl` to ask a question as an HR employee.

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What are the core working hours?",
           "role": "HR"
         }'
```

## Reviewing the Output
The JSON response will contain:
- `answer`: The extracted text answering the question.
- `citations`: An array showing exactly which document and page the answer came from.
- `confidence`: Indicates if the system is confident in the answer based on lexical grounding.
