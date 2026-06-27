# Metrics

Metrics are exposed via the `/metrics` endpoint in Prometheus format.

## Available Metrics

| Metric Name | Type | Description |
| :--- | :--- | :--- |
| `erag_queries_total` | Counter | Total number of queries executed, labeled by `role`. |
| `erag_query_latency_seconds` | Histogram | Distribution of query latency. |
| `fastapi_requests_total` | Counter | Total HTTP requests (via OpenTelemetry). |

## Prometheus Integration
You can point your Prometheus scraper directly at the `/metrics` endpoint of the FastAPI server. A sample `prometheus.yml` is provided in the repository root.
