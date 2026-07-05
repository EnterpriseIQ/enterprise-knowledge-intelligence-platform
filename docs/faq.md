# Frequently Asked Questions

### Why does the API return a 400 error sometimes?
If you request data outside of your configured role, the `RBACEngine` will reject the query entirely or return a grounded refusal indicating the data could not be found within your clearance.

### Does this require an OpenAI API Key?
**No.** By default, EnterpriseIQ runs 100% offline using `all-MiniLM-L6-v2` for embeddings and an internal extractive algorithm for generation. You only need an API key if you explicitly set `ERAG_LLM=1`.

### How do I update the RBAC rules?
Edit the `data/rbac/access_policies.json` file and restart the API server. In the future, this will be backed by a dynamic database.
