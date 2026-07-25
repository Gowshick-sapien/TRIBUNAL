"""Alternative Hypothesis Generator — Generates plausible non-malicious competing explanations."""

from __future__ import annotations

from dataclasses import dataclass, field

from tribunal.adversarial.evidence_reviewer import ReviewContext
from tribunal.models.investigation_card import InvestigationCard


@dataclass
class AlternativeExplanation:
    """Represents a specific legitimate, non-malicious explanation supporting a top-level hypothesis."""

    account_id: str
    target_card_id: str
    category: str  # e.g., "payroll", "invoice_settlement", "festival_shopping", "merchant_settlement"
    explanation_title: str
    top_level_hypothesis: str
    explanation_details: str
    plausibility_score: float
    supporting_signals: list[str] = field(default_factory=list)

    @property
    def title(self) -> str:
        """Alias for top_level_hypothesis for card construction."""
        return self.top_level_hypothesis

    @property
    def explanation(self) -> str:
        """Alias for explanation_details."""
        return self.explanation_details


# Alias for backward compatibility
AlternativeHypothesis = AlternativeExplanation


class AlternativeHypothesisGenerator:
    """Generates plausible non-malicious explanations challenging prosecution cards."""

    def generate(self, ctx: ReviewContext) -> list[AlternativeExplanation]:
        """Analyze prosecution cards and generate alternative non-malicious explanations."""
        alternatives: list[AlternativeExplanation] = []

        for card in ctx.prosecution_cards:
            acc_id = card.affected_accounts[0] if card.affected_accounts else "UNKNOWN_ACCOUNT"
            hyp_lower = card.hypothesis.lower()
            metrics = card.supporting_metrics or {}
            top_hypothesis = f"Legitimate Business Activity for Account {acc_id}"

            # Case A: Structuring / Sub-threshold deposits -> Payroll or Batch Settlement
            if "structuring" in hyp_lower or "threshold" in hyp_lower:
                alternatives.append(
                    AlternativeExplanation(
                        account_id=acc_id,
                        target_card_id=card.card_id,
                        category="payroll",
                        explanation_title=f"Routine Business Payroll & Invoice Batch Settlement",
                        top_level_hypothesis=top_hypothesis,
                        explanation_details=(
                            f"Multiple sub-threshold payments for account {acc_id} represent "
                            "routine payroll distribution, vendor invoice batch payments, or merchant settlement."
                        ),
                        plausibility_score=0.72,
                        supporting_signals=[
                            "batch_payment_pattern",
                            "recurring_monthly_schedule",
                            "business_account_profile",
                        ],
                    )
                )

            # Case B: Velocity Spike -> Seasonal Activity or Festival Shopping
            if "velocity" in hyp_lower or "rapid" in hyp_lower or metrics.get("velocity_score", 0.0) > 0.5:
                alternatives.append(
                    AlternativeExplanation(
                        account_id=acc_id,
                        target_card_id=card.card_id,
                        category="festival_shopping",
                        explanation_title=f"Festival Shopping & Monthly Bill Settlements",
                        top_level_hypothesis=top_hypothesis,
                        explanation_details=(
                            f"Rapid transaction volume on account {acc_id} aligns with legitimate "
                            "holiday/festival bulk purchases or monthly recurring bill settlements."
                        ),
                        plausibility_score=0.68,
                        supporting_signals=[
                            "bulk_purchasing_behaviour",
                            "payroll_day_coincidence",
                        ],
                    )
                )

            # Case C: Dormancy Reactivation -> Annual Tax/Loan Disbursement or Seasonal Business
            if "dormancy" in hyp_lower or metrics.get("days_since_last_transaction", 0) > 60:
                alternatives.append(
                    AlternativeExplanation(
                        account_id=acc_id,
                        target_card_id=card.card_id,
                        category="seasonal_business",
                        explanation_title=f"Seasonal Business Operations & Annual Tax Disbursement",
                        top_level_hypothesis=top_hypothesis,
                        explanation_details=(
                            f"Reactivation of account {acc_id} after inactivity corresponds to "
                            "seasonal business operations, annual tax refund, or contract disbursement."
                        ),
                        plausibility_score=0.70,
                        supporting_signals=[
                            "seasonal_operating_cycle",
                            "disbursement_schedule",
                        ],
                    )
                )

            # Case D: Currency or Payment Format Switch -> Travel or International Vendor
            if "currency" in hyp_lower or "payment" in hyp_lower or metrics.get("currency_switch_frequency", 0) > 0:
                alternatives.append(
                    AlternativeExplanation(
                        account_id=acc_id,
                        target_card_id=card.card_id,
                        category="merchant_settlement",
                        explanation_title=f"International Supplier Settlement & Business Travel Expenses",
                        top_level_hypothesis=top_hypothesis,
                        explanation_details=(
                            f"Currency or payment format switch on account {acc_id} reflects "
                            "legitimate cross-border supplier settlement or corporate travel expenses."
                        ),
                        plausibility_score=0.65,
                        supporting_signals=[
                            "cross_border_supplier_contract",
                            "corporate_travel_policy",
                        ],
                    )
                )

        return alternatives
