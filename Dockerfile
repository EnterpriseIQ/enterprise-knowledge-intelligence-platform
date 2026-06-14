# syntax=docker/dockerfile:1

# ----------------------------------------------------------------------------- #
# Secure Enterprise RAG Intelligence Platform — container image
#
# Single-stage, slim image. Dependencies are installed first (cached layer), then
# the synthetic corpus is generated at build time so the container starts with a
# ready-to-index dataset. The app builds its vector index on startup (FastAPI
# lifespan) and runs fully offline — no API keys required.
# ----------------------------------------------------------------------------- #
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    # Persisted Chroma index location inside the container
    ERAG_VECTORSTORE_DIR=/app/data/vectorstore \
    # Allow SentenceTransformers/HF to work offline; the platform falls back to a
    # deterministic hashing embedder when weights are unavailable.
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1

WORKDIR /app

# System deps kept minimal; build tools only where wheels may be missing.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching.
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source and data generator.
COPY . .

# Generate the synthetic enterprise corpus at build time (deterministic).
RUN python -m data.generate_data

# Run as a non-root user (least privilege).
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Container healthcheck hits the app's /health endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
