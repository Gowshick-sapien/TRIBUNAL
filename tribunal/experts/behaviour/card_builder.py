"""Card Builder module — Translates aggregated behavioural findings into InvestigationCard domain objects."""

from __future__ import annotations

from datetime import datetime, timezone
import uuid

from tribunal.experts.behaviour.confidence import AggregatedFinding
from tribunal.models.investigation_card import InvestigationCard


class CardBuilder:
    """Translates internal AggregatedFinding objects into standardized InvestigationCard domain objects."""

    def build_cards(self, aggregated_findings: list[AggregatedFinding]) -> list[InvestigationCard]:
        """Convert a list of AggregatedFinding objects into InvestigationCard objects."""
        cards: list[InvestigationCard] = []

        for idx, finding in enumerate(aggregated_findings, start=1):
            now_str = datetime.now(timezone.utc).isoformat()
            card_id = f"card_beh_{idx:03d}_{uuid.uuid4().hex[:6]}"

            card = InvestigationCard(
                card_id=card_id,
                source_expert="behaviour",
                derived_from_transactions=finding.transaction_ids,
                generated_at=now_str,
                hypothesis=finding.hypothesis,
                confidence=finding.combined_confidence,
                severity=finding.severity,
                evidence=finding.evidence_details,
                supporting_features=finding.supporting_features,
                supporting_metrics=finding.supporting_metrics,
                provenance=finding.provenance,
                affected_accounts=finding.affected_accounts,
                time_window=finding.time_window,
                supports=finding.supporting_features,
            )
            cards.append(card)

        return cards
