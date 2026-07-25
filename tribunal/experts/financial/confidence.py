"""Confidence Aggregator module — Deterministically aggregates pattern scores and assigns severity."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Any
from tribunal.experts.financial.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.financial.confidence")


@dataclass
class AggregatedFinding:
    """Aggregated financial finding combining multiple pattern signals for an account."""
    primary_account: str
    primary_pattern: str
    combined_confidence: float
    severity: str
    hypothesis: str
    supporting_features: list[str]
    supporting_metrics: dict[str, float]
    provenance: dict[str, Any]
    affected_accounts: list[str]
    evidence_details: list[str]
    transaction_ids: list[str]
    time_window: Any = None


class ConfidenceAggregator:
    """Combines multiple pattern findings deterministically using 1 - prod(1 - s_i) without AI."""

    @staticmethod
    def calculate_severity(confidence: float) -> str:
        """Map confidence score (0.0 to 1.0) to standardized severity string."""
        if confidence >= 0.90:
            return "CRITICAL"
        elif confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.60:
            return "MEDIUM"
        else:
            return "LOW"

    def aggregate(self, findings: list[PatternFinding]) -> list[AggregatedFinding]:
        """Group pattern findings by primary account, aggregate scores, supporting metrics, and provenance."""
        if not findings:
            return []

        # Group by account
        grouped: dict[str, list[PatternFinding]] = {}
        for f in findings:
            for acc in f.affected_accounts:
                grouped.setdefault(acc, []).append(f)

        results: list[AggregatedFinding] = []

        for acc, acc_findings in grouped.items():
            # Combine scores probabilistically: 1 - prod(1 - s_i)
            prob_product = 1.0
            for f in acc_findings:
                prob_product *= (1.0 - max(0.0, min(1.0, f.score)))
            combined_confidence = round(1.0 - prob_product, 2)

            if combined_confidence < 0.40:
                continue

            severity = self.calculate_severity(combined_confidence)

            # Collect unique pattern names, features, evidence, and transactions
            pattern_names = list(dict.fromkeys(f.pattern_name for f in acc_findings))
            primary_pattern = pattern_names[0] if pattern_names else "financial_anomaly"

            supp_features = list(dict.fromkeys(feat for f in acc_findings for feat in f.supporting_features))
            evidence_details = list(dict.fromkeys(detail for f in acc_findings for detail in f.evidence_details))
            txns = list(dict.fromkeys(tx for f in acc_findings for tx in f.transaction_ids))
            affected_accounts = list(dict.fromkeys(a for f in acc_findings for a in f.affected_accounts))

            # Aggregate supporting metrics dictionary
            combined_metrics: dict[str, float] = {}
            for f in acc_findings:
                for k, v in f.supporting_metrics.items():
                    combined_metrics[k] = float(v)

            # Aggregate provenance dictionary
            detectors_list = list(dict.fromkeys(f.detector_name for f in acc_findings))
            feature_rows = list(dict.fromkeys(row for f in acc_findings if "feature_store_rows" in f.provenance for row in f.provenance["feature_store_rows"]))

            provenance = {
                "detectors": detectors_list,
                "transaction_ids": txns,
                "feature_store_rows": feature_rows,
            }

            # Build hypothesis title
            if len(pattern_names) > 1:
                hypothesis = f"Multiple Financial Anomalies ({', '.join(p.title().replace('_', ' ') for p in pattern_names)}) for Account {acc}"
            else:
                hypothesis = f"Possible {primary_pattern.title().replace('_', ' ')} Activity for Account {acc}"

            results.append(
                AggregatedFinding(
                    primary_account=acc,
                    primary_pattern=primary_pattern,
                    combined_confidence=combined_confidence,
                    severity=severity,
                    hypothesis=hypothesis,
                    supporting_features=supp_features,
                    supporting_metrics=combined_metrics,
                    provenance=provenance,
                    affected_accounts=affected_accounts,
                    evidence_details=evidence_details,
                    transaction_ids=txns,
                )
            )

        return results
