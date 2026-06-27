# Rate Limiting

EnterpriseIQ does not currently implement rate limiting at the application layer.

**Recommendation:** If exposing the API publicly, you must implement rate limiting at your API Gateway, Load Balancer, or Ingress Controller to prevent Denial of Service (DoS) attacks or excessive LLM API costs.
