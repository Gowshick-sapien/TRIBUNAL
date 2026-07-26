"""Integration test suite for Phase D.6 — Interactive Report & Export Platform."""

import pytest
from fastapi.testclient import TestClient
from api.app import app
from storage.database import DatabaseManager, DEFAULT_DB_PATH
from storage.models import InvestigationRecord
from storage.repositories.report_repository import ReportAnnotationRepository
from storage.sqlite.sqlite_repository import SQLiteRepository


@pytest.fixture
def sample_investigation(tmp_path):
    db_file = tmp_path / "test_tribunal_d6.db"
    db_mgr = DatabaseManager(db_file)
    repo = SQLiteRepository(db_manager=db_mgr, base_file_dir=tmp_path / "files")

    inv = InvestigationRecord(
        id="inv_d6_test_100",
        created_at="2026-07-26T11:00:00Z",
        query="Structuring anomaly for ACC_8000A94C0",
        dataset="default",
        planner_intent="Financial Structuring Analysis",
        risk_level="HIGH",
        confidence=0.85,
        recommendation="ESC_AML",
        status="COMPLETED",
        duration_ms=150.0,
        version="1.0.0",
    )
    repo.create(inv)

    # Create dummy report files
    rpt_file = tmp_path / "files" / "reports" / "inv_d6_test_100.md"
    rpt_file.write_text("# Executive Summary\nTarget exhibits structuring.", encoding="utf-8")

    json_file = tmp_path / "files" / "reports" / "inv_d6_test_100.json"
    json_file.write_text('{"investigation_id": "inv_d6_test_100", "summary": "Structuring"}', encoding="utf-8")

    return db_mgr


def test_report_annotations_repository(sample_investigation):
    repo = ReportAnnotationRepository(db_manager=sample_investigation)
    
    # Add note
    item = repo.add_annotation("inv_d6_test_100", "Compliance Lead", "Needs SAR review")
    assert item is not None
    assert item.author == "Compliance Lead"
    assert item.text == "Needs SAR review"

    # Fetch notes
    notes = repo.get_annotations("inv_d6_test_100")
    assert len(notes) == 1
    assert notes[0].text == "Needs SAR review"

    # Delete note
    deleted = repo.delete_annotation(item.id)
    assert deleted is True
    assert len(repo.get_annotations("inv_d6_test_100")) == 0


def test_reports_rest_api():
    # Insert test record into default DB for foreign key constraint
    db_mgr = DatabaseManager(DEFAULT_DB_PATH)
    repo = SQLiteRepository(db_manager=db_mgr)
    test_id = "inv_demo_d6_api"
    if not repo.exists(test_id):
        inv = InvestigationRecord(
            id=test_id,
            created_at="2026-07-26T11:00:00Z",
            query="Structuring check for ACC_8000A94C0",
            dataset="default",
            planner_intent="Financial Analysis",
            risk_level="HIGH",
            confidence=0.88,
            recommendation="ESC_AML",
            status="COMPLETED",
            duration_ms=120.0,
            version="1.0.0",
        )
        repo.create(inv)

    client = TestClient(app)

    # Test annotations endpoints
    res_add = client.post(
        f"/api/v1/reports/{test_id}/annotations",
        json={"author": "Compliance Officer", "text": "Escalated for SAR filing"},
    )
    assert res_add.status_code == 201
    data_add = res_add.json()
    assert data_add["text"] == "Escalated for SAR filing"

    note_id = data_add["id"]
    res_get = client.get(f"/api/v1/reports/{test_id}/annotations")
    assert res_get.status_code == 200
    assert len(res_get.json()) >= 1

    res_del = client.delete(f"/api/v1/reports/{test_id}/annotations/{note_id}")
    assert res_del.status_code == 200
    assert res_del.json()["success"] is True
