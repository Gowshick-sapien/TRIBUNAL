"""Payment Pattern Detector module — Detects sudden shifts in payment format usage."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.payment")


class PaymentPatternDetector:
    """Detects sudden shifts in payment mechanisms (e.g., switching from ACH to Wire Transfer or Cash)."""

    detector_name: str = "PaymentPatternDetector"
    detector_version: str = "1.0"

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transactions for unexpected payment format shifts."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        fmt_col = "payment_format" if "payment_format" in df.columns else ("Payment Format" if "Payment Format" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col or not fmt_col:
            return []

        grouped = df.groupby(account_col)

        for account_id, group in grouped:
            pref_fmt = str(group["preferred_payment_format"].iloc[0]).lower() if "preferred_payment_format" in group.columns else None
            used_formats = set(group[fmt_col].dropna().astype(str).str.lower())

            if pref_fmt and any(f != pref_fmt for f in used_formats):
                unexpected = [f for f in used_formats if f != pref_fmt]
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "unique_format_count": float(len(used_formats)),
                    "format_switch_count": float(len(unexpected)),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="payment_pattern_change",
                    score=0.78,
                    supporting_features=[
                        "preferred_payment_format",
                        "payment_format_distribution",
                        "payment_frequency",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} switched to unexpected payment format(s) {unexpected} (Preferred: {pref_fmt}).",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)
            elif len(used_formats) >= 3:
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []
                supporting_metrics = {
                    "unique_format_count": float(len(used_formats)),
                }
                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="payment_pattern_change",
                    score=0.70,
                    supporting_features=[
                        "preferred_payment_format",
                        "payment_format_distribution",
                        "payment_frequency",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} executed transactions across {len(used_formats)} distinct payment formats: {sorted(used_formats)}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
