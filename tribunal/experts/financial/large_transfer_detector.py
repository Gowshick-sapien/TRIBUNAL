"""Large Transfer Detector module — Detects statistically significant large transactions."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.financial.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.financial.large_transfer")


class LargeTransferDetector:
    """Detects unusually large transfer amounts exceeding historical baselines or statistical thresholds."""

    detector_name: str = "LargeTransferDetector"
    detector_version: str = "1.0"

    def __init__(self, fixed_large_threshold: float = 50000.0, std_dev_multiplier: float = 2.5):
        self.fixed_large_threshold = fixed_large_threshold
        self.std_dev_multiplier = std_dev_multiplier

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transactions for statistical outliers and large transfer anomalies."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not amount_col or not account_col:
            return []

        mean_amt = df[amount_col].mean()
        std_amt = df[amount_col].std() if len(df) > 4 else 0.0

        cutoff = self.fixed_large_threshold
        if std_amt > 0:
            cutoff = min(cutoff, mean_amt + self.std_dev_multiplier * std_amt)

        large_txns = df[df[amount_col] >= cutoff].copy()
        if large_txns.empty:
            return []

        grouped = large_txns.groupby(account_col)
        for account_id, group in grouped:
            max_amt = float(group[amount_col].max())
            count = len(group)
            total_val = float(group[amount_col].sum())

            score = min(1.0, round(max_amt / (self.fixed_large_threshold * 1.5), 2))
            txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

            supporting_metrics = {
                "max_transaction_amount": max_amt,
                "cutoff_threshold": float(cutoff),
                "large_transfer_count": float(count),
                "rolling_amount_sum": float(total_val),
            }

            provenance = {
                "detectors": [self.detector_name],
                "detector_version": self.detector_version,
                "transaction_ids": txn_ids,
                "feature_store_rows": list(group.index.astype(int)),
            }

            finding = PatternFinding(
                pattern_name="large_transfer",
                score=max(0.60, score),
                supporting_features=[
                    "amount_percentile",
                    "std_dev_multiplier",
                    "historical_baseline_ratio",
                ],
                supporting_metrics=supporting_metrics,
                provenance=provenance,
                detector_name=self.detector_name,
                detector_version=self.detector_version,
                affected_accounts=[str(account_id)],
                evidence_details=[
                    f"Account {account_id} executed {count} large transfer(s) exceeding threshold ${cutoff:,.2f}.",
                    f"Maximum single transaction amount: ${max_amt:,.2f} (Total: ${total_val:,.2f}).",
                ],
                transaction_ids=txn_ids,
            )
            findings.append(finding)

        return findings
