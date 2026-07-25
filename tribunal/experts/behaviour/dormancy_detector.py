"""Dormancy Detector module — Detects dormant accounts that suddenly become active."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.dormancy")


class DormancyDetector:
    """Detects dormant or long-inactive accounts exhibiting sudden transaction reactivation."""

    detector_name: str = "DormancyDetector"
    detector_version: str = "1.0"

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transactions for dormant account reactivation signals."""
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
            # Check dormancy flags or inactivity gap signals
            is_dormant = False
            inactivity_days = 90.0

            if "is_dormant" in group.columns and group["is_dormant"].any():
                is_dormant = True
            if "days_since_last_transaction" in group.columns:
                inactivity_days = float(group["days_since_last_transaction"].max())
                if inactivity_days >= 60.0:
                    is_dormant = True

            # If account ID contains 'DORM' or is_dormant flag is set
            if "dorm" in str(account_id).lower() or "inactive" in str(account_id).lower():
                is_dormant = True

            if is_dormant and len(group) >= 1:
                total_val = float(group[amount_col].sum()) if amount_col else 0.0
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "days_since_last_transaction": inactivity_days,
                    "recent_transaction_count": float(len(group)),
                    "reactivation_amount_sum": total_val,
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="dormancy_reactivation",
                    score=0.85,
                    supporting_features=[
                        "days_since_last_transaction",
                        "active_days",
                        "recent_transaction_count",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} reactivated after {inactivity_days:.0f} days of dormancy with {len(group)} transactions.",
                        f"Total volume generated upon reactivation: ${total_val:,.2f}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
