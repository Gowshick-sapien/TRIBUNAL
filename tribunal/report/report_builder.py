"""Report Builder module — Orchestrates section builders into structured InvestigationReport."""

from __future__ import annotations

import datetime
import uuid
from typing import Any

from tribunal.models.investigation_report import InvestigationReport
from tribunal.models.tribunal_verdict import TribunalVerdict
from tribunal.report.evidence_summarizer import EvidenceSummarizer
from tribunal.report.executive_summary import ExecutiveSummaryBuilder
from tribunal.report.explainability_engine import ExplainabilityEngine
from tribunal.report.graph_summarizer import GraphSummarizer
from tribunal.report.investigation_timeline import InvestigationTimelineBuilder
from tribunal.report.tribunal_summary import TribunalSummaryBuilder


class ReportBuilder:
    """Orchestrates 10 report section projections into a single structured InvestigationReport."""

    def __init__(
        self,
        explainability_engine: ExplainabilityEngine | None = None,
    ) -> None:
        self.explainability_engine = explainability_engine or ExplainabilityEngine()
        self.exec_summary_builder = ExecutiveSummaryBuilder()
        self.timeline_builder = InvestigationTimelineBuilder()
        self.evidence_summarizer = EvidenceSummarizer(self.explainability_engine)
        self.graph_summarizer = GraphSummarizer()
        self.tribunal_summary_builder = TribunalSummaryBuilder()

    def build_report(
        self,
        planner_context: Any = None,
        case_file: Any = None,
        evidence_graph: Any = None,
        tribunal_verdict: TribunalVerdict | None = None,
        query_text: str = "",
    ) -> InvestigationReport:
        """Construct all 10 section payloads into an InvestigationReport object."""
        case_id = getattr(case_file, "case_id", "default_case") if case_file else "default_case"
        report_id = f"rpt_{case_id}_{uuid.uuid4().hex[:6]}"
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Section 1: Executive Summary
        exec_summary = self.exec_summary_builder.build(
            verdict=tribunal_verdict,
            query_text=query_text,
            case_id=case_id,
        )

        # Section 2: Query Interpretation
        intent = "unknown"
        experts_invoked = []
        target_entities: list[str] = []
        resolved_target_id = "N/A"
        target_resolution_status = "GENERAL_SEARCH"

        if planner_context:
            inv_plan = getattr(planner_context, "investigation_plan", None)
            exec_plan = getattr(planner_context, "execution_plan", None)
            if inv_plan:
                intent = getattr(inv_plan, "intent", "unknown")
                if getattr(inv_plan, "entities", None):
                    target_entities.extend([str(e) for e in inv_plan.entities])
                elif getattr(inv_plan, "customer_id", None):
                    target_entities.append(str(inv_plan.customer_id))
            if exec_plan:
                experts_invoked = getattr(exec_plan, "expert_sequence", [])
                if getattr(exec_plan, "filters", None) and isinstance(exec_plan.filters, dict):
                    cust_id = exec_plan.filters.get("customer_id")
                    if cust_id and str(cust_id) not in target_entities:
                        target_entities.append(str(cust_id))
                    ents = exec_plan.filters.get("entities")
                    if isinstance(ents, list):
                        for ent in ents:
                            if str(ent) not in target_entities:
                                target_entities.append(str(ent))

        if target_entities:
            target_resolution_status = "EXACT_MATCH"
            resolved_target_id = ", ".join(target_entities)

        query_interp = {
            "raw_query": query_text or "General Investigation Query",
            "parsed_intent": intent,
            "experts_invoked": experts_invoked,
            "target_entities": target_entities,
            "resolved_target_id": resolved_target_id,
            "target_resolution_status": target_resolution_status,
            "interpretation_statement": f"User query '{query_text}' parsed as intent '{intent}' targeting target '{resolved_target_id}' ({target_resolution_status}) with experts {experts_invoked}.",
        }

        # Section 3: Investigation Timeline
        timeline = self.timeline_builder.build(
            planner_context=planner_context,
            case_file=case_file,
            evidence_graph=evidence_graph,
            tribunal_verdict=tribunal_verdict,
        )

        # Section 4: Expert Findings
        expert_findings = self.evidence_summarizer.build_expert_findings(case_file)

        # Section 5: Evidence Summary
        evidence_summary = {
            "total_cards": len(expert_findings),
            "prosecution_cards": len([f for f in expert_findings if f["expert"] != "defense"]),
            "defense_cards": len([f for f in expert_findings if f["expert"] == "defense"]),
            "findings_by_expert": expert_findings,
        }

        # Section 6: Graph Summary
        graph_summary = self.graph_summarizer.build(evidence_graph)

        # Section 7: Defense Review
        defense_summary = self.tribunal_summary_builder.build_defense_summary(case_file)

        # Section 8: Tribunal Deliberation
        tribunal_summary = self.tribunal_summary_builder.build_tribunal_summary(tribunal_verdict)

        # Section 9: Evidence Provenance
        provenance_details = self.evidence_summarizer.build_provenance_details(case_file)

        # Section 10: Audit Trail
        audit_trail = list(tribunal_summary.get("deliberation_trace", []))

        metadata = {
            "report_id": report_id,
            "generated_at": now_str,
            "case_id": case_id,
            "engine_version": "C.7",
            "confidence": exec_summary.get("calibrated_confidence", 0.0),
            "risk_level": exec_summary.get("risk_level", "MEDIUM"),
        }

        # Construct InvestigationReport
        report = InvestigationReport(
            report_id=report_id,
            generated_at=now_str,
            metadata=metadata,
            executive_summary=exec_summary,
            query_interpretation=query_interp,
            timeline=timeline,
            expert_findings=expert_findings,
            evidence_summary=evidence_summary,
            graph_summary=graph_summary,
            defense_summary=defense_summary,
            tribunal_summary=tribunal_summary,
            provenance_details=provenance_details,
            audit_trail=audit_trail,
            query_recap=query_text,
            winning_hypothesis=exec_summary.get("primary_hypothesis", ""),
            winning_confidence=exec_summary.get("calibrated_confidence", 0.0),
            risk_level=exec_summary.get("risk_level", "MEDIUM"),
            recommendation=exec_summary.get("recommendation", ""),
            runner_up_hypothesis=exec_summary.get("secondary_hypothesis"),
            runner_up_confidence=exec_summary.get("secondary_score"),
        )

        return report
