# Enterprise Examples

## Integrating with Identity Providers

In an enterprise environment, you don't pass `role` as a plain string. You pass the user's ID, and the API resolves their role.

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secure_key" \
     -d '{
           "query": "Show Q4 budget.",
           "user_id": "fin_carol"
         }'
```
The API looks up `fin_carol` in `data/rbac/access_policies.json`, determines she is in the `Finance` role with `confidential` clearance, and executes the search accordingly.

## Cross-Department Compliance Audits
The `Admin` and `Compliance` roles have read access across departments to facilitate auditing.

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secure_key" \
     -d '{
           "query": "Summarize all outstanding critical incidents and budget shortfalls.",
           "role": "Compliance"
         }'
```
This single query retrieves data from both `Engineering` (incidents) and `Finance` (budget), ranking them together via the fused index.
