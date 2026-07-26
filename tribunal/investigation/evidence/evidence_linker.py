"""Evidence Linker module — Infers semantic nodes and directional relationships."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from tribunal.models.evidence_edge import EvidenceEdge
from tribunal.models.evidence_node import EvidenceNode

if TYPE_CHECKING:
    from tribunal.models.investigation_card import InvestigationCard

logger = logging.getLogger("tribunal.investigation.evidence.linker")


class EvidenceLinker:
    """Infers graph nodes and semantic edges (HAS_EVIDENCE, SUPPORTS, CORROBORATES, CONTRADICTS, DERIVED_FROM, SAME_ACCOUNT)."""

    def generate_nodes_and_edges(self, cards: list[InvestigationCard]) -> tuple[list[EvidenceNode], list[EvidenceEdge]]:
        """Construct EvidenceNode and EvidenceEdge objects from a set of InvestigationCard objects."""
        nodes_dict: dict[str, EvidenceNode] = {}
        edges: list[EvidenceEdge] = []

        cards_by_account: dict[str, list[InvestigationCard]] = {}
        cards_by_hypothesis: dict[tuple[str, str], list[InvestigationCard]] = {}

        for card in cards:
            primary_acc = card.affected_accounts[0] if card.affected_accounts else "global"
            cards_by_account.setdefault(primary_acc, []).append(card)

            hyp_slug = card.hypothesis.strip().lower().replace(" ", "_")
            cards_by_hypothesis.setdefault((primary_acc, hyp_slug), []).append(card)

            # 1. Create Account Node if not present
            acc_node_id = f"acc_{primary_acc}"
            if acc_node_id not in nodes_dict:
                nodes_dict[acc_node_id] = EvidenceNode(
                    node_id=acc_node_id,
                    node_type="account",
                    label=f"Account {primary_acc}",
                    expert="system",
                    confidence=1.0,
                    severity="LOW",
                )

            # 2. Create Card Node
            card_node_id = card.card_id
            nodes_dict[card_node_id] = EvidenceNode(
                node_id=card_node_id,
                node_type="card",
                label=f"{card.source_expert.title()} Card: {card.hypothesis[:30]}",
                expert=card.source_expert,
                confidence=card.confidence,
                severity=card.severity,
                timestamp=card.generated_at,
                metadata={
                    "card": card.to_dict(),
                    "affected_accounts": card.affected_accounts,
                    "supporting_features": card.supporting_features,
                    "supporting_metrics": card.supporting_metrics,
                    "evidence": card.evidence,
                },
                provenance=card.provenance or {"transaction_ids": card.derived_from_transactions},
            )

            # 3. Create Hypothesis Node
            hyp_node_id = f"hyp_{hyp_slug}_{primary_acc}"
            if hyp_node_id not in nodes_dict:
                nodes_dict[hyp_node_id] = EvidenceNode(
                    node_id=hyp_node_id,
                    node_type="hypothesis",
                    label=card.hypothesis,
                    expert=card.source_expert,
                    confidence=card.confidence,
                    severity=card.severity,
                )

            # 4. Create HAS_EVIDENCE edge: Account -> Card
            edges.append(
                EvidenceEdge(
                    source=acc_node_id,
                    target=card_node_id,
                    relationship="HAS_EVIDENCE",
                    weight=1.0,
                    reason=f"Account {primary_acc} has evidence card {card_node_id}",
                    confidence=card.confidence,
                )
            )

            # 5. Create SUPPORTS edge: Card -> Hypothesis
            edges.append(
                EvidenceEdge(
                    source=card_node_id,
                    target=hyp_node_id,
                    relationship="SUPPORTS",
                    weight=card.confidence,
                    reason=f"Card {card_node_id} supports hypothesis {card.hypothesis}",
                    confidence=card.confidence,
                )
            )

            # 6. Create DERIVED_FROM edge: Card -> Account / Data
            edges.append(
                EvidenceEdge(
                    source=card_node_id,
                    target=acc_node_id,
                    relationship="DERIVED_FROM",
                    weight=1.0,
                    reason=f"Evidence derived from transactions of account {primary_acc}",
                    confidence=1.0,
                )
            )

        # 7. Infer CORROBORATES & CONTRADICTS & SAME_ACCOUNT edges
        for (acc, hyp_slug), hyp_cards in cards_by_hypothesis.items():
            if len(hyp_cards) >= 2:
                for i in range(len(hyp_cards)):
                    for j in range(i + 1, len(hyp_cards)):
                        c1, c2 = hyp_cards[i], hyp_cards[j]
                        if c1.source_expert != c2.source_expert:
                            edges.append(
                                EvidenceEdge(
                                    source=c1.card_id,
                                    target=c2.card_id,
                                    relationship="CORROBORATES",
                                    weight=round((c1.confidence + c2.confidence) / 2, 2),
                                    reason=f"{c1.source_expert.title()} and {c2.source_expert.title()} independently corroborate hypothesis '{c1.hypothesis}'",
                                    confidence=round(1.0 - (1.0 - c1.confidence) * (1.0 - c2.confidence), 2),
                                )
                            )

        # Infer SAME_ACCOUNT edges between distinct cards for same account
        for acc, acc_cards in cards_by_account.items():
            if len(acc_cards) >= 2:
                for i in range(len(acc_cards)):
                    for j in range(i + 1, len(acc_cards)):
                        c1, c2 = acc_cards[i], acc_cards[j]
                        if c1.hypothesis.strip().lower() != c2.hypothesis.strip().lower():
                            edges.append(
                                EvidenceEdge(
                                    source=c1.card_id,
                                    target=c2.card_id,
                                    relationship="SAME_ACCOUNT",
                                    weight=0.5,
                                    reason=f"Both cards target account {acc}",
                                    confidence=1.0,
                                )
                            )

        return list(nodes_dict.values()), edges
