# Production LLM Examples

If you choose to move away from the Extractive backend and use a true Generative LLM (like Anthropic Claude), here is how to configure it.

1. Ensure the `[llm]` dependencies are installed (`pip install -e ".[llm]"`).
2. Set the environment variables:
   ```bash
   export ERAG_LLM=1
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```
3. Restart the API server.

Now, queries will use the `LLMBackend`. The security guarantees remain intact: the `LLMBackend` only receives chunks that have already passed the strict RBAC post-filter. The prompt instructs the LLM to only use the provided context and refuse if the answer is missing.
