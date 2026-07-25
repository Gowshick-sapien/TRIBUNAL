"""Uncertainty Estimator — Evaluates evidence sparsity, single-expert risk, and uncertainty scores."""

from __future__ import annotations

from dataclasses import dataclass

from tribunal.adversarial.evidence_reviewer import ReviewContext
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class UncertaintyScore:
    """Uncertainty analysis result for an account or hypothesis."""

    account_id: str
    uncertainty_score: float  # 0.0 (low uncertainty) to 1.0 (high uncertainty)
    expert_diversity: int  # number of distinct experts
    card_count: int
    is_high_uncertainty: bool


class UncertaintyEstimator:
    """Estimates investigation uncertainty based on card volume, expert diversity, and evidence coverage."""

    def estimate_for_account(self, account_id: str, ctx: ReviewContext) -> UncertaintyScore:
        """Calculate UncertaintyScore for a specific account."""
        cards = ctx.account_cards_map.get(account_id, [])
        card_count = len(cards)

        experts = {c.source_expert for c in cards}
        expert_diversity = len(experts)

        if card_count == 0:
            return UncertaintyScore(
                account_id=account_id,
                uncertainty_score=1.0,
                expert_diversity=0,
                card_count=0,
                is_high_uncertainty=True,
            )

        # Base uncertainty calculation:
        # 1 card -> 0.70 uncertainty base
        # 2 cards -> 0.40 uncertainty base
        # 3+ cards -> 0.20 uncertainty base
        if card_count == 1:
            base_u = 0.70
        elif card_count == 2:
            base_u = 0.40
        else:
            base_u = 0.20

        # Multi-expert reduction: if multiple domain experts agree, uncertainty drops by 0.20
        if expert_diversity > 1:
            base_u = max(0.05, base_u - 0.20)

        is_high = base_u >= 0.50

        return UncertaintyScore(
            account_id=account_id,
            uncertainty_score=round(base_u, 3),
            expert_diversity=expert_diversity,
            card_count=card_count,
            is_high_uncertainty=is_high,
        )

    def estimate_all(self, ctx: ReviewContext) -> dict[str, UncertaintyScore]:
        """Estimate uncertainty scores for all accounts present in ReviewContext."""
        scores: dict[str, UncertaintyScore] = {}
        for node in ctx.account_nodes:
            acc_id = node.node_id.replace("acc_", "")
            scores[acc_id] = self.estimate_for_account(acc_id, ctx)
        for acc_id in ctx.account_cards_map:
            if acc_id not in scores:
                scores[acc_id] = self.estimate_for_account(acc_id, ctx)
        return scores
