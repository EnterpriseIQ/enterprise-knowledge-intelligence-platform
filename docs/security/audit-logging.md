# Audit Logging

Every interaction with the RAG pipeline is recorded in the Audit Log, satisfying enterprise security requirements.

The log captures:
- Timestamp
- User ID and Assumed Role
- The raw query text
- The routed intent and targeted departments
- The total documents retrieved
- The count of documents allowed by RBAC
- The count of documents denied by RBAC
- Query Latency

You can query this log programmatically via the `/audit` endpoint to integrate with SIEM solutions (like Splunk or QRadar).
