"""Unit tests for ReportValidator (Phase C.7)."""

from __future__ import annotations

import pytest
from tribunal.models.investigation_report import InvestigationReport
from tribunal.report.report_validator import ReportValidator, ReportValidationError


def test_report_validator_valid():
    report = InvestigationReport(
        report_id="rpt_123",
        generated_at="2026-07-25T12:00:00Z",
        executive_summary={
            "verdict": "POSSIBLY_MALICIOUS",
            "calibrated_confidence": 0.65,
            "primary_hypothesis": "Test Hypothesis",
        },
        evidence_summary={},
        audit_trail=[],
    )

    validator = ReportValidator()
    assert validator.validate(report) is True


def test_report_validator_missing_verdict():
    report = InvestigationReport(
        report_id="rpt_123",
        generated_at="2026-07-25T12:00:00Z",
        executive_summary={
            "calibrated_confidence": 0.65,
            "primary_hypothesis": "Test Hypothesis",
        },
    )

    validator = ReportValidator()
    with pytest.raises(ReportValidationError, match="missing mandatory 'verdict'"):
        validator.validate(report)
