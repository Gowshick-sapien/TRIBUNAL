"""Report Validator module — Enforces strict report quality and completeness criteria."""

from __future__ import annotations

from tribunal.models.investigation_report import InvestigationReport


class ReportValidationError(ValueError):
    """Raised when an InvestigationReport fails completeness validation criteria."""
    pass


class ReportValidator:
    """Validates completeness and integrity of generated InvestigationReport instances."""

    def validate(self, report: InvestigationReport) -> bool:
        """Enforce completeness criteria across all mandatory report sections."""
        if not report:
            raise ReportValidationError("Report object cannot be None.")

        if not report.report_id:
            raise ReportValidationError("Report metadata is missing mandatory 'report_id'.")

        if not report.generated_at:
            raise ReportValidationError("Report metadata is missing mandatory 'generated_at' timestamp.")

        es = report.executive_summary
        if not es or not isinstance(es, dict):
            raise ReportValidationError("Report is missing mandatory 'executive_summary' section.")

        if "verdict" not in es or not es["verdict"]:
            raise ReportValidationError("Executive summary is missing mandatory 'verdict'.")

        if "calibrated_confidence" not in es:
            raise ReportValidationError("Executive summary is missing mandatory 'calibrated_confidence'.")

        if "primary_hypothesis" not in es or not es["primary_hypothesis"]:
            raise ReportValidationError("Executive summary is missing mandatory 'primary_hypothesis'.")

        if report.evidence_summary is None:
            raise ReportValidationError("Report is missing mandatory 'evidence_summary' section.")

        if report.audit_trail is None:
            raise ReportValidationError("Report is missing mandatory 'audit_trail' section.")

        return True
