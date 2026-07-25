"""Currency Change Detector module — Detects unexpected currency switches."""

from __future__ import annotations

import logging
import pandas as pd
from tribunal.experts.behaviour.pattern_finding import PatternFinding

logger = logging.getLogger("tribunal.experts.behaviour.currency")


class CurrencyChangeDetector:
    """Detects unexpected currency usage deviating from an account's historical baseline currency."""

    detector_name: str = "CurrencyChangeDetector"
    detector_version: str = "1.0"

    def detect(self, transactions: pd.DataFrame) -> list[PatternFinding]:
        """Analyze transactions for unexpected currency switches."""
        if transactions is None or transactions.empty:
            return []

        findings: list[PatternFinding] = []
        df = transactions.copy()

        account_col = "from_account" if "from_account" in df.columns else ("Account" if "Account" in df.columns else None)
        curr_col = "receiving_currency" if "receiving_currency" in df.columns else ("Receiving Currency" if "Receiving Currency" in df.columns else None)
        txn_id_col = "transaction_id" if "transaction_id" in df.columns else None

        if not account_col or not curr_col:
            return []

        grouped = df.groupby(account_col)

        for account_id, group in grouped:
            pref_curr = str(group["preferred_currency"].iloc[0]).upper() if "preferred_currency" in group.columns else None
            used_currencies = set(group[curr_col].dropna().astype(str).str.upper())

            # Detect if currencies outside preferred_currency exist or multiple unusual currencies are used
            if pref_curr and any(c != pref_curr for c in used_currencies):
                unexpected = [c for c in used_currencies if c != pref_curr]
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []

                supporting_metrics = {
                    "unique_currency_count": float(len(used_currencies)),
                    "currency_switch_frequency": float(len(unexpected)),
                }

                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="currency_change",
                    score=0.80,
                    supporting_features=[
                        "preferred_currency",
                        "currency_distribution",
                        "currency_switch_frequency",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} transacted in unexpected currency {unexpected} (Preferred: {pref_curr}).",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)
            elif len(used_currencies) > 2:
                txn_ids = group[txn_id_col].astype(str).tolist() if txn_id_col else []
                supporting_metrics = {
                    "unique_currency_count": float(len(used_currencies)),
                    "currency_switch_frequency": float(len(used_currencies) - 1),
                }
                provenance = {
                    "detectors": [self.detector_name],
                    "detector_version": self.detector_version,
                    "transaction_ids": txn_ids,
                    "feature_store_rows": list(group.index.astype(int)),
                }

                finding = PatternFinding(
                    pattern_name="currency_change",
                    score=0.75,
                    supporting_features=[
                        "preferred_currency",
                        "currency_distribution",
                        "currency_switch_frequency",
                    ],
                    supporting_metrics=supporting_metrics,
                    provenance=provenance,
                    detector_name=self.detector_name,
                    detector_version=self.detector_version,
                    affected_accounts=[str(account_id)],
                    evidence_details=[
                        f"Account {account_id} executed transactions across {len(used_currencies)} distinct currencies: {sorted(used_currencies)}.",
                    ],
                    transaction_ids=txn_ids,
                )
                findings.append(finding)

        return findings
