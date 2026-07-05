# Installation Guide

EnterpriseIQ can be installed either via standard Python tools or deployed via Docker for production environments.

## Local Installation (Development)

Requires **Python 3.10+**.

```bash
git clone https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform.git
cd enterprise-knowledge-intelligence-platform

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e "."
```

### Optional Dependencies
If you wish to use external LLMs (like Anthropic) instead of the default offline extractive mode, install with the `llm` extra:
```bash
pip install -e ".[llm]"
```

## Docker Installation (Production)

We strongly recommend Docker for production deployments to ensure environment consistency.

```bash
# Build the image
make docker-build

# Run the container
make docker-run
```

The Docker image is built to run as a non-root user and includes a `HEALTHCHECK`. It is compatible with Kubernetes, ECS, and Docker Swarm. See the [Deployment Guide](deployment.md) for more details.
