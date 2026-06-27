# Threat Model

The EnterpriseIQ threat model focuses on data leakage and hallucination risks.

## 1. Cross-Department Leakage
**Threat:** An HR user formulates a semantic query specifically designed to retrieve Finance documents.
**Mitigation:** The two-layer RBAC engine explicitly drops any chunk not belonging to `HR` from the generator's context window.

## 2. Prompt Injection (Jailbreaking)
**Threat:** A user submits a query containing instructions to ignore rules and output sensitive data.
**Mitigation:** In the default Extractive mode, prompt injection is impossible because there is no LLM to manipulate. If using the LLM mode, the strict RBAC post-filter ensures that even if the prompt is jailbroken, the LLM physically does not possess the forbidden chunks in its context window to leak them.

## 3. Timing Attacks
**Threat:** An attacker probes the `/query` endpoint to guess valid API keys based on response times.
**Mitigation:** `src/api/auth.py` uses `secrets.compare_digest` for constant-time string comparison.
