# Monitoring

EnterpriseIQ is instrumented for comprehensive monitoring to ensure reliability and performance in production.

We expose metrics, logs, and traces using standard protocols.

## Key Areas to Monitor
1. **Query Latency:** The time taken from receiving the `/query` request to returning the generated answer.
2. **Access Denials:** Spikes in denied access logs may indicate misconfigured roles or a potential internal threat.
3. **Retrieval Health:** Monitor if the system is falling back to the backup hashing embedder, which indicates SentenceTransformers has failed.
