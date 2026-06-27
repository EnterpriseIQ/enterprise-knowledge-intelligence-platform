"""API tests using FastAPI's TestClient (exercises startup/lifespan + endpoints)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app
from src.config import API_KEY


def test_health_and_query_flow():
    with TestClient(app) as client:
        headers = {"X-API-Key": API_KEY}
        h = client.get("/health")
        assert h.status_code == 200
        assert h.json()["status"] == "ok"
        assert h.json()["index"]["chunks"] > 0

        r = client.get("/roles", headers=headers)
        assert r.status_code == 200
        assert "HR" in r.json()["roles"]

        resp = client.post(
            "/query",
            json={"query": "What is the remote work policy?", "role": "HR"},
            headers=headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["citations"]
        assert body["citations"][0]["department"] == "HR"
        assert body["confidence"]["label"] in {"high", "medium", "low"}


def test_query_rbac_no_leak_via_api():
    with TestClient(app) as client:
        headers = {"X-API-Key": API_KEY}
        resp = client.post(
            "/query",
            json={"query": "Show finance budget allocations.", "role": "HR"},
            headers=headers,
        )
        assert resp.status_code == 200
        depts = {c["department"] for c in resp.json()["citations"]}
        assert "Finance" not in depts


def test_query_with_user_id():
    with TestClient(app) as client:
        headers = {"X-API-Key": API_KEY}
        resp = client.post(
            "/query",
            json={"query": "Show finance budget allocations.", "user_id": "fin_carol"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["role"] == "Finance"


def test_invalid_role_returns_400():
    with TestClient(app) as client:
        headers = {"X-API-Key": API_KEY}
        resp = client.post("/query", json={"query": "hello", "role": "Marketing"}, headers=headers)
        assert resp.status_code == 400


def test_audit_endpoint():
    with TestClient(app) as client:
        headers = {"X-API-Key": API_KEY}
        client.post("/query", json={"query": "leave policy", "role": "HR"}, headers=headers)
        resp = client.get("/audit?limit=5", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json()["entries"], list)


def test_unauthorized_endpoints():
    with TestClient(app) as client:
        # Test missing API key
        r = client.get("/roles")
        assert r.status_code == 401

        resp = client.post(
            "/query", json={"query": "What is the remote work policy?", "role": "HR"}
        )
        assert resp.status_code == 401

        resp = client.get("/audit?limit=5")
        assert resp.status_code == 401

        # Test invalid API key
        headers = {"X-API-Key": "invalid-key"}
        r = client.get("/roles", headers=headers)
        assert r.status_code == 401
