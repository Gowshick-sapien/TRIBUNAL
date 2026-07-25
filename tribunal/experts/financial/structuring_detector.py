"""Structuring Detector module — Detects transactions structured just below reporting thresholds."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.financial.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.financial.structuring")


class StructuringDetector:
    """Detects structuring typologies (e.g., repeated transactions just below $10,000 threshold)."""

    detector_name: str = "StructuringDetector"
    detector_version: str = "1.0"

    def __init__(self, threshold: float = 10000.0, proximity_ratio: float = 0.80):
        self.threshold = threshold
        self.lower_bound = threshold * proximity_ratio

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transaction DataFrame and return structuring pattern findings."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not amount_col or not account_col:
            return []

        near_threshold = df[(df[amount_col] >= self.lower_bound) & (df[amount_col] < self.threshold)].copy()
        if near_threshold.empty:
            return []

        grouped = near_threshold.groupby(account_col)

        for account_id, group in grouped:
            count = len(group)
            total_sum = float(group[amount_col].sum())
            avg_amount = float(group[amount_col].mean())

            proximity_score = round(avg_amount / self.threshold, 4)
            count_multiplier = min(1.0, count / 3.0)
            score = round(min(1.0, proximity_score * 0.5 + count_multiplier * 0.5), 2)

            txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

            supporting_metrics = {
                "threshold_proximity": proximity_score,
                "near_threshold_txn_count": float(count),
                "rolling_amount_sum": float(total_sum),
            }

            provenance = {
                "detectors": [self.detector_name],
                "detector_version": self.detector_version,
                "transaction_ids": txn_ids,
                "feature_store_rows": list(group.index.astype(int)),
            }

            finding = PatternFinding(
                pattern_name="structuring",
                score=score,
                supporting_features=[
                    "threshold_proximity",
                    "near_threshold_txn_count",
                    "rolling_amount_sum",
                ],
                supporting_metrics=supporting_metrics,
                provenance=provenance,
                detector_name=self.detector_name,
                detector_version=self.detector_version,
                affected_accounts=[str(account_id)],
                evidence_details=[
                    f"Account {account_id} executed {count} transactions totaling ${total_sum:,.2f} near the ${self.threshold:,.0f} threshold.",
                    f"Average amount ${avg_amount:,.2f} sits at {proximity_score * 100:.1f}% of reporting threshold.",
                ],
                transaction_ids=txn_ids,
            )
            findings.append(finding)

        return findings
