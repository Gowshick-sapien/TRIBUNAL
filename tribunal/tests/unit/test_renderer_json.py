"""Unit tests for JSONRenderer (Phase C.7)."""

from __future__ import annotations

import json
from tribunal.models.case_file import CaseFile
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.renderer_json import JSONRenderer
from tribunal.report.report_builder import ReportBuilder


def test_json_renderer():
    verdict = TribunalVerdict(
        verdict="LIKELY_LEGITIMATE",
        winning_hypothesis="Legitimate Business Activity",
        winning_score=0.82,
        confidence=0.75,
    )
    case_file = CaseFile(case_id="case_json")
    report = ReportBuilder().build_report(case_file=case_file, tribunal_verdict=verdict, query_text="Test JSON")

    renderer = JSONRenderer()
    json_str = renderer.render(report)
    parsed = json.loads(json_str)

    assert "metadata" in parsed
    assert "executive_summary" in parsed
    assert parsed["executive_summary"]["verdict"] == "LIKELY_LEGITIMATE"
    assert parsed["executive_summary"]["primary_hypothesis"] == "Legitimate Business Activity"
