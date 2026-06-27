# Security Policy

## Supported Versions

Currently, only the latest release of the EnterpriseIQ platform receives security updates. If you are running an older version, please upgrade to the latest stable release.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of EnterpriseIQ seriously, especially given its role in handling sensitive enterprise data.

If you discover a security vulnerability, please **DO NOT** open a public issue.

Instead, please email your findings to **security@enterpriseiq.example.com** (replace with actual security contact if deployed).

### What to Include

Please provide the following information in your report:

- Description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact (e.g., RBAC bypass, data leakage, remote code execution).
- Any suggested mitigations or patches.

### Response Timeline

- **Acknowledgement**: Within 24 hours.
- **Triage & Fix**: We aim to verify and patch critical vulnerabilities within 48 hours.
- **Disclosure**: After the patch is released and users have had time to update, we will publish a security advisory.

## Threat Model & Design

EnterpriseIQ is designed with a defense-in-depth approach. See [docs/security/threat-model.md](docs/security/threat-model.md) for a detailed overview of our security assumptions and architecture.
