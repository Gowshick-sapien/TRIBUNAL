"""Integration tests for Phase D.1 Investigation Service Layer & REST API."""

import pytest
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture
def client():
    """Test client fixture for FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client: TestClient):
    """Test root discovery endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TRIBUNAL Investigation Engine REST API"
    assert data["version"] == "1.0.0"
    assert data["documentation"] == "/docs"


def test_health_endpoint(client: TestClient):
    """Test /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert data["api_version"] == "v1"
    assert data["planner_ready"] is True
    assert data["engine_ready"] is True
    assert "uptime_seconds" in data
    assert "X-Response-Time-Ms" in response.headers


def test_metadata_endpoint(client: TestClient):
    """Test /api/v1/metadata endpoint."""
    response = client.get("/api/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["api_version"] == "v1"
    assert "financial" in data["supported_experts"]
    assert "behaviour" in data["supported_experts"]
    assert "structuring" in data["supported_aml_patterns"]


def test_investigate_and_artifacts_flow(client: TestClient):
    """Test full investigation endpoint and retrieval of report, graph, and verdict artifacts."""
    payload = {
        "query": "Is customer ACC_8000A94C0 engaged in structuring and velocity anomalies?",
        "dataset": "default",
        "options": {
            "confidence_threshold": 0.6,
            "max_depth": 3,
            "include_graph": True,
        },
    }

    # 1. Trigger Investigation
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 200
    res_data = response.json()

    assert "investigation_id" in res_data
    inv_id = res_data["investigation_id"]
    assert inv_id.startswith("inv_")
    assert res_data["verdict"] in ("LIKELY_MALICIOUS", "POSSIBLY_MALICIOUS", "LIKELY_LEGITIMATE", "INCONCLUSIVE")
    assert 0.0 <= res_data["confidence"] <= 1.0
    assert "summary" in res_data
    assert "report_url" in res_data
    assert "graph_url" in res_data
    assert "verdict_url" in res_data
    assert "planner_ms" in res_data["metrics"]
    assert "total_ms" in res_data["metrics"]

    # 2. Fetch Report (JSON)
    report_res = client.get(f"/api/v1/report/{inv_id}")
    assert report_res.status_code == 200
    report_data = report_res.json()
    assert report_data["investigation_id"] == inv_id
    assert len(report_data["sections"]) == 10
    assert "markdown_content" in report_data

    # 3. Fetch Report (Markdown header)
    md_res = client.get(f"/api/v1/report/{inv_id}", headers={"Accept": "text/markdown"})
    assert md_res.status_code == 200
    assert "text/markdown" in md_res.headers["content-type"]
    assert len(md_res.text) > 0

    # 4. Fetch Evidence Graph
    graph_res = client.get(f"/api/v1/graph/{inv_id}")
    assert graph_res.status_code == 200
    graph_data = graph_res.json()
    assert graph_data["investigation_id"] == inv_id
    assert isinstance(graph_data["nodes"], list)
    assert isinstance(graph_data["edges"], list)
    assert "statistics" in graph_data

    # 5. Fetch Tribunal Verdict
    verdict_res = client.get(f"/api/v1/verdict/{inv_id}")
    assert verdict_res.status_code == 200
    verdict_data = verdict_res.json()
    assert verdict_data["investigation_id"] == inv_id
    assert verdict_data["verdict"] in ("LIKELY_MALICIOUS", "POSSIBLY_MALICIOUS", "LIKELY_LEGITIMATE", "INCONCLUSIVE")
    assert "winning_hypothesis" in verdict_data
    assert isinstance(verdict_data["deliberation_trace"], list)


def test_conversational_query_endpoint(client: TestClient):
    """Test lightweight conversational /query endpoint."""
    payload = {
        "query": "Is customer 541 suspicious?",
        "dataset": "default",
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Is customer 541 suspicious?"
    assert "verdict" in data
    assert "short_answer" in data
    assert "financial" in data["invoked_experts"]


def test_invalid_query_validation(client: TestClient):
    """Test 400 response for invalid short query."""
    payload = {"query": "a", "dataset": "default"}
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 400
    error_data = response.json()
    assert error_data["error"] == "InvalidQuery"
    assert "at least 3 characters" in error_data["message"]


def test_nonexistent_dataset(client: TestClient):
    """Test 404 response for nonexistent dataset reference."""
    payload = {"query": "Investigate suspicious transfer", "dataset": "nonexistent_dataset_ref_123"}
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "DatasetNotFound"


def test_nonexistent_investigation_artifact(client: TestClient):
    """Test 404 response when requesting nonexistent investigation ID."""
    response = client.get("/api/v1/report/inv_nonexistent_999")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "InvestigationNotFound"


def test_openapi_schema(client: TestClient):
    """Test OpenAPI spec generation."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    paths = schema["paths"]
    assert "/api/v1/investigate" in paths
    assert "/api/v1/query" in paths
    assert "/api/v1/report/{id}" in paths
    assert "/api/v1/graph/{id}" in paths
    assert "/api/v1/verdict/{id}" in paths
    assert "/api/v1/health" in paths
    assert "/api/v1/metadata" in paths
