"""Evidence Reviewer — Graph traversal and finding extraction for Adversarial Review."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any

from tribunal.models.evidence_graph import EvidenceGraph
from tribunal.models.evidence_node import EvidenceNode
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class ReviewContext:
    """Consolidated context extracted from an EvidenceGraph for adversarial review."""

    graph_snapshot_id: str = ""
    review_timestamp: str = ""
    review_version: str = "C.5"
    account_nodes: list[EvidenceNode] = field(default_factory=list)
    prosecution_cards: list[InvestigationCard] = field(default_factory=list)
    hypotheses: list[EvidenceNode] = field(default_factory=list)
    corroborations: list[tuple[str, str]] = field(default_factory=list)
    contradictions: list[tuple[str, str]] = field(default_factory=list)
    expert_cards_map: dict[str, list[InvestigationCard]] = field(default_factory=dict)
    account_cards_map: dict[str, list[InvestigationCard]] = field(default_factory=dict)


class EvidenceReviewer:
    """Traverses EvidenceGraph to collect cards, hypotheses, snapshot metadata, and relationships for review."""

    def review(self, graph: EvidenceGraph) -> ReviewContext:
        """Traverse the graph and extract structured ReviewContext with snapshot metadata."""
        timestamp_now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        snapshot_id = (
            graph.metadata.get("case_id", "snapshot")
            + f"_{len(graph.nodes)}n_{len(graph.edges)}e"
            if graph and graph.metadata
            else f"snapshot_{len(graph.nodes) if graph else 0}n"
        )

        ctx = ReviewContext(
            graph_snapshot_id=snapshot_id,
            review_timestamp=timestamp_now,
            review_version="C.5",
        )

        if not graph:
            return ctx

        # 1. Extract nodes by type
        for node in graph.nodes:
            if node.node_type == "account":
                ctx.account_nodes.append(node)
            elif node.node_type == "hypothesis":
                ctx.hypotheses.append(node)
            elif node.node_type == "card":
                card_data = node.metadata.get("card")
                if isinstance(card_data, InvestigationCard):
                    card = card_data
                elif isinstance(card_data, dict):
                    card = InvestigationCard(**card_data)
                else:
                    accs = node.metadata.get("affected_accounts", [])
                    card = InvestigationCard(
                        card_id=node.node_id,
                        source_expert=node.expert,
                        derived_from_transactions=node.provenance.get("transactions", []),
                        generated_at=node.timestamp or "",
                        hypothesis=node.label,
                        confidence=node.confidence,
                        severity=node.severity,
                        supporting_metrics=node.metadata.get("metrics", {}),
                        provenance=node.provenance,
                        affected_accounts=accs,
                    )

                if card.source_expert != "defense":
                    ctx.prosecution_cards.append(card)

                    if card.source_expert not in ctx.expert_cards_map:
                        ctx.expert_cards_map[card.source_expert] = []
                    ctx.expert_cards_map[card.source_expert].append(card)

                    acc_list = card.affected_accounts
                    if not acc_list:
                        for edge in graph.edges:
                            if edge.target == card.card_id and edge.source.startswith("acc_"):
                                acc_list.append(edge.source.replace("acc_", ""))
                            elif edge.source == card.card_id and edge.target.startswith("acc_"):
                                acc_list.append(edge.target.replace("acc_", ""))
                        card.affected_accounts = list(set(acc_list))

                    for acc_id in card.affected_accounts:
                        if acc_id not in ctx.account_cards_map:
                            ctx.account_cards_map[acc_id] = []
                        if card not in ctx.account_cards_map[acc_id]:
                            ctx.account_cards_map[acc_id].append(card)

        # 2. Extract edge relationships
        for edge in graph.edges:
            if edge.relationship == "CORROBORATES":
                ctx.corroborations.append((edge.source, edge.target))
            elif edge.relationship == "CONTRADICTS":
                ctx.contradictions.append((edge.source, edge.target))

        return ctx
