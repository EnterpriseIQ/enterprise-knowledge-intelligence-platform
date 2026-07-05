# Security Policy

Security is foundational to EnterpriseIQ. Our primary mandate is to prevent data leakage and hallucinations within enterprise environments.

## Supported Versions

Currently, only the latest `main` branch is receiving active security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please DO NOT report it through public issues or discussions.

Instead, please email the security team at **security@enterpriseiq.io**.

We will acknowledge your email within 48 hours and provide a timeline for triaging and resolving the issue.

### What to Include
Please provide as much information as possible:
- A description of the vulnerability.
- Steps to reproduce.
- Any relevant logs (scrubbed of actual confidential data).
- Potential impact (e.g., cross-department data leakage, RBAC bypass).

## Threat Model

EnterpriseIQ assumes a hostile internal environment (Zero-Trust). We expect users to actively try to prompt-inject or bypass RBAC to access other departments' data.

Our threat model explicitly covers:
1.  **RBAC Bypass:** Attempting to retrieve chunks outside of the user's explicit ACL or department.
2.  **Prompt Injection (Jailbreaking):** Attempting to force the LLM to output restricted data.
3.  **Data Poisoning:** Attempting to ingest malicious documents to corrupt the index.

We rely on explicit, code-level pre-filters (during vector retrieval) and post-filters (before context assembly) to mitigate these threats, rather than relying on LLM behavior.

## Secure Coding Guidelines

When contributing to EnterpriseIQ, please adhere to the following:
- **Never hardcode secrets.** Use environment variables or secure token generators (`secrets.token_hex`).
- **Validate all inputs strictly** using Pydantic.
- **Prevent timing attacks** by always using `secrets.compare_digest` with an explicit `None` check for secret string comparisons.
- **Ensure error messages do not leak internal state or stack traces.** Use standard HTTP exception responses.
