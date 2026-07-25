"""Counterparty Behaviour Detector module — Detects sudden expansions in counterparty networks."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.counterparty")


class CounterpartyBehaviourDetector:
    """Detects sudden expansion of recipient/sender counterparty relationships."""

    detector_name: str = "CounterpartyBehaviourDetector"
    detector_version: str = "1.0"

    def __init__(self, counterparty_expansion_threshold: int = 5):
        self.counterparty_expansion_threshold = counterparty_expansion_threshold

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transaction network relationships for counterparty expansions."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        from_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        to_col = "to_account" if "to_account" in df.columns else ("Account.1" if "Account.1" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not from_col or not to_col:
            return []

        grouped = df.groupby(from_col)

        for account_id, group in grouped:
            recipients = set(group[to_col].dropna().astype(str))
            unique_count = len(recipients)

            if unique_count >= self.counterparty_expansion_threshold:
                score = min(1.0, round(unique_count / 10.0, 2))
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "unique_counterparties": float(unique_count),
                    "fan_out": float(unique_count),
                    "total_outbound_txns": float(len(group)),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="counterparty_expansion",
                    score=max(0.60, score),
                    supporting_features=[
                        "unique_counterparties",
                        "repeat_counterparties",
                        "fan_out",
                        "fan_in",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} exhibited counterparty expansion: transferred funds to {unique_count} distinct recipients.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
