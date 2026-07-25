"""Unit tests for HTMLRenderer (Phase C.7)."""

from __future__ import annotations

from tribunal.models.case_file import CaseFile
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.renderer_html import HTMLRenderer
from tribunal.report.report_builder import ReportBuilder


def test_html_renderer():
    verdict = TribunalVerdict(
        verdict="LIKELY_MALICIOUS",
        winning_hypothesis="Structuring & Velocity Spike",
        winning_score=0.92,
        confidence=0.88,
        risk_level="HIGH",
    )
    case_file = CaseFile(case_id="case_html")
    report = ReportBuilder().build_report(case_file=case_file, tribunal_verdict=verdict, query_text="Test HTML")

    renderer = HTMLRenderer()
    html_text = renderer.render(report)

    assert "<!DOCTYPE html>" in html_text
    assert "<title>TRIBUNAL Investigation Report —" in html_text
    assert "LIKELY_MALICIOUS" in html_text
    assert "#ef4444" in html_text  # High risk / malicious red badge styling
