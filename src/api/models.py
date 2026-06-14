"""Pydantic request/response models for the API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural-language question.", min_length=1)
    role: str | None = Field(
        None, description="Explicit role (Admin|HR|Finance|Engineering|Compliance).")
    user_id: str | None = Field(
        None, description="Known user id; its role is used if 'role' is omitted.")
    top_k: int | None = Field(None, ge=1, le=20, description="Number of sources to return.")

    model_config = {
        "json_schema_extra": {
            "examples": [{"query": "What is the remote work policy?", "role": "HR"}]
        }
    }


class Citation(BaseModel):
    marker: int
    reference: str
    doc_id: str | None = None
    title: str | None = None
    department: str | None = None
    source_type: str | None = None
    page: int | None = 0
    relevance: float | None = None
    snippet: str | None = None


class QueryResponse(BaseModel):
    query: str
    role: str
    answer: str
    confidence: dict
    citations: list[Citation]
    routing: dict
    source_coverage: dict
    access_summary: dict
