"""Velocity Detector module — Detects rapid transaction bursts and velocity spikes."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.financial.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.financial.velocity")


class VelocityDetector:
    """Detects transaction velocity spikes and rapid fund movement."""

    detector_name: str = "VelocityDetector"
    detector_version: str = "1.0"

    def __init__(self, velocity_threshold_per_day: float = 5.0):
        self.velocity_threshold_per_day = velocity_threshold_per_day

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transaction velocity per account and return pattern findings."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        timestamp_col = "timestamp" if "timestamp" in df.columns else ("Timestamp" if "Timestamp" in df.columns else None)
        amount_col = "amount_received" if "amount_received" in df.columns else ("Amount Received" if "Amount Received" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col:
            return []

        grouped = df.groupby(account_col)

        for account_id, group in grouped:
            total_txns = len(group)
            if total_txns < 3:
                continue

            if timestamp_col and pd.api.types.is_datetime64_any_dtype(group[timestamp_col]):
                time_span_days = max(1.0, (group[timestamp_col].max() - group[timestamp_col].min()).total_seconds() / 86400.0)
            else:
                time_span_days = 1.0

            daily_velocity = round(total_txns / time_span_days, 2)

            if daily_velocity >= self.velocity_threshold_per_day or total_txns >= 8:
                velocity_score = min(1.0, round(daily_velocity / 10.0, 2))
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []
                total_val = float(group[amount_col].sum()) if amount_col else 0.0

                supporting_metrics = {
                    "velocity_score": velocity_score,
                    "daily_velocity": float(daily_velocity),
                    "burst_score": round(min(1.0, total_txns / 5.0), 2),
                    "rolling_amount_sum": float(total_val),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="velocity",
                    score=velocity_score,
                    supporting_features=[
                        "transaction_velocity",
                        "burst_score",
                        "active_days_ratio",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} exhibited high velocity with {total_txns} transactions over {time_span_days:.1f} days ({daily_velocity:.1f} txns/day).",
                        f"Total velocity volume: ${total_val:,.2f}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
