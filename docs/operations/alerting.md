# Alerting Recommendations

Based on the exposed metrics, we recommend setting up the following alerts in your monitoring system (e.g., Prometheus Alertmanager or Datadog):

1. **High Error Rate Alert:** Trigger if `HTTP 5xx` responses exceed 1% over 5 minutes.
2. **High Latency Alert:** Trigger if the 95th percentile of `erag_query_latency_seconds` exceeds 2 seconds.
3. **RBAC Denial Spike:** Trigger if the ratio of denied documents to allowed documents spikes suddenly (indicates either a misconfigured policy or a user probing for access).
4. **Offline Mode Triggered:** Alert if `ERAG_LLM` is 1, but the system falls back to extractive mode due to API failures.
