"""FastAPI application exposing the secure RAG platform.

Endpoints
---------
GET  /health        Liveness + active backends (embedding/vectorstore/bm25).
GET  /roles         RBAC roles, their scope and clearance.
POST /query         Ask a question as a given role; returns a grounded, cited answer.
GET  /audit         Recent audit-trail entries (explainability).

The pipeline is built once at startup so the model and index are warm.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import Counter, Histogram, make_asgi_app

from src.api.models import QueryRequest, QueryResponse
from src.pipeline import RAGPipeline

_state: dict = {}

# Prometheus metrics
QUERY_COUNT = Counter("erag_queries_total", "Total queries executed", ["role"])
QUERY_LATENCY = Histogram("erag_query_latency_seconds", "Query latency in seconds")


@asynccontextmanager
async def lifespan(app: FastAPI):
    def _setup():
        p = RAGPipeline()
        s = p.build_index()
        return p, s

    pipeline, stats = await asyncio.to_thread(_setup)
    _state["pipeline"] = pipeline
    _state["stats"] = stats
    yield
    _state.clear()


app = FastAPI(
    title="Secure Enterprise RAG Intelligence Platform",
    description="Context-aware Retrieval-Augmented Generation across heterogeneous "
    "enterprise sources with strict RBAC, grounded citations and "
    "confidence scoring.",
    version="1.0.0",
    lifespan=lifespan,
)

# Add prometheus asgi middleware to route /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Instrument the FastAPI app with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)


def _pipeline() -> RAGPipeline:
    pipeline = _state.get("pipeline")
    if pipeline is None:  # pragma: no cover - lifespan guarantees this
        pipeline = RAGPipeline()
        _state["pipeline"] = pipeline
        _state["stats"] = pipeline.build_index()
    return pipeline


@app.get("/health")
def health():
    _pipeline()  # ensure the index/model are warm
    return {"status": "ok", "version": app.version, "index": _state.get("stats", {})}


@app.get("/roles")
def roles():
    rbac = _pipeline().rbac
    return {
        "roles": {
            name: {
                "departments": cfg["departments"],
                "clearance": cfg["clearance"],
                "description": cfg.get("description", ""),
            }
            for name, cfg in rbac.roles.items()
        },
        "users": rbac.users,
    }


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    pipeline = _pipeline()
    role_label = req.role or "anonymous"
    QUERY_COUNT.labels(role=role_label).inc()

    with QUERY_LATENCY.time():
        try:
            result = pipeline.agentic_query(
                req.query, role=req.role, user_id=req.user_id or "", top_k=req.top_k
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.to_dict()


@app.get("/audit")
def audit(limit: int = 20):
    return {"entries": _pipeline().audit.tail(limit)}
