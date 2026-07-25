"""Unit tests for ExecutiveSummaryBuilder (Phase C.7)."""

from __future__ import annotations

from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.executive_summary import ExecutiveSummaryBuilder


def test_executive_summary_builder():
    verdict = TribunalVerdict(
        verdict="POSSIBLY_MALICIOUS",
        winning_hypothesis="Multiple Behavioural Anomalies for Account ACC_1",
        winning_score=0.76,
        confidence=0.58,
        primary_hypothesis="Multiple Behavioural Anomalies for Account ACC_1",
        primary_score=0.76,
        secondary_hypothesis="Possible Structuring Activity",
        secondary_score=0.74,
        confidence_gap=0.02,
        risk_level="MEDIUM",
    )

    builder = ExecutiveSummaryBuilder()
    summary = builder.build(verdict=verdict, query_text="Investigate account ACC_1", case_id="case_001")

    assert summary["case_id"] == "case_001"
    assert summary["verdict"] == "POSSIBLY_MALICIOUS"
    assert summary["primary_hypothesis"] == "Multiple Behavioural Anomalies for Account ACC_1"
    assert summary["primary_score"] == 0.76
    assert summary["secondary_hypothesis"] == "Possible Structuring Activity"
    assert summary["confidence_gap"] == 0.02
    assert summary["calibrated_confidence"] == 0.58
    assert summary["risk_level"] == "MEDIUM"
