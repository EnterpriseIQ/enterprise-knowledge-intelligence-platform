# Security Recommendations

Before deploying to production, verify the following:

1. **Change the Default Data:** Do not run production using the output of `data.generate_data`. Provide your own real enterprise data.
2. **Review RBAC Policies:** Double-check `data/rbac/access_policies.json` to ensure the mapping of clearance levels and departments matches your organizational structure.
3. **Set API_KEY:** Never run the API on a public network without setting `API_KEY`.
4. **Use Extractive Mode:** If your compliance requirements forbid hallucinations entirely, leave `ERAG_LLM=0` (the default) to use the extractive generation backend.
5. **Network Isolation:** The vector database volume should only be accessible by the EnterpriseIQ container.
