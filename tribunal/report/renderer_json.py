"""JSON Renderer module — Renders InvestigationReport into structured JSON API payload."""

from __future__ import annotations

import json
from typing import Any

from tribunal.models.investigation_report import InvestigationReport


class JSONRenderer:
    """Renders structured InvestigationReport into JSON payload string or dictionary."""

    def render_dict(self, report: InvestigationReport) -> dict[str, Any]:
        """Transform InvestigationReport into a clean dictionary."""
        return {
            "metadata": report.metadata,
            "executive_summary": report.executive_summary,
            "query_interpretation": report.query_interpretation,
            "timeline": report.timeline,
            "expert_findings": report.expert_findings,
            "evidence_summary": report.evidence_summary,
            "graph_summary": report.graph_summary,
            "defense_summary": report.defense_summary,
            "tribunal_summary": report.tribunal_summary,
            "provenance_details": report.provenance_details,
            "audit_trail": report.audit_trail,
        }

    def render(self, report: InvestigationReport) -> str:
        """Transform InvestigationReport into formatted JSON string."""
        return json.dumps(self.render_dict(report), indent=2)
