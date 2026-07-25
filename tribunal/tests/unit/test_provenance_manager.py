"""Unit tests for ProvenanceManager."""

import pytest
from tribunal.investigation.evidence.provenance_manager import ProvenanceManager


def test_provenance_manager_validation():
    pm = ProvenanceManager()
    assert pm.validate_provenance({"transaction_ids": ["TX1"]}) is True
    assert pm.validate_provenance({"detectors": ["StructuringDetector"]}) is True
    assert pm.validate_provenance({"feature_store_rows": [0, 1]}) is True
    assert pm.validate_provenance({}) is False
    assert pm.validate_provenance(None) is False


def test_provenance_manager_merge():
    pm = ProvenanceManager()
    p1 = {"detectors": ["DetectorA"], "transaction_ids": ["TX1"], "feature_store_rows": [0]}
    p2 = {"detectors": ["DetectorB"], "transaction_ids": ["TX1", "TX2"], "feature_store_rows": [1]}

    merged = pm.merge_provenance(p1, p2)
    assert set(merged["detectors"]) == {"DetectorA", "DetectorB"}
    assert set(merged["transaction_ids"]) == {"TX1", "TX2"}
    assert set(merged["feature_store_rows"]) == {0, 1}
