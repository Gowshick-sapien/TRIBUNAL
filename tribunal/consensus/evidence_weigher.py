"""Evidence Weigher module — Calculates support scores for hypotheses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.consensus.hypothesis_extractor import ExtractedHypothesis
from tribunal.models.evidence_graph import EvidenceGraph


@dataclass
class HypothesisScore:
    hypothesis_id: str
    title: str
    raw_support_score: float
    expert_confidences: dict[str, float] = field(default_factory=dict)
    expert_sources: list[str] = field(default_factory=list)
    multi_expert_multiplier: float = 1.0
    corroboration_count: int = 0
    supporting_cards: list[str] = field(default_factory=list)
    is_defense_hypothesis: bool = False


class EvidenceWeigher:
    """Weighs evidence quality, expert confidence, and corroboration to compute raw support score for hypotheses."""

    def weigh(
        self,
        extracted_hypotheses: list[ExtractedHypothesis],
        graph: EvidenceGraph,
    ) -> list[HypothesisScore]:
        """Compute support scores across all candidate hypotheses."""
        scores: list[HypothesisScore] = []
        nx_graph = graph._graph if graph else None

        for hyp in extracted_hypotheses:
            expert_confs: dict[str, float] = {}
            cards = hyp.supporting_card_ids if not hyp.is_defense_hypothesis else hyp.defense_card_ids
            if not cards:
                cards = hyp.supporting_card_ids + hyp.defense_card_ids

            # Collect confidence per expert type
            for meta in hyp.cards_metadata:
                exp = meta.get("source_expert", "unknown")
                conf = float(meta.get("confidence", 0.5))
                if exp not in expert_confs or conf > expert_confs[exp]:
                    expert_confs[exp] = conf

            # Check edge weights on SUPPORTS edges in graph
            if nx_graph and hyp.hypothesis_id in nx_graph:
                for in_node, _, edge_data in nx_graph.in_edges(hyp.hypothesis_id, data=True):
                    in_exp = nx_graph.nodes[in_node].get("source_expert", "")
                    weight = edge_data.get("weight") or edge_data.get("confidence", 0.5)
                    if in_exp and (in_exp not in expert_confs or weight > expert_confs[in_exp]):
                        expert_confs[in_exp] = float(weight)

            # Probabilistic support aggregation: 1 - Π(1 - c_i)
            if expert_confs:
                prob_not_supported = 1.0
                for c in expert_confs.values():
                    prob_not_supported *= (1.0 - c)
                base_score = 1.0 - prob_not_supported
            else:
                base_score = 0.40

            # Multi-expert corroboration multiplier
            valid_experts = [e for e in expert_confs.keys() if e != "system"]
            multiplier = 1.0
            if len(valid_experts) > 1:
                multiplier = 1.15  # Boost for multi-expert agreement
            elif len(valid_experts) == 1 and valid_experts[0] != "defense":
                multiplier = 0.95  # Slight penalty for single-expert risk

            final_score = round(min(1.0, base_score * multiplier), 4)

            # Count corroboration edges connected to supporting cards
            corroboration_count = 0
            if nx_graph:
                for c_id in cards:
                    if c_id in nx_graph:
                        for _, out_node, edge_data in nx_graph.out_edges(c_id, data=True):
                            if edge_data.get("relationship") == "CORROBORATES":
                                corroboration_count += 1

            scores.append(
                HypothesisScore(
                    hypothesis_id=hyp.hypothesis_id,
                    title=hyp.title,
                    raw_support_score=final_score,
                    expert_confidences=expert_confs,
                    expert_sources=sorted(list(expert_confs.keys())),
                    multi_expert_multiplier=multiplier,
                    corroboration_count=corroboration_count,
                    supporting_cards=cards,
                    is_defense_hypothesis=hyp.is_defense_hypothesis,
                )
            )

        return scores
