"""Unit tests for EvidenceSummarizer (Phase C.7)."""

from __future__ import annotations

import datetime
from tribunal.models.case_file import CaseFile
from tribunal.models.investigation_card import InvestigationCard
from tribunal.report.evidence_summarizer import EvidenceSummarizer


def test_evidence_summarizer():
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    card1 = InvestigationCard(
        card_id="card_fin_001",
        source_expert="financial",
        derived_from_transactions=["TX_01"],
        generated_at=now_str,
        hypothesis="Structuring Activity",
        confidence=0.85,
        severity="HIGH",
        affected_accounts=["ACC_1"],
        supporting_metrics={"threshold_proximity": 0.96},
        provenance={"detectors": ["StructuringDetector"]},
    )

    case_file = CaseFile(case_id="case_001")
    case_file.add_evidence_card(card1)

    summarizer = EvidenceSummarizer()
    findings = summarizer.build_expert_findings(case_file)

    assert len(findings) == 1
    assert findings[0]["card_id"] == "card_fin_001"
    assert findings[0]["expert"] == "financial"
    assert len(findings[0]["natural_language_explanations"]) == 2

    provenance = summarizer.build_provenance_details(case_file)
    assert len(provenance) == 1
    assert provenance[0]["detectors"] == ["StructuringDetector"]
