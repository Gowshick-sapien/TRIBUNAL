"""Unit tests for EvidenceMerger."""

import pytest
from tribunal.investigation.evidence.evidence_merger import EvidenceMerger
from tribunal.models.investigation_card import InvestigationCard


def test_evidence_merger_duplicate_cards():
    merger = EvidenceMerger()
    card1 = InvestigationCard(
        card_id="c1",
        source_expert="financial",
        derived_from_transactions=["TX1"],
        generated_at="2026-07-25T12:00:00Z",
        hypothesis="Possible Structuring",
        confidence=0.80,
        severity="HIGH",
        affected_accounts=["ACC_100"],
        supporting_metrics={"structuring_score": 0.85},
        provenance={"detectors": ["StructuringDetector"]},
    )
    card2 = InvestigationCard(
        card_id="c2",
        source_expert="financial",
        derived_from_transactions=["TX2"],
        generated_at="2026-07-25T12:05:00Z",
        hypothesis="Possible Structuring",
        confidence=0.90,
        severity="CRITICAL",
        affected_accounts=["ACC_100"],
        supporting_metrics={"velocity_score": 0.90},
        provenance={"detectors": ["VelocityDetector"]},
    )

    merged = merger.merge_cards([card1, card2])
    assert len(merged) == 1
    m = merged[0]
    assert m.confidence == 0.90
    assert m.source_expert == "financial"
    assert set(m.derived_from_transactions) == {"TX1", "TX2"}
    assert "StructuringDetector" in m.provenance["detectors"]
    assert "VelocityDetector" in m.provenance["detectors"]
