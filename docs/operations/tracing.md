# Tracing

EnterpriseIQ is instrumented with **OpenTelemetry** for distributed tracing.

## Setup
By default, the `FastAPIInstrumentor` is applied in `src/api/main.py`.

To export traces to a backend like Jaeger, Zipkin, or Honeycomb, you must configure the standard OpenTelemetry environment variables:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://your-collector:4317"
export OTEL_SERVICE_NAME="enterprise-rag-api"
```

Traces will capture the duration of the HTTP request, and you can extend spans into the retrieval pipeline to identify bottlenecks between vector search and BM25 processing.
