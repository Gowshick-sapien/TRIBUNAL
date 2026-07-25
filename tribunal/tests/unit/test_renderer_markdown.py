"""Unit tests for MarkdownRenderer (Phase C.7)."""

from __future__ import annotations

from tribunal.models.case_file import CaseFile
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.renderer_markdown import MarkdownRenderer
from tribunal.report.report_builder import ReportBuilder


def test_markdown_renderer():
    verdict = TribunalVerdict(
        verdict="POSSIBLY_MALICIOUS",
        winning_hypothesis="Multiple Behavioural Anomalies",
        winning_score=0.76,
        confidence=0.58,
    )
    case_file = CaseFile(case_id="case_md")
    report = ReportBuilder().build_report(case_file=case_file, tribunal_verdict=verdict, query_text="Test Markdown")

    renderer = MarkdownRenderer()
    md_text = renderer.render(report)

    assert "# Investigation Report —" in md_text
    assert "## 1. Executive Summary" in md_text
    assert "POSSIBLY_MALICIOUS" in md_text
    assert "Multiple Behavioural Anomalies" in md_text
