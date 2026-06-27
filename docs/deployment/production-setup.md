# Production Setup

When moving from local evaluation to a production environment, several configurations should be hardened.

## 1. Authentication
In production, you **must** set the `API_KEY` environment variable.
```bash
export API_KEY="your_secure_random_string"
```
This forces all endpoints (except `/health`) to require the `X-API-Key` header.

## 2. Docker Deployment
Use the provided `Dockerfile`. It is optimized for production:
- It runs as a non-root user (`appuser`).
- It includes a `HEALTHCHECK` directive.
- It copies the pre-generated index to avoid building it at runtime.

### Building the Image
```bash
docker build -t enterpriseiq:latest .
```

### Running the Image
```bash
docker run -d \
  --name enterpriseiq \
  -p 8000:8000 \
  -e API_KEY="your_secure_random_string" \
  -v /path/to/host/data:/app/data \
  enterpriseiq:latest
```

*Note: Mounting the `/app/data` volume is crucial if you are ingesting new documents at runtime, so the vector database persists across container restarts.*

## 3. Reverse Proxy / TLS
The FastAPI application runs on HTTP. In production, you should place it behind a reverse proxy (like Nginx, Traefik, or an AWS Application Load Balancer) that handles TLS termination (HTTPS).

## 4. Environment Variables
Ensure the following are set appropriately:
- `LOG_LEVEL`: Set to `INFO` or `WARNING` to reduce noise.
- `ERAG_LLM`: If using an external LLM, ensure `ANTHROPIC_API_KEY` is securely injected (e.g., via Kubernetes Secrets).
