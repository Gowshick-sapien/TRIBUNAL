"""Integration tests for DatasetResolver, GET /api/v1/datasets endpoint, and dataset early validation."""

import pytest
from fastapi.testclient import TestClient

from api.app import app
from tribunal.data.dataset_resolver import DatasetResolver, DatasetNotFoundError

client = TestClient(app)


def test_dataset_resolver_alias_resolution():
    """Test resolving registered alias IDs ('default', 'li_small', 'ibm_small')."""
    resolver = DatasetResolver()

    # 1. Resolve default alias
    res_default = resolver.resolve("default")
    assert res_default.resolved_path.exists()
    assert res_default.is_file is True
    assert "LI-Small_Trans.csv" in str(res_default.resolved_path)

    # 2. Resolve li_small alias
    res_li = resolver.resolve("li_small")
    assert res_li.resolved_path.exists()
    assert res_li.is_file is True

    # 3. Resolve direct CSV file path without appending /processed or /raw
    direct_csv_path = "tribunal/datasets/LI-Small_Trans.csv"
    res_direct = resolver.resolve(direct_csv_path)
    assert res_direct.resolved_path.exists()
    assert res_direct.is_file is True
    assert not str(res_direct.resolved_path).endswith("processed")


def test_dataset_resolver_nonexistent_raises_error():
    """Test that resolving a nonexistent dataset raises DatasetNotFoundError with searched locations."""
    resolver = DatasetResolver()
    with pytest.raises(DatasetNotFoundError) as exc_info:
        resolver.resolve("nonexistent_dataset_123.csv")

    err = exc_info.value
    assert err.dataset_ref == "nonexistent_dataset_123.csv"
    assert len(err.searched_locations) > 0
    assert "Expected a valid CSV/Parquet file path" in err.hint


def test_get_datasets_api_endpoint():
    """Test GET /api/v1/datasets metadata endpoint."""
    response = client.get("/api/v1/datasets")
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
    assert data["total"] >= 3

    dataset_ids = [d["id"] for d in data["datasets"]]
    assert "default" in dataset_ids
    assert "li_small" in dataset_ids
    assert "ibm_small" in dataset_ids


def test_investigate_early_dataset_validation():
    """Test that POST /api/v1/investigate fails early with 404 when given a bad dataset reference."""
    payload = {
        "query": "Check account ACC_8000A94C0 for structuring",
        "dataset": "nonexistent_dataset_456.csv",
    }
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "DatasetNotFound"
    assert "details" in data
    assert "searched_locations" in data["details"]
    assert "hint" in data["details"]
