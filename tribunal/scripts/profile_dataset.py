"""Dataset Profiling Module & Script for TRIBUNAL.

Performs empirical dataset profiling to understand dataset distribution, entity statistics,
payment channels, currencies, degree distributions, and transaction volume characteristics.

Outputs dataset_profile.json into datasets/processed/.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict
import pandas as pd
import numpy as np

from tribunal.data.loader import DataLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("profile_dataset")


class DatasetProfiler:
    """Profiles dataset characteristics for feature design and expert tuning."""

    def __init__(self, dataset_dir: str = "datasets"):
        self.loader = DataLoader(dataset_dir)
        self.output_dir = Path(dataset_dir) / "processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def profile(self) -> Dict[str, Any]:
        """Run dataset profiling suite."""
        logger.info("Loading dataset via DataLoader...")
        trans_df = self.loader.load_transactions(as_dataclasses=False)
        accounts_df = self.loader.load_accounts(as_dataclasses=False)

        logger.info("Computing profile statistics...")

        profile_report: Dict[str, Any] = {}

        # 1. Dataset Dimensions & General Info
        profile_report["general"] = {
            "total_transactions": len(trans_df),
            "total_accounts": len(accounts_df),
            "unique_sender_accounts": int(trans_df["from_account"].nunique()),
            "unique_receiver_accounts": int(trans_df["to_account"].nunique()),
            "unique_total_active_accounts": int(
                len(set(trans_df["from_account"]).union(set(trans_df["to_account"])))
            ),
            "laundering_transactions_count": int(trans_df["is_laundering"].sum()) if "is_laundering" in trans_df.columns else 0,
            "laundering_ratio_pct": float((trans_df["is_laundering"].mean() * 100)) if "is_laundering" in trans_df.columns else 0.0,
        }

        # 2. Timestamps Scope
        if "timestamp" in trans_df.columns:
            ts_series = pd.to_datetime(trans_df["timestamp"])
            min_ts = ts_series.min()
            max_ts = ts_series.max()
            profile_report["timestamps"] = {
                "start_date": str(min_ts),
                "end_date": str(max_ts),
                "span_days": float((max_ts - min_ts).total_seconds() / 86400.0),
            }

        # 3. Payment Formats Distribution
        if "payment_format" in trans_df.columns:
            fmt_counts = trans_df["payment_format"].value_counts()
            profile_report["payment_formats"] = {
                str(k): int(v) for k, v in fmt_counts.items()
            }

        # 4. Currencies Distribution
        if "payment_currency" in trans_df.columns:
            curr_counts = trans_df["payment_currency"].value_counts()
            profile_report["currencies"] = {
                str(k): int(v) for k, v in curr_counts.items()
            }

        # 5. Amount Distribution & Percentiles
        amounts = trans_df["amount_paid"].dropna().values if "amount_paid" in trans_df.columns else trans_df["amount_received"].dropna().values
        profile_report["amount_stats"] = {
            "min": float(np.min(amounts)),
            "max": float(np.max(amounts)),
            "mean": float(np.mean(amounts)),
            "median": float(np.median(amounts)),
            "std": float(np.std(amounts)),
            "p25": float(np.percentile(amounts, 25)),
            "p75": float(np.percentile(amounts, 75)),
            "p90": float(np.percentile(amounts, 90)),
            "p95": float(np.percentile(amounts, 95)),
            "p99": float(np.percentile(amounts, 99)),
            "sub_threshold_9k_10k_count": int(np.sum((amounts >= 9000) & (amounts < 10000))),
        }

        # 6. Top Banks
        if "from_bank" in trans_df.columns:
            from_banks = trans_df["from_bank"].value_counts().head(10)
            profile_report["top_originating_banks"] = {
                str(k): int(v) for k, v in from_banks.items()
            }

        # 7. Account Degree Statistics
        from_counts = trans_df["from_account"].value_counts()
        to_counts = trans_df["to_account"].value_counts()

        profile_report["degree_stats"] = {
            "max_fan_out_degree": int(from_counts.max()) if len(from_counts) > 0 else 0,
            "top_fan_out_accounts": [
                {"account": str(k), "out_degree": int(v)}
                for k, v in from_counts.head(5).items()
            ],
            "max_fan_in_degree": int(to_counts.max()) if len(to_counts) > 0 else 0,
            "top_fan_in_accounts": [
                {"account": str(k), "in_degree": int(v)}
                for k, v in to_counts.head(5).items()
            ],
        }

        # Save profile output
        output_file = self.output_dir / "dataset_profile.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(profile_report, f, indent=2)

        logger.info(f"Dataset profile written to: {output_file.resolve()}")
        return profile_report


if __name__ == "__main__":
    dataset_path = "datasets"
    if not Path(dataset_path).exists() and Path("tribunal/datasets").exists():
        dataset_path = "tribunal/datasets"
    profiler = DatasetProfiler(dataset_path)
    profiler.profile()
