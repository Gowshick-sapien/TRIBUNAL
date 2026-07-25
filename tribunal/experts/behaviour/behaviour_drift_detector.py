"""Behaviour Drift Detector module — Detects significant deviation from historical baseline activity."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.drift")


class BehaviourDriftDetector:
    """Detects significant shifts in daily/weekly transaction amounts and rates relative to baseline."""

    detector_name: str = "BehaviourDriftDetector"
    detector_version: str = "1.0"

    def __init__(self, drift_multiplier_threshold: float = 2.5):
        self.drift_multiplier_threshold = drift_multiplier_threshold

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transactions for behavioural drift against historical baseline."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col or not amount_col:
            return []

        overall_avg = float(df[amount_col].mean()) if len(df) > 0 else 100.0
        grouped = df.groupby(account_col)

        for account_id, group in grouped:
            acc_avg = float(group[amount_col].mean())
            acc_total = float(group[amount_col].sum())
            count = len(group)

            # Check if account average is significantly higher than historical baseline / overall average
            baseline = group["baseline_daily_amount"].iloc[0] if "baseline_daily_amount" in group.columns else overall_avg
            baseline = max(1.0, float(baseline))
            ratio = round(acc_avg / baseline, 2)

            if ratio >= self.drift_multiplier_threshold:
                drift_score = min(1.0, round(ratio / 5.0, 2))
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "baseline_daily_amount": baseline,
                    "current_average_amount": acc_avg,
                    "behaviour_deviation_ratio": ratio,
                    "rolling_amount_sum": acc_total,
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="behaviour_drift",
                    score=max(0.60, drift_score),
                    supporting_features=[
                        "baseline_daily_amount",
                        "average_amount",
                        "transaction_frequency",
                        "behaviour_deviation",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} exhibited severe behavioural drift: average transaction ${acc_avg:,.2f} is {ratio:.1f}x higher than baseline ${baseline:,.2f}.",
                        f"Executed {count} transactions totaling ${acc_total:,.2f}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
