"""Contradiction Resolver module — Evaluates opposing evidence and calculates Net Support."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.consensus.evidence_weigher import HypothesisScore
from tribunal.consensus.hypothesis_extractor import ExtractedHypothesis
from tribunal.models.evidence_graph import EvidenceGraph


@dataclass
class ResolvedHypothesis:
    hypothesis_id: str
    title: str
    raw_support_score: float
    opposing_score: float
    net_support_score: float
    contradiction_reasons: list[str] = field(default_factory=list)
    expert_sources: list[str] = field(default_factory=list)
    is_defense_hypothesis: bool = False
    supporting_cards: list[str] = field(default_factory=list)


class ContradictionResolver:
    """Evaluates opposing evidence, defense challenges, and expert contradictions to calculate Net Evidence Strength."""

    def resolve(
        self,
        scores: list[HypothesisScore],
        extracted_hypotheses: list[ExtractedHypothesis],
        graph: EvidenceGraph,
    ) -> list[ResolvedHypothesis]:
        """Compute opposing evidence penalties and net support scores across hypotheses."""
        resolved: list[ResolvedHypothesis] = []
        nx_graph = graph._graph if graph else None

        # Build map of hypotheses for defense challenge matching
        defense_hypotheses = [h for h in scores if h.is_defense_hypothesis]
        malicious_hypotheses = [h for h in scores if not h.is_defense_hypothesis]

        # Calculate max defense support score if any
        max_defense_support = max([d.raw_support_score for d in defense_hypotheses], default=0.0)

        for h in scores:
            opposing_penalty = 0.0
            reasons: list[str] = []

            if not h.is_defense_hypothesis:
                # Malicious hypothesis opposed by defense alternative explanations
                if defense_hypotheses:
                    # Defense card challenge penalty scales with defense score
                    penalty_factor = min(0.35, max_defense_support * 0.40)
                    opposing_penalty += penalty_factor
                    reasons.append(
                        f"Challenged by {len(defense_hypotheses)} alternative explanation card(s) (defense support: {max_defense_support:.2f})"
                    )

                # Check graph CONTRADICTS edges or expert conflicts
                if nx_graph and h.hypothesis_id in nx_graph:
                    for in_node, _, edge_data in nx_graph.in_edges(h.hypothesis_id, data=True):
                        if edge_data.get("relationship") == "CONTRADICTS":
                            opposing_penalty += 0.25
                            reasons.append(f"Direct graph contradiction edge from node '{in_node}'")
            else:
                # Defense hypothesis opposed by malicious prosecution cards
                max_malicious_support = max([m.raw_support_score for m in malicious_hypotheses], default=0.0)
                if malicious_hypotheses:
                    penalty_factor = min(0.40, max_malicious_support * 0.45)
                    opposing_penalty += penalty_factor
                    reasons.append(
                        f"Opposed by prosecution cards (prosecution support: {max_malicious_support:.2f})"
                    )

            net_score = round(max(0.0, h.raw_support_score - opposing_penalty), 4)

            resolved.append(
                ResolvedHypothesis(
                    hypothesis_id=h.hypothesis_id,
                    title=h.title,
                    raw_support_score=h.raw_support_score,
                    opposing_score=round(opposing_penalty, 4),
                    net_support_score=net_score,
                    contradiction_reasons=reasons,
                    expert_sources=h.expert_sources,
                    is_defense_hypothesis=h.is_defense_hypothesis,
                    supporting_cards=h.supporting_cards,
                )
            )

        return resolved
