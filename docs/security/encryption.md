# Encryption

## Data in Transit
EnterpriseIQ does not handle TLS termination natively. You **must** deploy it behind a reverse proxy (like Nginx, Traefik, or an AWS Load Balancer) that provides HTTPS/TLS encryption to protect API keys and query data in transit.

## Data at Rest
The ChromaDB index and BM25 index are stored on disk (usually in `/app/data`). Ensure that the underlying storage volume (e.g., EBS volume, SAN, or local disk) has Data-at-Rest encryption enabled (like AES-256) at the infrastructure level.
