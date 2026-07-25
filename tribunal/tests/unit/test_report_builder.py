"""Unit tests for ReportBuilder (Phase C.7)."""

from __future__ import annotations

from tribunal.models.case_file import CaseFile
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.report_builder import ReportBuilder


def test_report_builder_sections():
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
    case_file = CaseFile(case_id="case_100")

    builder = ReportBuilder()
    report = builder.build_report(
        planner_context=None,
        case_file=case_file,
        evidence_graph=None,
        tribunal_verdict=verdict,
        query_text="Investigate account ACC_1",
    )

    assert report.report_id.startswith("rpt_case_100_")
    assert report.executive_summary["verdict"] == "POSSIBLY_MALICIOUS"
    assert report.query_interpretation["raw_query"] == "Investigate account ACC_1"
    assert len(report.timeline) == 6
    assert report.tribunal_summary["primary_score"] == 0.76
