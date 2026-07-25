"""Frequency Detector module — Detects abnormal transaction frequency spikes."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.financial.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.financial.frequency")


class FrequencyDetector:
    """Detects high-frequency transaction activity exceeding baseline rates."""

    detector_name: str = "FrequencyDetector"
    detector_version: str = "1.0"

    def __init__(self, high_frequency_count: int = 5):
        self.high_frequency_count = high_frequency_count

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transaction frequency per account and return pattern findings."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col:
            return []

        grouped = df.groupby(account_col)
        for account_id, group in grouped:
            count = len(group)
            if count >= self.high_frequency_count:
                freq_score = min(1.0, round(count / 10.0, 2))
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []
                total_val = float(group[amount_col].sum()) if amount_col else 0.0

                supporting_metrics = {
                    "frequency_count": float(count),
                    "frequency_score": float(freq_score),
                    "rolling_amount_sum": float(total_val),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="frequency",
                    score=max(0.50, freq_score),
                    supporting_features=[
                        "rolling_count",
                        "daily_average_frequency",
                        "weekly_average_frequency",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} performed {count} transactions, exceeding frequency threshold of {self.high_frequency_count}.",
                        f"Total volume across frequency spike: ${total_val:,.2f}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
