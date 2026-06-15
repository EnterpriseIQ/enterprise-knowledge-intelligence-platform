# Lessons Learned

- **Provider Abstraction is Crucial:** The landscape of LLMs changes weekly. Tying an application directly to Anthropic's or OpenAI's SDK is a mistake.
- **Defence in Depth:** Applying RBAC at the pre-filter level (Chroma DB `where` clause) and post-retrieval ensures no leakage.
- **Evaluation Before Refactoring:** Establishing a test suite with explicit query relevance mappings (the tiny benchmark in `benchmarks/runner.py`) made it trivial to test changes to RRF and Reranking.
