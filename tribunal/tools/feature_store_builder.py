"""Feature Store Builder for TRIBUNAL (Stage 2.2).

Transforms raw transactions and the Transaction Network into a reusable,
persistent collection of account-level AML analytical features (feature_store.parquet).
"""

import json
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import networkx as nx
import numpy as np
import pandas as pd

from tribunal.data.loader import DataLoader

logger = logging.getLogger("tribunal.tools.feature_store_builder")


class FeatureStoreBuilder:
    """Computes, validates, profiles, and persists account-level AML features.
    
    Generates feature vectors across 6 categories:
    1. Financial Features (amounts, rolling sums, threshold proximity)
    2. Behavioural Features (active days, velocity, deviation, preferred formats)
    3. Network Features (fan-in, fan-out, degree, neighbourhood size)
    4. Temporal Features (weekend ratio, burst counts)
    5. Statistical Features (z-score, IQR outlier score)
    6. Rule-Ready Features (sub-threshold counts, structuring score)
    """

    REPORTING_THRESHOLD = 10_000.0
    STRUCTURING_MARGIN = 1_000.0  # $9,000 to $9,999

    def __init__(self, dataset_dir: Union[str, Path] = "datasets"):
        self.dataset_dir = Path(dataset_dir)
        self.processed_dir = self.dataset_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.loader = DataLoader(self.dataset_dir)
        self.feature_df: Optional[pd.DataFrame] = None

    def compute_financial_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute financial amount, quantile, and threshold proximity features per account."""
        logger.info("Computing financial features...")
        
        # Prepare working DataFrame
        from_col = "from_account" if "from_account" in df.columns else "Account"
        amt_col = "amount_paid" if "amount_paid" in df.columns else "Amount Paid"
        ts_col = "timestamp" if "timestamp" in df.columns else "Timestamp"

        # Outgoing financial aggregates
        outgoing_stats = df.groupby(from_col)[amt_col].agg(
            total_outgoing_txns="count",
            total_outgoing_amount="sum",
            average_amount="mean",
            median_amount="median",
            max_amount="max",
            min_amount="min",
            std_amount="std",
        ).reset_index().rename(columns={from_col: "account_id"})

        # Vectorized percentiles for high performance
        p90 = df.groupby(from_col)[amt_col].quantile(0.90).reset_index().rename(columns={from_col: "account_id", amt_col: "amount_p90"})
        p95 = df.groupby(from_col)[amt_col].quantile(0.95).reset_index().rename(columns={from_col: "account_id", amt_col: "amount_p95"})

        outgoing_stats = pd.merge(outgoing_stats, p90, on="account_id", how="left")
        outgoing_stats = pd.merge(outgoing_stats, p95, on="account_id", how="left")

        outgoing_stats["std_amount"] = outgoing_stats["std_amount"].fillna(0.0)

        # Incoming financial aggregates
        to_col = "to_account" if "to_account" in df.columns else "Account.1"
        rec_amt_col = "amount_received" if "amount_received" in df.columns else "Amount Received"
        incoming_stats = df.groupby(to_col)[rec_amt_col].agg(
            total_incoming_txns="count",
            total_incoming_amount="sum",
        ).reset_index().rename(columns={to_col: "account_id"})

        # Rolling 7-day and 30-day features
        max_ts = df[ts_col].max()
        cutoff_7d = max_ts - pd.Timedelta(days=7)
        
        df_7d = df[df[ts_col] >= cutoff_7d]
        rolling_7d = df_7d.groupby(from_col)[amt_col].agg(
            rolling_sum_7d="sum",
            rolling_count_7d="count",
        ).reset_index().rename(columns={from_col: "account_id"})

        # Merge financial features
        financial_df = pd.merge(outgoing_stats, incoming_stats, on="account_id", how="outer")
        financial_df = pd.merge(financial_df, rolling_7d, on="account_id", how="left")

        financial_df["total_outgoing_txns"] = financial_df["total_outgoing_txns"].fillna(0).astype(int)
        financial_df["total_incoming_txns"] = financial_df["total_incoming_txns"].fillna(0).astype(int)
        financial_df["total_outgoing_amount"] = financial_df["total_outgoing_amount"].fillna(0.0)
        financial_df["total_incoming_amount"] = financial_df["total_incoming_amount"].fillna(0.0)
        financial_df["average_amount"] = financial_df["average_amount"].fillna(0.0)
        financial_df["median_amount"] = financial_df["median_amount"].fillna(0.0)
        financial_df["max_amount"] = financial_df["max_amount"].fillna(0.0)
        financial_df["min_amount"] = financial_df["min_amount"].fillna(0.0)
        financial_df["std_amount"] = financial_df["std_amount"].fillna(0.0)
        financial_df["amount_p90"] = financial_df["amount_p90"].fillna(0.0)
        financial_df["amount_p95"] = financial_df["amount_p95"].fillna(0.0)
        financial_df["rolling_sum_7d"] = financial_df["rolling_sum_7d"].fillna(0.0)
        financial_df["rolling_count_7d"] = financial_df["rolling_count_7d"].fillna(0).astype(int)

        # Fill 30d rolling (equals full dataset span volume)
        financial_df["rolling_sum_30d"] = financial_df["total_outgoing_amount"]
        financial_df["rolling_count_30d"] = financial_df["total_outgoing_txns"]

        # Sub-threshold / Threshold proximity features ($9,000 to $9,999)
        lower_band = self.REPORTING_THRESHOLD - self.STRUCTURING_MARGIN
        sub_mask = (df[amt_col] >= lower_band) & (df[amt_col] < self.REPORTING_THRESHOLD)
        sub_df = df[sub_mask]
        
        sub_counts = sub_df.groupby(from_col)[amt_col].count().reset_index()
        sub_counts.columns = ["account_id", "sub_threshold_count"]

        financial_df = pd.merge(financial_df, sub_counts, on="account_id", how="left")
        financial_df["sub_threshold_count"] = financial_df["sub_threshold_count"].fillna(0).astype(int)
        
        # Threshold proximity ratio
        financial_df["threshold_proximity"] = np.where(
            financial_df["total_outgoing_txns"] > 0,
            financial_df["sub_threshold_count"] / financial_df["total_outgoing_txns"],
            0.0
        )

        return financial_df

    def compute_behaviour_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute behavioural velocity, active days, currency/format preferences."""
        logger.info("Computing behavioural features...")

        from_col = "from_account" if "from_account" in df.columns else "Account"
        to_col = "to_account" if "to_account" in df.columns else "Account.1"
        ts_col = "timestamp" if "timestamp" in df.columns else "Timestamp"
        amt_col = "amount_paid" if "amount_paid" in df.columns else "Amount Paid"
        curr_col = "payment_currency" if "payment_currency" in df.columns else "Payment Currency"
        fmt_col = "payment_format" if "payment_format" in df.columns else "Payment Format"

        max_ts = df[ts_col].max()
        min_ts = df[ts_col].min()
        span_days = max(1.0, (max_ts - min_ts).total_seconds() / 86400.0)

        # Date extract for active days
        df_copy = df.copy()
        df_copy["txn_date"] = df_copy[ts_col].dt.date

        # Active days per sender
        active_days_sender = df_copy.groupby(from_col)["txn_date"].nunique().reset_index()
        active_days_sender.columns = ["account_id", "active_days"]

        # Last transaction timestamp per sender
        last_ts_sender = df_copy.groupby(from_col)[ts_col].max().reset_index()
        last_ts_sender.columns = ["account_id", "last_timestamp"]
        last_ts_sender["days_since_last_transaction"] = (max_ts - last_ts_sender["last_timestamp"]).dt.total_seconds() / 86400.0

        # Preferred payment format and currency (most common mode)
        pref_curr = df_copy.groupby([from_col, curr_col]).size().reset_index(name="count")
        pref_curr = pref_curr.sort_values(by=["count"], ascending=False).drop_duplicates(subset=[from_col])
        pref_curr = pref_curr[[from_col, curr_col]].rename(columns={from_col: "account_id", curr_col: "preferred_currency"})

        pref_fmt = df_copy.groupby([from_col, fmt_col]).size().reset_index(name="count")
        pref_fmt = pref_fmt.sort_values(by=["count"], ascending=False).drop_duplicates(subset=[from_col])
        pref_fmt = pref_fmt[[from_col, fmt_col]].rename(columns={from_col: "account_id", fmt_col: "preferred_payment_format"})

        # Currency changes count
        curr_count = df_copy.groupby(from_col)[curr_col].nunique().reset_index()
        curr_count.columns = ["account_id", "currency_changes_count"]

        # Counterparty stability (unique receivers / outgoing count)
        cp_count = df_copy.groupby(from_col)[to_col].nunique().reset_index()
        cp_count.columns = ["account_id", "unique_receivers_count"]

        # Merge behavioural features
        beh_df = pd.merge(active_days_sender, last_ts_sender[["account_id", "days_since_last_transaction"]], on="account_id", how="outer")
        beh_df = pd.merge(beh_df, pref_curr, on="account_id", how="left")
        beh_df = pd.merge(beh_df, pref_fmt, on="account_id", how="left")
        beh_df = pd.merge(beh_df, curr_count, on="account_id", how="left")
        beh_df = pd.merge(beh_df, cp_count, on="account_id", how="left")

        beh_df["active_days"] = beh_df["active_days"].fillna(1).astype(int)
        beh_df["days_since_last_transaction"] = beh_df["days_since_last_transaction"].fillna(span_days)
        beh_df["preferred_currency"] = beh_df["preferred_currency"].fillna("US Dollar")
        beh_df["preferred_payment_format"] = beh_df["preferred_payment_format"].fillna("ACH")
        beh_df["currency_changes_count"] = beh_df["currency_changes_count"].fillna(1).astype(int)
        beh_df["unique_receivers_count"] = beh_df["unique_receivers_count"].fillna(0).astype(int)

        # Baseline volume & velocity metrics
        beh_df["average_daily_volume"] = beh_df["active_days"].apply(lambda d: d / span_days)
        beh_df["weekly_frequency"] = (beh_df["active_days"] / span_days) * 7.0
        beh_df["monthly_frequency"] = (beh_df["active_days"] / span_days) * 30.0

        return beh_df

    def compute_network_features(self, graph: Optional[nx.MultiDiGraph] = None) -> pd.DataFrame:
        """Compute network features from persisted MultiDiGraph."""
        logger.info("Computing network features from Transaction Network...")

        if graph is None:
            gpickle_path = self.processed_dir / "transaction_network.gpickle"
            if gpickle_path.exists():
                with open(gpickle_path, "rb") as f:
                    graph = pickle.load(f)
            else:
                logger.warning("No persisted MultiDiGraph found. Returning empty network features.")
                return pd.DataFrame(columns=["account_id", "fan_in", "fan_out", "account_degree", "incoming_outgoing_ratio", "repeated_counterparties_count", "neighbourhood_size_2hop"])

        network_rows = []
        for node in graph.nodes():
            in_deg = graph.in_degree(node)
            out_deg = graph.out_degree(node)
            unique_in = len(list(graph.predecessors(node)))
            unique_out = len(list(graph.successors(node)))
            tot_deg = in_deg + out_deg
            io_ratio = float(in_deg) / (out_deg + 1e-5)

            # Node stored attributes
            node_data = graph.nodes[node]
            rep_cp = node_data.get("repeated_counterparties_count", 0)

            network_rows.append({
                "account_id": str(node),
                "fan_in": int(in_deg),
                "fan_out": int(out_deg),
                "account_degree": int(tot_deg),
                "unique_senders": int(unique_in),
                "unique_receivers": int(unique_out),
                "incoming_outgoing_ratio": float(io_ratio),
                "repeated_counterparties": int(rep_cp),
            })

        return pd.DataFrame(network_rows)

    def compute_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute timestamp temporal features (weekend ratio, burst counts)."""
        logger.info("Computing temporal features...")

        from_col = "from_account" if "from_account" in df.columns else "Account"
        ts_col = "timestamp" if "timestamp" in df.columns else "Timestamp"

        df_temp = df.copy()
        df_temp["is_weekend"] = df_temp[ts_col].dt.weekday >= 5
        df_temp["hour"] = df_temp[ts_col].dt.hour

        # Weekend ratio
        weekend_stats = df_temp.groupby(from_col)["is_weekend"].agg(
            weekend_txns="sum",
            total_txns="count"
        ).reset_index().rename(columns={from_col: "account_id"})

        weekend_stats["weekend_ratio"] = np.where(
            weekend_stats["total_txns"] > 0,
            weekend_stats["weekend_txns"] / weekend_stats["total_txns"],
            0.0
        )

        # Hour of day mode
        hour_mode = df_temp.groupby([from_col, "hour"]).size().reset_index(name="count")
        hour_mode = hour_mode.sort_values(by=["count"], ascending=False).drop_duplicates(subset=[from_col])
        hour_mode = hour_mode[[from_col, "hour"]].rename(columns={from_col: "account_id", "hour": "hour_of_day_mode"})

        # Rapid successive txns (txns within 1 hour of prior txn)
        df_temp = df_temp.sort_values(by=[from_col, ts_col])
        df_temp["prev_ts"] = df_temp.groupby(from_col)[ts_col].shift(1)
        df_temp["diff_hours"] = (df_temp[ts_col] - df_temp["prev_ts"]).dt.total_seconds() / 3600.0
        df_temp["is_rapid"] = df_temp["diff_hours"] <= 1.0

        rapid_stats = df_temp.groupby(from_col)["is_rapid"].sum().reset_index()
        rapid_stats.columns = ["account_id", "rapid_successive_txns_count"]

        # Merge temporal
        temp_df = pd.merge(weekend_stats[["account_id", "weekend_ratio"]], hour_mode, on="account_id", how="outer")
        temp_df = pd.merge(temp_df, rapid_stats, on="account_id", how="left")

        temp_df["weekend_ratio"] = temp_df["weekend_ratio"].fillna(0.0)
        temp_df["hour_of_day_mode"] = temp_df["hour_of_day_mode"].fillna(12).astype(int)
        temp_df["rapid_successive_txns_count"] = temp_df["rapid_successive_txns_count"].fillna(0).astype(int)

        return temp_df

    def compute_statistical_features(self, financial_df: pd.DataFrame) -> pd.DataFrame:
        """Compute statistical z-score and IQR outlier scores relative to global amounts."""
        logger.info("Computing statistical outlier features...")

        stats_df = financial_df[["account_id", "average_amount", "max_amount"]].copy()

        global_mean = stats_df["average_amount"].mean()
        global_std = stats_df["average_amount"].std()
        global_std = global_std if global_std > 0 else 1.0

        stats_df["z_score_amount"] = (stats_df["average_amount"] - global_mean) / global_std

        # IQR Outlier score
        q25 = stats_df["average_amount"].quantile(0.25)
        q75 = stats_df["average_amount"].quantile(0.75)
        iqr = q75 - q25
        iqr = iqr if iqr > 0 else 1.0

        stats_df["iqr_outlier_score"] = np.maximum(0.0, (stats_df["average_amount"] - (q75 + 1.5 * iqr)) / iqr)

        return stats_df[["account_id", "z_score_amount", "iqr_outlier_score"]]

    def compute_rule_ready_features(self, financial_df: pd.DataFrame, temporal_df: pd.DataFrame) -> pd.DataFrame:
        """Compute AML rule-ready indicators (structuring_score, rapid_cashout_indicator, high_frequency_deposit_indicator)."""
        logger.info("Computing AML rule-ready indicators...")

        merged = pd.merge(financial_df[["account_id", "sub_threshold_count", "threshold_proximity"]], 
                          temporal_df[["account_id", "rapid_successive_txns_count"]], on="account_id", how="left")

        merged["structuring_score"] = np.where(
            merged["sub_threshold_count"] >= 2,
            np.minimum(1.0, merged["threshold_proximity"] * 1.5),
            0.0
        )

        merged["high_frequency_deposit_indicator"] = (merged["sub_threshold_count"] >= 3).astype(int)
        merged["rapid_cashout_indicator"] = (merged["rapid_successive_txns_count"] >= 5).astype(int)

        return merged[["account_id", "structuring_score", "high_frequency_deposit_indicator", "rapid_cashout_indicator"]]

    def build(
        self,
        transactions_df: Optional[pd.DataFrame] = None,
        graph: Optional[nx.MultiDiGraph] = None,
    ) -> pd.DataFrame:
        """Execute full feature store build pipeline."""
        if transactions_df is None:
            logger.info("Loading transactions dataset for Feature Store...")
            transactions_df = self.loader.load_transactions(as_dataclasses=False)

        # 1. Compute Feature Categories
        fin_df = self.compute_financial_features(transactions_df)
        beh_df = self.compute_behaviour_features(transactions_df)
        net_df = self.compute_network_features(graph)
        temp_df = self.compute_temporal_features(transactions_df)
        stat_df = self.compute_statistical_features(fin_df)
        rule_df = self.compute_rule_ready_features(fin_df, temp_df)

        # 2. Merge Feature Tables
        logger.info("Merging feature tables into unified Feature Store...")
        
        # Outer join to ensure every active account is included
        feature_store = pd.merge(fin_df, beh_df, on="account_id", how="outer")
        feature_store = pd.merge(feature_store, net_df, on="account_id", how="left")
        feature_store = pd.merge(feature_store, temp_df, on="account_id", how="left")
        feature_store = pd.merge(feature_store, stat_df, on="account_id", how="left")
        feature_store = pd.merge(feature_store, rule_df, on="account_id", how="left")

        # 3. Clean up NAs
        feature_store["fan_in"] = feature_store["fan_in"].fillna(0).astype(int)
        feature_store["fan_out"] = feature_store["fan_out"].fillna(0).astype(int)
        feature_store["account_degree"] = feature_store["account_degree"].fillna(0).astype(int)
        feature_store["unique_senders"] = feature_store["unique_senders"].fillna(0).astype(int)
        feature_store["unique_receivers"] = feature_store["unique_receivers"].fillna(0).astype(int)
        feature_store["incoming_outgoing_ratio"] = feature_store["incoming_outgoing_ratio"].fillna(0.0)
        feature_store["repeated_counterparties"] = feature_store["repeated_counterparties"].fillna(0).astype(int)
        feature_store["structuring_score"] = feature_store["structuring_score"].fillna(0.0)
        feature_store["z_score_amount"] = feature_store["z_score_amount"].fillna(0.0)
        feature_store["iqr_outlier_score"] = feature_store["iqr_outlier_score"].fillna(0.0)

        # Total transaction count per account
        feature_store["transaction_count"] = feature_store["total_outgoing_txns"] + feature_store["total_incoming_txns"]

        # Behavior deviation score default calculation
        feature_store["behaviour_deviation_score"] = np.where(
            feature_store["average_daily_volume"] > 0,
            np.minimum(5.0, feature_store["rolling_sum_7d"] / (feature_store["average_daily_volume"] * 7.0 + 1e-5)),
            1.0
        )

        self.feature_df = feature_store
        logger.info(f"Feature Store build complete: {len(feature_store):,} accounts, {len(feature_store.columns)} features.")
        return feature_store

    def save(self, path: Optional[Union[str, Path]] = None) -> Path:
        """Save constructed Feature Store to Parquet."""
        if self.feature_df is None:
            raise ValueError("Feature Store has not been built yet. Call build() first.")

        target_path = Path(path) if path else self.processed_dir / "feature_store.parquet"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving Feature Store to {target_path}...")
        self.feature_df.to_parquet(target_path, index=False, engine="pyarrow")
        logger.info(f"Successfully saved {target_path} ({target_path.stat().st_size / (1024*1024):.2f} MB)")
        return target_path

    def load(self, path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """Load persisted Feature Store Parquet from disk."""
        target_path = Path(path) if path else self.processed_dir / "feature_store.parquet"
        if not target_path.exists():
            raise FileNotFoundError(f"Feature store file not found at {target_path}")

        logger.info(f"Loading Feature Store from {target_path}...")
        self.feature_df = pd.read_parquet(target_path)
        logger.info(f"Loaded Feature Store: {len(self.feature_df):,} accounts.")
        return self.feature_df

    def validate(self) -> Dict[str, Any]:
        """Validate Feature Store completeness and data types."""
        if self.feature_df is None:
            raise ValueError("Feature Store has not been built or loaded yet.")

        logger.info("Validating Feature Store Parquet dataset...")

        report: Dict[str, Any] = {
            "account_count": len(self.feature_df),
            "feature_count": len(self.feature_df.columns),
            "checks": {},
            "issues": [],
            "status": "PASSED"
        }

        # Check 1: Account ID non-null and unique
        null_accs = self.feature_df["account_id"].isna().sum()
        dups = self.feature_df["account_id"].duplicated().sum()
        report["checks"]["account_id_validity"] = {
            "passed": bool(null_accs == 0 and dups == 0),
            "null_count": int(null_accs),
            "duplicate_count": int(dups)
        }

        # Check 2: No missing critical numerical values
        critical_cols = ["transaction_count", "average_amount", "rolling_sum_7d", "fan_in", "fan_out", "structuring_score"]
        missing_critical = {c: int(self.feature_df[c].isna().sum()) for c in critical_cols if c in self.feature_df.columns}
        has_missing = any(v > 0 for v in missing_critical.values())
        report["checks"]["no_missing_critical_features"] = {
            "passed": not has_missing,
            "missing_counts": missing_critical
        }

        # Check 3: Types
        numeric_cols = self.feature_df.select_dtypes(include=[np.number]).columns.tolist()
        report["checks"]["numeric_features_typed"] = {
            "passed": len(numeric_cols) > 20,
            "numeric_feature_count": len(numeric_cols)
        }

        all_passed = all(c["passed"] for c in report["checks"].values())
        report["status"] = "PASSED" if all_passed else "FAILED_WITH_ISSUES"

        output_file = self.processed_dir / "feature_validation_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Feature Validation Report saved to {output_file}")
        return report

    def get_feature_profile(self) -> Dict[str, Any]:
        """Generate summary statistics for feature_store_profile.json."""
        if self.feature_df is None:
            raise ValueError("Feature Store has not been built or loaded yet.")

        logger.info("Computing Feature Store Profile Statistics...")

        df = self.feature_df

        profile = {
            "accounts_processed": len(df),
            "feature_count": len(df.columns),
            "feature_names": list(df.columns),
            "average_transactions_per_account": float(df["transaction_count"].mean()),
            "average_fan_in": float(df["fan_in"].mean()),
            "average_fan_out": float(df["fan_out"].mean()),
            "total_sub_threshold_transactions": int(df["sub_threshold_count"].sum()),
            "high_structuring_risk_accounts_count": int((df["structuring_score"] > 0.5).sum()),
            "preferred_formats_distribution": {k: int(v) for k, v in df["preferred_payment_format"].value_counts().items()},
            "preferred_currencies_distribution": {k: int(v) for k, v in df["preferred_currency"].value_counts().items()},
            "missing_values_total": int(df.isna().sum().sum())
        }

        output_file = self.processed_dir / "feature_store_profile.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

        logger.info(f"Feature Store Profile written to {output_file}")
        return profile
