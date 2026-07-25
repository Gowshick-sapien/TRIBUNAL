"""Provenance Manager module — Validates, combines, and maintains evidence lineage."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("tribunal.investigation.evidence.provenance")


class ProvenanceManager:
    """Manages evidence provenance lineage (transaction IDs, feature names, detectors)."""

    def validate_provenance(self, provenance: dict[str, Any] | None) -> bool:
        """Verify that provenance dictionary is valid and contains non-empty evidence lineage."""
        if not provenance or not isinstance(provenance, dict):
            return False
        # Provenance must contain at least transaction IDs, detectors, or feature store rows
        has_txns = bool(provenance.get("transaction_ids") or provenance.get("derived_from_transactions"))
        has_detectors = bool(provenance.get("detectors"))
        has_features = bool(provenance.get("feature_store_rows") or provenance.get("features"))

        return has_txns or has_detectors or has_features

    def merge_provenance(self, prov1: dict[str, Any], prov2: dict[str, Any]) -> dict[str, Any]:
        """Merge two provenance dictionaries preserving all unique lineage items."""
        detectors = list(dict.fromkeys((prov1.get("detectors") or []) + (prov2.get("detectors") or [])))
        txns = list(dict.fromkeys((prov1.get("transaction_ids") or []) + (prov2.get("transaction_ids") or [])))
        rows = list(dict.fromkeys((prov1.get("feature_store_rows") or []) + (prov2.get("feature_store_rows") or [])))
        features = list(dict.fromkeys((prov1.get("features") or []) + (prov2.get("features") or [])))

        merged = {
            "detectors": detectors,
            "transaction_ids": txns,
            "feature_store_rows": rows,
        }
        if features:
            merged["features"] = features
        return merged
