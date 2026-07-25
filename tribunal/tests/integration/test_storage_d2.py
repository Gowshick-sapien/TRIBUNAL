"""Integration test suite for Phase D.2 Persistent Investigation Repository."""

import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.dependencies import get_investigation_service
from api.schemas.investigation import InvestigationRequest
from api.services.investigation_service import InvestigationService
from storage.database import DatabaseManager
from storage.models import InvestigationRecord, VerdictRecord
from storage.sqlite.sqlite_repository import SQLiteRepository


@pytest.fixture
def temp_storage():
    """Fixture initializing isolated SQLite DB and file storage directories in a temp folder."""
    kwargs = {"ignore_cleanup_errors": True} if sys.version_info >= (3, 10) else {}
    with tempfile.TemporaryDirectory(**kwargs) as tmp_dir:
        tmp_path = Path(tmp_dir)
        db_path = tmp_path / "test_tribunal.db"
        db_manager = DatabaseManager(db_path)
        file_dir = tmp_path / "files"
        repo = SQLiteRepository(db_manager=db_manager, base_file_dir=file_dir)
        yield repo


@pytest.fixture
def service_with_temp_storage(temp_storage):
    """Fixture providing InvestigationService connected to isolated temp storage."""
    svc = InvestigationService(repository=temp_storage)
    return svc


@pytest.fixture
def client_with_storage(service_with_temp_storage):
    """FastAPI TestClient with overridden get_investigation_service dependency."""
    app.dependency_overrides[get_investigation_service] = lambda: service_with_temp_storage
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_sqlite_repository_basic_crud(temp_storage: SQLiteRepository):
    """Test basic CRUD operations on SQLiteRepository."""
    inv_id = "inv_test_crud_001"
    rec = InvestigationRecord(
        id=inv_id,
        query="Test query for structuring",
        dataset="default",
        risk_level="HIGH",
        confidence=0.9,
    )

    # 1. Create
    temp_storage.create(rec)
    assert temp_storage.exists(inv_id) is True

    # 2. Get
    fetched = temp_storage.get(inv_id)
    assert fetched is not None
    assert fetched.id == inv_id
    assert fetched.query == "Test query for structuring"
    assert fetched.confidence == 0.9

    # 3. List
    records = temp_storage.list(limit=10)
    assert len(records) >= 1
    assert records[0].id == inv_id

    # 4. Delete
    deleted = temp_storage.delete(inv_id)
    assert deleted is True
    assert temp_storage.exists(inv_id) is False


def test_atomic_full_investigation_save(temp_storage: SQLiteRepository):
    """Test save_full_investigation atomic multi-artifact persistence."""
    inv_id = "inv_atomic_001"
    rec = InvestigationRecord(
        id=inv_id,
        query="Check account ACC_100 for money laundering",
        dataset="default",
        risk_level="CRITICAL",
        confidence=0.95,
    )

    md_report = "# Report for inv_atomic_001\nFull markdown text..."
    json_report = {"summary": "Critical AML risk"}
    graph_dict = {"nodes": [{"id": "ACC_100", "label": "Account 100", "node_type": "account"}], "edges": []}
    verdict_rec = VerdictRecord(
        investigation_id=inv_id,
        winning_hypothesis="Structuring Activity",
        confidence=0.95,
        recommendation="Escalate to Compliance",
    )

    temp_storage.save_full_investigation(
        record=rec,
        markdown_report=md_report,
        json_report=json_report,
        graph_dict=graph_dict,
        verdict_record=verdict_rec,
        case_file_dict={"case_id": inv_id},
    )

    assert temp_storage.exists(inv_id) is True
    loaded_report = temp_storage.load_report(inv_id)
    assert loaded_report is not None
    assert "# Report for inv_atomic_001" in loaded_report["markdown_content"]

    loaded_graph = temp_storage.load_graph(inv_id)
    assert loaded_graph is not None
    assert len(loaded_graph["nodes"]) == 1

    loaded_verdict = temp_storage.load_verdict(inv_id)
    assert loaded_verdict is not None
    assert loaded_verdict.winning_hypothesis == "Structuring Activity"


def test_persistence_survival_across_service_restarts(temp_storage: SQLiteRepository):
    """Verify that persisted investigations survive when a brand new InvestigationService instance is constructed."""
    svc_1 = InvestigationService(repository=temp_storage)

    req = InvestigationRequest(query="Test account ACC_8000A94C0 for structuring", dataset="default")
    res = svc_1.run_investigation(req)
    inv_id = res.investigation_id

    # Instantiate brand NEW InvestigationService using same repository (simulating server restart)
    svc_2 = InvestigationService(repository=temp_storage)

    # 1. Fetch Report
    report_res = svc_2.get_report(inv_id)
    assert report_res.investigation_id == inv_id
    assert len(report_res.sections) == 10

    # 2. Fetch Graph
    graph_res = svc_2.get_graph(inv_id)
    assert graph_res.investigation_id == inv_id

    # 3. Fetch Verdict
    verdict_res = svc_2.get_verdict(inv_id)
    assert verdict_res.investigation_id == inv_id

    # 4. Audit History
    audit_history = temp_storage.history(inv_id)
    events = [a.event for a in audit_history]
    assert "PERSISTED" in events
    assert "RETRIEVED" in events


def test_extended_rest_endpoints_d2(client_with_storage: TestClient, service_with_temp_storage: InvestigationService):
    """Test D.2 REST API endpoints: GET /investigations, GET /investigation/{id}, DELETE /investigation/{id}."""
    # 1. Create an investigation via API
    payload = {"query": "Check account ACC_8000A94C0 for anomalies", "dataset": "default"}
    inv_res = client_with_storage.post("/api/v1/investigate", json=payload)
    assert inv_res.status_code == 200
    inv_id = inv_res.json()["investigation_id"]

    # 2. List investigations (GET /api/v1/investigations)
    list_res = client_with_storage.get("/api/v1/investigations")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1
    assert any(item["id"] == inv_id for item in list_data["investigations"])

    # 3. Get investigation detail (GET /api/v1/investigation/{id})
    detail_res = client_with_storage.get(f"/api/v1/investigation/{inv_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["record"]["id"] == inv_id
    assert f"/api/v1/report/{inv_id}" in detail_data["report_url"]

    # 4. Delete investigation (DELETE /api/v1/investigation/{id})
    del_res = client_with_storage.delete(f"/api/v1/investigation/{inv_id}")
    assert del_res.status_code == 204

    # 5. Confirm 404 after deletion
    detail_res_2 = client_with_storage.get(f"/api/v1/investigation/{inv_id}")
    assert detail_res_2.status_code == 404
