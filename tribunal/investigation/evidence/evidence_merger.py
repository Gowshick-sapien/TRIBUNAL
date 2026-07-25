"""Evidence Merger module — Consolidates duplicate or identical cards from the same expert."""

from __future__ import annotations

from datetime import datetime, timezone
import logging

from tribunal.investigation.evidence.provenance_manager import ProvenanceManager
from tribunal.models.investigation_card import InvestigationCard

logger = logging.getLogger("tribunal.investigation.evidence.merger")


class EvidenceMerger:
    """Merges duplicate or identical investigation cards from the same expert targeting the same entity."""

    def __init__(self, provenance_manager: ProvenanceManager | None = None):
        self.provenance_manager = provenance_manager or ProvenanceManager()

    def merge_cards(self, cards: list[InvestigationCard]) -> list[InvestigationCard]:
        """Deduplicate and merge identical hypothesis cards from the same expert targeting the same primary account."""
        if not cards:
            return []

        # Group by account, hypothesis, AND source_expert to keep distinct expert findings separate for cross-expert corroboration
        grouped: dict[tuple[str, str, str], list[InvestigationCard]] = {}
        for card in cards:
            primary_acc = card.affected_accounts[0] if card.affected_accounts else "global"
            hyp_key = card.hypothesis.strip().lower()
            key = (primary_acc, hyp_key, card.source_expert)
            grouped.setdefault(key, []).append(card)

        merged_cards: list[InvestigationCard] = []

        for (acc, hyp_key, expert), group in grouped.items():
            if len(group) == 1:
                merged_cards.append(group[0])
            else:
                # Merge multiple duplicate cards from the same expert
                primary_card = group[0]
                combined_confidence = max(c.confidence for c in group)

                all_evidence = list(dict.fromkeys(e for c in group for e in c.evidence))
                all_txns = list(dict.fromkeys(t for c in group for t in c.derived_from_transactions))
                all_features = list(dict.fromkeys(f for c in group for f in c.supporting_features))
                all_accounts = list(dict.fromkeys(a for c in group for a in c.affected_accounts))

                merged_metrics: dict[str, float] = {}
                for c in group:
                    for k, v in c.supporting_metrics.items():
                        merged_metrics[k] = float(v)

                merged_prov = group[0].provenance or {}
                for c in group[1:]:
                    merged_prov = self.provenance_manager.merge_provenance(merged_prov, c.provenance or {})

                now_str = datetime.now(timezone.utc).isoformat()
                merged_card = InvestigationCard(
                    card_id=f"merged_{primary_card.card_id}",
                    source_expert=expert,
                    derived_from_transactions=all_txns,
                    generated_at=now_str,
                    hypothesis=primary_card.hypothesis,
                    confidence=combined_confidence,
                    severity=primary_card.severity,
                    evidence=all_evidence,
                    supporting_features=all_features,
                    supporting_metrics=merged_metrics,
                    provenance=merged_prov,
                    affected_accounts=all_accounts,
                    supports=all_features,
                )
                merged_cards.append(merged_card)

        return merged_cards
