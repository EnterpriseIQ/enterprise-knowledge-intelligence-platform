# Logging

EnterpriseIQ logs are written to `stdout`/`stderr` using standard Python logging, making them compatible with log aggregators like ELK (Elasticsearch, Logstash, Kibana), Datadog, or CloudWatch.

## Log Levels
- `INFO`: Standard operational events (server startup, index warm-up).
- `WARNING`: Graceful degradation events (e.g., falling back to secondary embedder).
- `ERROR`: Failures in query execution or dependency crashes.
- `DEBUG`: Detailed retrieval scores and routing logic (useful for troubleshooting, but noisy).

## Audit Logging
In addition to standard system logs, the application maintains a business-level **Audit Log**. This log records the "who, what, and why" for every query, including specific documents allowed or denied by the RBAC engine. This is accessible via the `/audit` API endpoint.
