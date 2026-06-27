# Frequently Asked Questions (FAQ)

### Q: Does EnterpriseIQ require an OpenAI API key?
**A:** No. By default, EnterpriseIQ runs 100% offline using local embedding models (`all-MiniLM-L6-v2`) and an Extractive generation backend. If you *want* to use an LLM for more conversational answers, you can enable it via the `ERAG_LLM=1` environment variable.

### Q: Can I use this with my existing Active Directory / SSO?
**A:** Currently, RBAC mapping is handled via `data/rbac/access_policies.json`. However, the architecture is designed so you can easily replace the identity resolution step in `src/api/main.py` with an OAuth2/OIDC middleware that reads claims from a JWT token.

### Q: Why do I get an explicit refusal sometimes?
**A:** If you ask a question that is completely outside the scope of the ingested documents (e.g., "What is the capital of France?"), the confidence scorer will detect low lexical overlap and explicitly refuse to answer. This is a core safety feature to prevent hallucinations.

### Q: How do I scale ChromaDB for production?
**A:** For production deployments exceeding ~100k chunks, we recommend running ChromaDB in Client/Server mode on a dedicated instance, rather than the embedded mode used by default.

### Q: Is the frontend included?
**A:** Yes, there is a React/Vite frontend located in the `website/` directory. You can build it using `pnpm build`.
