# Secrets Management

EnterpriseIQ requires careful management of secrets to maintain security.

## Handled Secrets
1. **`API_KEY`**: The master key for accessing the platform API.
2. **`ANTHROPIC_API_KEY`**: (Optional) Required only if `ERAG_LLM=1`.

## Best Practices
- **Never hardcode secrets** in the source code or in `Dockerfile`.
- Always use a `.env` file for local development (ensure `.env` is in `.gitignore`).
- In production, inject secrets via your orchestrator (e.g., Kubernetes Secrets, AWS Secrets Manager, or Docker Swarm Secrets).
