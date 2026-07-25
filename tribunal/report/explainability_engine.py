"""Explainability Engine module — Translates technical metrics into natural language explanations."""

from __future__ import annotations

from typing import Any


class ExplainabilityEngine:
    """Translates internal metric key-values and findings into clear, natural language explanations."""

    def explain_metric(self, key: str, value: Any, threshold: float | None = None) -> str:
        """Convert a single technical metric key-value pair into a human-readable explanation."""
        key_lower = key.lower()

        if "threshold_proximity" in key_lower:
            val_pct = float(value) * 100.0 if float(value) <= 1.0 else float(value)
            return f"Average transaction size sits at {val_pct:.1f}% of the $10,000 regulatory reporting threshold."

        if "near_threshold_txn_count" in key_lower:
            return f"Identified {int(value)} repeated transactions structured just below the reporting limit."

        if "rolling_amount_sum" in key_lower:
            return f"Accumulated an aggregate volume of ${float(value):,.2f} over the evaluation window."

        if "velocity_score" in key_lower or "daily_velocity" in key_lower:
            return f"Recorded an elevated transaction frequency of {float(value):.1f} transactions per day."

        if "burst_score" in key_lower:
            return f"Burst transaction intensity score reached {float(value):.2f}, indicating rapid succession of transfers."

        if "amount_spike_ratio" in key_lower or "behaviour_deviation_ratio" in key_lower:
            return f"Observed a {float(value):.1f}x surge in transaction volume compared with historical daily baseline."

        if "days_since_last_transaction" in key_lower or "dormancy" in key_lower:
            return f"Account reactivated after a dormant period of {int(value)} consecutive days."

        if "currency_switch" in key_lower or "preferred_currency" in key_lower:
            return f"Unexpected currency shift detected ({value}), diverging from the customer's historical profile."

        if "format_switch" in key_lower or "payment_format" in key_lower:
            return f"Unusual payment mechanism switch observed ({value}) relative to established customer patterns."

        if "unique_counterparties" in key_lower or "fan_out" in key_lower:
            return f"Rapid counterparty network expansion with {int(value)} newly observed recipient entities."

        if "plausibility_score" in key_lower:
            return f"Alternative legitimate explanation evaluated with a plausibility score of {float(value):.2f}."

        if "uncertainty_score" in key_lower:
            return f"Evidence sparsity and expert coverage uncertainty measured at {float(value):.2f}."

        return f"Metric '{key}' evaluated at {value}."

    def explain_finding(self, finding_title: str, metrics: dict[str, Any] | None = None) -> list[str]:
        """Generate a list of natural language sentences explaining an investigation finding."""
        explanations: list[str] = [f"Summary: {finding_title}."]
        if metrics:
            for k, v in metrics.items():
                explanations.append(self.explain_metric(k, v))
        return explanations
