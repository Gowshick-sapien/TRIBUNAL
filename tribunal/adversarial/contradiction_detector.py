"""Contradiction Detector — Identifies conflicting signals across investigation cards."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tribunal.adversarial.evidence_reviewer import ReviewContext
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class ContradictionFinding:
    """Represents a conflict between two expert findings or baseline signals."""

    account_id: str
    primary_card_id: str
    conflicting_card_id: str | None
    conflict_type: str  # e.g., "financial_vs_behaviour", "velocity_vs_stable"
    description: str
    severity: str = "MEDIUM"
    confidence_delta: float = 0.20


class ContradictionDetector:
    """Detects contradictions between prosecution findings across domain experts."""

    def detect(self, ctx: ReviewContext) -> list[ContradictionFinding]:
        """Analyze ReviewContext and return a list of ContradictionFinding objects."""
        findings: list[ContradictionFinding] = []

        for acc_id, cards in ctx.account_cards_map.items():
            if len(cards) < 2:
                continue

            fin_cards = [c for c in cards if c.source_expert == "financial"]
            beh_cards = [c for c in cards if c.source_expert == "behaviour"]

            # Scenario 1: Financial Structuring / Velocity vs Behaviour Stable Baseline
            for fin_card in fin_cards:
                for beh_card in beh_cards:
                    beh_metrics = beh_card.supporting_metrics or {}
                    
                    # Conflict: Financial Structuring vs Normal Behaviour Baseline
                    if "structuring" in fin_card.hypothesis.lower() and beh_card.confidence < 0.60:
                        findings.append(
                            ContradictionFinding(
                                account_id=acc_id,
                                primary_card_id=fin_card.card_id,
                                conflicting_card_id=beh_card.card_id,
                                conflict_type="financial_vs_behaviour",
                                description=(
                                    f"Financial Structuring card ({fin_card.card_id}) conflicts with "
                                    f"low-confidence behavioural anomaly card ({beh_card.card_id})."
                                ),
                                severity="HIGH",
                                confidence_delta=0.25,
                            )
                        )

                    # Conflict: High Velocity vs Low Behaviour Drift Ratio
                    velocity_score = fin_card.supporting_metrics.get("velocity_score", 0.0)
                    drift_ratio = beh_metrics.get("behaviour_deviation_ratio", 1.0)
                    if velocity_score > 0.70 and drift_ratio < 2.0:
                        findings.append(
                            ContradictionFinding(
                                account_id=acc_id,
                                primary_card_id=fin_card.card_id,
                                conflicting_card_id=beh_card.card_id,
                                conflict_type="velocity_vs_stable",
                                description=(
                                    f"High velocity score ({velocity_score:.2f}) on {fin_card.card_id} "
                                    f"conflicts with low behavioural deviation ({drift_ratio:.2f}) on {beh_card.card_id}."
                                ),
                                severity="MEDIUM",
                                confidence_delta=0.20,
                            )
                        )

        return findings
