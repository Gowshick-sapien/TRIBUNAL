"""Spending Pattern Detector module — Detects sudden shifts in transaction amounts."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.spending")


class SpendingPatternDetector:
    """Detects sudden drastic shifts in transaction amount distributions."""

    detector_name: str = "SpendingPatternDetector"
    detector_version: str = "1.0"

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transaction amounts for spending pattern shifts."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col or not amount_col:
            return []

        grouped = df.groupby(account_col)

        for account_id, group in grouped:
            max_amt = float(group[amount_col].max())
            min_amt = float(group[amount_col].min())
            mean_amt = float(group[amount_col].mean())

            # Detect large ratio difference between max transaction and mean or standard baseline
            if len(group) >= 2 and max_amt > mean_amt * 2.5 and max_amt >= 5000.0:
                score = min(1.0, round(max_amt / (mean_amt * 4.0), 2))
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "max_transaction_amount": max_amt,
                    "mean_transaction_amount": mean_amt,
                    "amount_spike_ratio": round(max_amt / max(1.0, mean_amt), 2),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="spending_pattern_change",
                    score=max(0.65, score),
                    supporting_features=[
                        "rolling_mean",
                        "rolling_std",
                        "amount_percentile",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} experienced a spending pattern shift: peak transaction ${max_amt:,.2f} is {max_amt / max(1.0, mean_amt):.1f}x the mean ${mean_amt:,.2f}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
