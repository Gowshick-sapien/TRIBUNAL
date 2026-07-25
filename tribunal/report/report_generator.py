"""Report Generator — Core orchestrator and single public interface for Phase C.7."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from tribunal.report.explainability_engine import ExplainabilityEngine
from tribunal.report.renderer_html import HTMLRenderer
from tribunal.report.renderer_json import JSONRenderer
from tribunal.report.renderer_markdown import MarkdownRenderer
from tribunal.report.report_builder import ReportBuilder
from tribunal.report.report_validator import ReportValidator

if TYPE_CHECKING:
    from tribunal.models.case_file import CaseFile
    from tribunal.models.evidence_graph import EvidenceGraph
    from tribunal.models.investigation_report import InvestigationReport
    from tribunal.models.tribunal_verdict import TribunalVerdict

logger = logging.getLogger("tribunal.report.report_generator")


class ReportGenerator:
    """Transforms the complete TRIBUNAL investigation lifecycle into an explainable, auditable report."""

    def __init__(self) -> None:
        self.explainability_engine = ExplainabilityEngine()
        self.report_builder = ReportBuilder(self.explainability_engine)
        self.markdown_renderer = MarkdownRenderer()
        self.html_renderer = HTMLRenderer()
        self.json_renderer = JSONRenderer()
        self.validator = ReportValidator()

    def generate(
        self,
        planner_context: Any = None,
        case_file: CaseFile | None = None,
        evidence_graph: EvidenceGraph | None = None,
        tribunal_verdict: TribunalVerdict | None = None,
        query_text: str = "",
        # Backward compatibility parameters
        verdict: TribunalVerdict | None = None,
        execution_plan: Any = None,
        query_context: Any = None,
        all_cards: list[Any] | None = None,
    ) -> InvestigationReport:
        """Single public entry point to generate a complete, validated, multi-format InvestigationReport."""
        logger.info("Executing Phase C.7 Investigation Report & Explainability Engine...")

        # Handle backward compatibility parameters
        final_verdict = tribunal_verdict or verdict
        final_planner = planner_context or execution_plan or query_context
        final_query = query_text or getattr(query_context, "query", "") or getattr(final_planner, "query", "")

        # 1. Build structured 10-section report
        report = self.report_builder.build_report(
            planner_context=final_planner,
            case_file=case_file,
            evidence_graph=evidence_graph,
            tribunal_verdict=final_verdict,
            query_text=final_query,
        )

        # 2. Render Markdown, HTML, and JSON outputs
        report.markdown_content = self.markdown_renderer.render(report)
        report.html_content = self.html_renderer.render(report)
        report.json_payload = self.json_renderer.render_dict(report)

        # Populate legacy full_text attribute for backward compatibility
        report.full_text = report.markdown_content

        # 3. Validate report completeness & integrity
        self.validator.validate(report)

        logger.info(f"InvestigationReport '{report.report_id}' successfully generated and validated.")
        return report
