"""Integration test suite for Phase D.5 — Investigation Repository Explorer & Search Platform."""

import pytest
from fastapi.testclient import TestClient
from api.app import app
from storage.database import DatabaseManager
from storage.models import InvestigationRecord
from storage.repositories.search_repository import SearchRepository
from storage.sqlite.sqlite_repository import SQLiteRepository


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_tribunal_d5.db"
    db_mgr = DatabaseManager(db_file)
    repo = SQLiteRepository(db_manager=db_mgr, base_file_dir=tmp_path / "files")
    
    # Create sample investigations
    inv1 = InvestigationRecord(
        id="inv_d5_test_001",
        created_at="2026-07-26T10:00:00Z",
        query="Structuring anomaly for ACC_8000A94C0",
        dataset="default",
        planner_intent="Financial Structuring Analysis",
        risk_level="HIGH",
        confidence=0.85,
        recommendation="ESC_AML",
        status="COMPLETED",
        duration_ms=120.5,
        version="1.0.0",
    )
    inv2 = InvestigationRecord(
        id="inv_d5_test_002",
        created_at="2026-07-26T10:05:00Z",
        query="Velocity and dormancy check for ACC_9999",
        dataset="li_small",
        planner_intent="Velocity Analysis",
        risk_level="CRITICAL",
        confidence=0.92,
        recommendation="ESC_AML",
        status="COMPLETED",
        duration_ms=85.0,
        version="1.0.0",
    )
    repo.create(inv1)
    repo.create(inv2)
    return db_mgr


def test_search_repository_query(test_db):
    search_repo = SearchRepository(db_manager=test_db)
    items, total = search_repo.search(query="Structuring", risk_level="ALL")
    assert total >= 1
    assert any(i.id == "inv_d5_test_001" for i in items)


def test_search_repository_risk_filter(test_db):
    search_repo = SearchRepository(db_manager=test_db)
    items, total = search_repo.search(risk_level="CRITICAL")
    assert total == 1
    assert items[0].id == "inv_d5_test_002"


def test_search_repository_bookmark_and_tags(test_db):
    search_repo = SearchRepository(db_manager=test_db)
    
    # Toggle bookmark on
    is_bookmarked = search_repo.toggle_bookmark("inv_d5_test_001", notes="Target Account")
    assert is_bookmarked is True
    
    bookmarked = search_repo.get_bookmarked()
    assert len(bookmarked) == 1
    assert bookmarked[0].id == "inv_d5_test_001"
    
    # Add tag
    tag_ok = search_repo.add_tag("inv_d5_test_001", "Structuring")
    assert tag_ok is True
    
    # Check tags fetched in search
    items, _ = search_repo.search(only_bookmarked=True)
    assert "Structuring" in items[0].tags


def test_search_repository_similar_engine(test_db):
    search_repo = SearchRepository(db_manager=test_db)
    sim_items = search_repo.get_similar("inv_d5_test_001")
    assert isinstance(sim_items, list)


def test_search_rest_api_endpoints():
    client = TestClient(app)
    
    # Test GET /api/v1/search
    res = client.get("/api/v1/search")
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "results" in data
    
    # Test GET /api/v1/search/recent
    res_recent = client.get("/api/v1/search/recent")
    assert res_recent.status_code == 200
    assert isinstance(res_recent.json(), list)
    
    # Test GET /api/v1/search/export (CSV)
    res_csv = client.get("/api/v1/search/export?format=csv")
    assert res_csv.status_code == 200
    assert "ID,Created At,Query" in res_csv.text
    
    # Test GET /api/v1/search/export (JSON)
    res_json = client.get("/api/v1/search/export?format=json")
    assert res_json.status_code == 200
    assert isinstance(res_json.json(), list)
