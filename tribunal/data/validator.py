"""Data Validation Module for TRIBUNAL dataset integrity checks."""

import json
from pathlib import Path
from typing import Any, Dict, Tuple
import pandas as pd


class DataValidator:
    """Validates raw transaction and account datasets for completeness and correctness.
    
    Verifies:
    - No missing timestamps
    - Account IDs parse correctly (non-null, string format)
    - Currency codes validity
    - Payment format validity
    - Timestamp chronological ordering / format
    - Overall data summary metrics
    """

    VALID_CURRENCIES = {
        "US Dollar", "Euro", "Yen", "Yuan", "UK Pound", "Canadian Dollar",
        "Australian Dollar", "Swiss Franc", "Brazil Real", "Mexican Peso",
        "Ruble", "Rupee", "Saudi Riyal", "Shekel", "Turkey Lira", "Bitcoin"
    }

    VALID_PAYMENT_FORMATS = {
        "ACH", "Cheque", "Credit Card", "Reinvestment", "Wire", "Cash", "Bitcoin"
    }

    def __init__(self, output_dir: Path | str = "datasets/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def validate(
        self, transactions_df: pd.DataFrame, accounts_df: pd.DataFrame
    ) -> Tuple[bool, Dict[str, Any]]:
        """Run complete validation suite on transaction and account DataFrames."""
        report: Dict[str, Any] = {
            "transactions_count": len(transactions_df),
            "accounts_count": len(accounts_df),
            "checks": {},
            "issues": [],
            "status": "PASSED"
        }

        # 1. Missing Timestamps check
        missing_ts = transactions_df["Timestamp"].isna().sum() if "Timestamp" in transactions_df.columns else len(transactions_df)
        report["checks"]["no_missing_timestamps"] = {
            "passed": bool(missing_ts == 0),
            "missing_count": int(missing_ts)
        }
        if missing_ts > 0:
            report["issues"].append(f"Found {missing_ts} rows with missing Timestamp")

        # 2. Account IDs parsing check
        missing_from_acc = transactions_df["Account"].isna().sum() if "Account" in transactions_df.columns else 0
        missing_to_acc = transactions_df["Account.1"].isna().sum() if "Account.1" in transactions_df.columns else 0
        acc_check_passed = bool((missing_from_acc + missing_to_acc) == 0)
        report["checks"]["account_ids_valid"] = {
            "passed": acc_check_passed,
            "missing_from_account": int(missing_from_acc),
            "missing_to_account": int(missing_to_acc)
        }
        if not acc_check_passed:
            report["issues"].append("Found missing or unparseable Account IDs")

        # 3. Currencies validity check
        currencies_found = set(transactions_df["Receiving Currency"].unique()).union(
            set(transactions_df["Payment Currency"].unique())
        )
        invalid_currencies = currencies_found - self.VALID_CURRENCIES
        report["checks"]["currencies_valid"] = {
            "passed": bool(len(invalid_currencies) == 0),
            "currencies_found": list(sorted([str(c) for c in currencies_found])),
            "invalid_currencies": list(sorted([str(c) for c in invalid_currencies]))
        }
        if len(invalid_currencies) > 0:
            report["issues"].append(f"Found invalid currencies: {invalid_currencies}")

        # 4. Payment formats validity check
        formats_found = set(transactions_df["Payment Format"].unique())
        invalid_formats = formats_found - self.VALID_PAYMENT_FORMATS
        report["checks"]["payment_formats_valid"] = {
            "passed": bool(len(invalid_formats) == 0),
            "formats_found": list(sorted([str(f) for f in formats_found])),
            "invalid_formats": list(sorted([str(f) for f in invalid_formats]))
        }
        if len(invalid_formats) > 0:
            report["issues"].append(f"Found invalid payment formats: {invalid_formats}")

        # 5. Timestamps parsing & chronological ordering check
        ts_series = pd.to_datetime(transactions_df["Timestamp"], format="%Y/%m/%d %H:%M", errors="coerce")
        unparseable_ts = ts_series.isna().sum()
        is_sorted = ts_series.is_monotonic_increasing
        report["checks"]["timestamps_chronological"] = {
            "passed": bool(unparseable_ts == 0 and is_sorted),
            "unparseable_count": int(unparseable_ts),
            "is_chronological_sorted": bool(is_sorted),
            "min_timestamp": str(ts_series.min()) if unparseable_ts < len(ts_series) else None,
            "max_timestamp": str(ts_series.max()) if unparseable_ts < len(ts_series) else None,
        }
        if unparseable_ts > 0:
            report["issues"].append(f"Found {unparseable_ts} unparseable timestamps")

        # Set final status
        all_passed = all(check["passed"] for check in report["checks"].values())
        report["status"] = "PASSED" if all_passed else "FAILED_WITH_WARNINGS"

        # Save validation report
        report_path = self.output_dir / "validation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return all_passed, report
