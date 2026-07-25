"""Verdict Builder module — Assembles structured TribunalVerdict domain object."""

from __future__ import annotations

from typing import Any

from tribunal.consensus.confidence_calibrator import ConfidenceCalibrator
from tribunal.consensus.consensus_engine import ConsensusResult
from tribunal.consensus.deliberation_trace import DeliberationTrace
from tribunal.models.case_file import CaseFile
from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.tribunal_verdict import TribunalVerdict


class VerdictBuilder:
    """Constructs the comprehensive TribunalVerdict domain object."""

    def build_verdict(
        self,
        consensus_result: ConsensusResult,
        calibrated_confidence: float,
        deliberation_trace: DeliberationTrace,
        graph: EvidenceGraph,
        case_file: CaseFile,
    ) -> TribunalVerdict:
        """Assemble all deliberation outputs into a standardized TribunalVerdict."""
        winner = consensus_result.winning_hypothesis
        runner_up = consensus_result.runner_up_hypothesis
        cat = consensus_result.consensus_category

        primary_title = winner.title
        primary_score = winner.net_support_score
        secondary_title = runner_up.title if runner_up else None
        secondary_score = runner_up.net_support_score if runner_up else None
        gap = consensus_result.confidence_gap

        # Collect supporting cards and defense cards
        supporting_cards: list[str] = list(winner.supporting_cards)
        defense_cards_considered: list[str] = []
        if graph and graph._graph:
            for n, d in graph._graph.nodes(data=True):
                if d.get("type") == "card" and d.get("source_expert") == "defense":
                    defense_cards_considered.append(n)

        # Alternative hypotheses titles
        alt_titles = [
            h.title
            for h in consensus_result.ranked_hypotheses[1:]
        ]

        # Supporting experts
        supporting_experts = [e for e in winner.expert_sources if e != "system"]

        # Risk level mapping
        risk_level = "LOW"
        if cat == "LIKELY_MALICIOUS":
            risk_level = "HIGH" if calibrated_confidence >= 0.80 else "MEDIUM"
        elif cat == "POSSIBLY_MALICIOUS":
            risk_level = "MEDIUM"
        elif cat == "INCONCLUSIVE":
            risk_level = "MEDIUM" if calibrated_confidence >= 0.50 else "LOW"
        elif cat == "LIKELY_LEGITIMATE":
            risk_level = "LOW"

        # Evidence summary metrics
        evidence_summary = {
            "prosecution_cards_count": len(supporting_cards),
            "defense_cards_count": len(defense_cards_considered),
            "total_hypotheses_evaluated": len(consensus_result.ranked_hypotheses),
            "graph_node_count": len(graph.nodes) if graph else 0,
            "graph_edge_count": len(graph.edges) if graph else 0,
            "confidence_gap": gap,
            "primary_hypothesis": primary_title,
            "primary_score": primary_score,
            "secondary_hypothesis": secondary_title,
            "secondary_score": secondary_score,
        }

        # Reasoning metadata
        reasoning_metadata = {
            "consensus_category": cat,
            "winning_net_support": primary_score,
            "winning_raw_support": winner.raw_support_score,
            "opposing_penalty": winner.opposing_score,
            "rejection_reason": consensus_result.rejection_reason,
            "case_id": getattr(case_file, "case_id", "default_case") if case_file else "default_case",
        }

        verdict = TribunalVerdict(
            verdict=cat,
            winning_hypothesis=primary_title,
            winning_score=primary_score,
            confidence=calibrated_confidence,
            primary_hypothesis=primary_title,
            primary_score=primary_score,
            secondary_hypothesis=secondary_title,
            secondary_score=secondary_score,
            confidence_gap=gap,
            alternative_hypotheses=alt_titles,
            rejected_hypotheses=consensus_result.rejected_hypotheses,
            supporting_cards=supporting_cards,
            defense_cards_considered=defense_cards_considered,
            supporting_experts=supporting_experts,
            deliberation_trace=deliberation_trace.to_dict_list(),
            evidence_summary=evidence_summary,
            reasoning_metadata=reasoning_metadata,
            winning_confidence=calibrated_confidence,
            winning_chain=supporting_cards,
            risk_level=risk_level,
            recommendation=f"Verdict: {cat} for primary hypothesis '{primary_title}' (confidence: {calibrated_confidence:.2f})",
            runner_up_hypothesis=secondary_title,
            runner_up_confidence=secondary_score,
            rejection_reason=consensus_result.rejection_reason,
        )

        return verdict
