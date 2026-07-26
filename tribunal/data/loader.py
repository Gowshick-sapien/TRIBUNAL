"""DataLoader module — Canonical data ingestion layer for TRIBUNAL."""

import logging
from pathlib import Path
from typing import List, Optional, Union
import pandas as pd

from tribunal.data.dataset_resolver import DatasetResolver, DatasetNotFoundError
from tribunal.models.account import Account
from tribunal.models.transaction import Transaction

logger = logging.getLogger("tribunal.data.loader")


class DataLoader:
    """Canonical data loader for TRIBUNAL.
    
    Serves as the single point of entry for loading transaction and account data.
    Prefers DatasetResolver for path resolution, supporting both direct file paths and directory candidates.
    """

    def __init__(self, dataset_dir: Union[str, Path] = "default"):
        self.dataset_ref = str(dataset_dir)
        self.resolver = DatasetResolver()

    def _resolve_transactions_path(self) -> Path:
        """Locate the best available transactions dataset file using DatasetResolver."""
        resolved = self.resolver.resolve(self.dataset_ref)
        if resolved.is_file:
            return resolved.resolved_path

        # If resolved path is a directory, search standard candidate files inside
        dataset_path = resolved.resolved_path
        parquet_path = dataset_path / "processed" / "transactions.parquet"
        if parquet_path.exists():
            return parquet_path

        for p in [
            dataset_path / "raw" / "LI-Small_Trans.csv",
            dataset_path / "LI-Small_Trans.csv",
            dataset_path / "raw" / "transactions.csv",
            dataset_path / "transactions.csv",
        ]:
            if p.exists():
                return p

        raise DatasetNotFoundError(
            dataset_ref=self.dataset_ref,
            message=f"No transaction dataset file found in '{dataset_path}'.",
            searched_locations=[str(dataset_path)],
        )

    def _resolve_accounts_path(self) -> Path:
        """Locate the best available accounts dataset file."""
        try:
            resolved = self.resolver.resolve(self.dataset_ref)
            dataset_path = resolved.resolved_path if not resolved.is_file else resolved.resolved_path.parent
        except Exception:
            dataset_path = Path("tribunal/datasets")

        parquet_path = dataset_path / "processed" / "accounts.parquet"
        if parquet_path.exists():
            return parquet_path

        for p in [
            dataset_path / "raw" / "LI-Small_accounts.csv",
            dataset_path / "LI-Small_accounts.csv",
            dataset_path / "raw" / "accounts.csv",
            dataset_path / "accounts.csv",
        ]:
            if p.exists():
                return p

        # Fallback to default raw directory
        fallback = Path("tribunal/datasets/LI-Small_accounts.csv")
        if fallback.exists():
            return fallback

        raise DatasetNotFoundError(
            dataset_ref=self.dataset_ref,
            message=f"No account dataset file found in '{dataset_path}'.",
            searched_locations=[str(dataset_path)],
        )

    def load_transactions(
        self,
        as_dataclasses: bool = False,
        limit: Optional[int] = None,
        account_id: Optional[str] = None,
        target_entities: Optional[List[str]] = None,
    ) -> Union[pd.DataFrame, List[Transaction]]:
        """Load transaction records into DataFrame or list of Transaction objects.
        
        Supports target-aware ingestion: when target_entities or account_id is specified,
        scans for matching target account transactions across pattern files and transaction logs.
        """
        targets = set()
        if account_id:
            targets.add(str(account_id).strip())
        if target_entities:
            for e in target_entities:
                if e:
                    s = str(e).strip()
                    targets.add(s)
                    if s.upper().startswith("ACC_"):
                        targets.add(s[4:])
                    elif s.upper().startswith("ACC"):
                        targets.add(s[3:])
                    elif s.upper().startswith("ACCOUNT_"):
                        targets.add(s[8:])

        file_path = self._resolve_transactions_path()
        logger.info(f"Loading transactions from {file_path} (targets={targets})")

        df = pd.DataFrame()

        if targets:
            # 1. Search pattern file LI-Small_Patterns.txt for instant target pattern matching
            dataset_dir = file_path.parent
            if dataset_dir.name == "raw":
                dataset_dir = dataset_dir.parent
            pattern_file = dataset_dir / "LI-Small_Patterns.txt"
            if not pattern_file.exists():
                pattern_file = Path("tribunal/datasets/LI-Small_Patterns.txt")

            pattern_df = pd.DataFrame()
            if pattern_file.exists():
                try:
                    lines = []
                    with open(pattern_file, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            if line.startswith("BEGIN") or line.startswith("END") or not line.strip():
                                continue
                            parts = line.strip().split(",")
                            if len(parts) >= 11:
                                from_acc = parts[2].strip()
                                to_acc = parts[4].strip()
                                if any(t in from_acc or t in to_acc for t in targets):
                                    lines.append(parts[:11])
                    if lines:
                        pattern_df = pd.DataFrame(lines, columns=[
                            "Timestamp", "From Bank", "Account", "To Bank", "Account.1",
                            "Amount Received", "Receiving Currency", "Amount Paid",
                            "Payment Currency", "Payment Format", "Is Laundering"
                        ])
                        pattern_df["Amount Received"] = pd.to_numeric(pattern_df["Amount Received"], errors="coerce")
                        pattern_df["Amount Paid"] = pd.to_numeric(pattern_df["Amount Paid"], errors="coerce")
                        pattern_df["Is Laundering"] = pd.to_numeric(pattern_df["Is Laundering"], errors="coerce").fillna(0).astype(int)
                except Exception as err:
                    logger.warning(f"Failed to scan pattern file: {err}")

            # 2. Search primary transaction file (parquet or CSV)
            file_df = pd.DataFrame()
            if file_path.suffix == ".parquet":
                full_df = pd.read_parquet(file_path)
                from_col = "Account" if "Account" in full_df.columns else ("from_account" if "from_account" in full_df.columns else None)
                to_col = "Account.1" if "Account.1" in full_df.columns else ("to_account" if "to_account" in full_df.columns else None)
                if from_col and to_col:
                    file_df = full_df[
                        full_df[from_col].astype(str).isin(targets) | full_df[to_col].astype(str).isin(targets)
                    ]
            else:
                chunk_matches = []
                try:
                    for chunk in pd.read_csv(file_path, chunksize=50000):
                        from_col = "Account" if "Account" in chunk.columns else ("from_account" if "from_account" in chunk.columns else ("From Account" if "From Account" in chunk.columns else None))
                        to_col = "Account.1" if "Account.1" in chunk.columns else ("to_account" if "to_account" in chunk.columns else ("To Account" if "To Account" in chunk.columns else None))
                        if from_col and to_col:
                            matched = chunk[
                                chunk[from_col].astype(str).isin(targets) | chunk[to_col].astype(str).isin(targets)
                            ]
                            if not matched.empty:
                                chunk_matches.append(matched)
                                if sum(len(c) for c in chunk_matches) >= 500:
                                    break
                except Exception as err:
                    logger.warning(f"Error chunk-reading transaction CSV: {err}")
                if chunk_matches:
                    file_df = pd.concat(chunk_matches, ignore_index=True)

            # Combine pattern matches and file matches
            if not pattern_df.empty and not file_df.empty:
                df = pd.concat([pattern_df, file_df], ignore_index=True).drop_duplicates()
            elif not pattern_df.empty:
                df = pattern_df
            elif not file_df.empty:
                df = file_df
            else:
                df = pd.DataFrame()
        else:
            if file_path.suffix == ".parquet":
                df = pd.read_parquet(file_path)
                if limit:
                    df = df.head(limit)
            else:
                df = pd.read_csv(file_path, nrows=limit or 500)

        if df.empty:
            return pd.DataFrame() if not as_dataclasses else []

        if "Account.1" not in df.columns and "To Account" in df.columns:
            df = df.rename(columns={
                "From Account": "Account",
                "To Account": "Account.1"
            })

        rename_map = {
            "Timestamp": "timestamp",
            "From Bank": "from_bank",
            "Account": "from_account",
            "To Bank": "to_bank",
            "Account.1": "to_account",
            "Amount Received": "amount_received",
            "Receiving Currency": "receiving_currency",
            "Amount Paid": "amount_paid",
            "Payment Currency": "payment_currency",
            "Payment Format": "payment_format",
            "Is Laundering": "is_laundering",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        if "timestamp" in df.columns and df["timestamp"].dtype == "object":
            df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M", errors="coerce")

        if limit and len(df) > limit:
            df = df.head(limit)

        if not as_dataclasses:
            return df

        transactions = []
        for idx, row in df.iterrows():
            txn = Transaction(
                timestamp=row["timestamp"],
                from_bank=str(row["from_bank"]),
                from_account=str(row["from_account"]),
                to_bank=str(row["to_bank"]),
                to_account=str(row["to_account"]),
                amount_received=float(row["amount_received"]),
                receiving_currency=str(row["receiving_currency"]),
                amount_paid=float(row["amount_paid"]),
                payment_currency=str(row["payment_currency"]),
                payment_format=str(row["payment_format"]),
                is_laundering=int(row.get("is_laundering", 0)),
                transaction_id=str(row.get("transaction_id", f"txn_{idx}")),
            )
            transactions.append(txn)
        return transactions

    def load_accounts(
        self,
        as_dataclasses: bool = False,
        limit: Optional[int] = None,
        account_id: Optional[str] = None,
    ) -> Union[pd.DataFrame, List[Account]]:
        """Load account metadata into DataFrame or list of Account objects."""
        file_path = self._resolve_accounts_path()
        logger.info(f"Loading accounts from {file_path}")

        if file_path.suffix == ".parquet":
            df = pd.read_parquet(file_path)
            if limit:
                df = df.head(limit)
        else:
            df = pd.read_csv(file_path, nrows=limit)

        rename_map = {
            "Bank Name": "bank_name",
            "Bank ID": "bank_id",
            "Account Number": "account_number",
            "Entity ID": "entity_id",
            "Entity Name": "entity_name",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        if account_id:
            df = df[df["account_number"] == account_id].copy()

        if not as_dataclasses:
            return df

        accounts = []
        for _, row in df.iterrows():
            acc = Account(
                bank_name=str(row["bank_name"]),
                bank_id=str(row["bank_id"]),
                account_number=str(row["account_number"]),
                entity_id=str(row["entity_id"]),
                entity_name=str(row["entity_name"]),
            )
            accounts.append(acc)
        return accounts

    def load_feature_store(
        self,
        account_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """Load persisted Feature Store DataFrame."""
        try:
            resolved = self.resolver.resolve(self.dataset_ref)
            dataset_path = resolved.resolved_path if not resolved.is_file else resolved.resolved_path.parent
        except Exception:
            dataset_path = Path("tribunal/datasets")

        fs_path = dataset_path / "processed" / "feature_store.parquet"
        if not fs_path.exists():
            fs_path = Path("tribunal/datasets/processed/feature_store.parquet")

        if not fs_path.exists():
            raise FileNotFoundError(
                f"Feature store not found at {fs_path}. Run FeatureStoreBuilder.build() first."
            )
        logger.info(f"Loading feature store from {fs_path}")
        df = pd.read_parquet(fs_path)

        if account_id:
            df = df[df["account_id"] == account_id].copy()
        if limit:
            df = df.head(limit)
        return df
