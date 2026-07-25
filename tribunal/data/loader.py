"""DataLoader module — Canonical data ingestion layer for TRIBUNAL."""

import logging
from pathlib import Path
from typing import List, Optional, Union
import pandas as pd

from tribunal.models.account import Account
from tribunal.models.transaction import Transaction

logger = logging.getLogger("tribunal.data.loader")


class DataLoader:
    """Canonical data loader for TRIBUNAL.
    
    Serves as the single point of entry for loading transaction and account data.
    Prefers optimized Parquet formats from datasets/processed/, falling back to CSVs if required.
    """

    def __init__(self, dataset_dir: Union[str, Path] = "datasets"):
        self.dataset_dir = Path(dataset_dir)
        self.raw_dir = self.dataset_dir / "raw"
        self.processed_dir = self.dataset_dir / "processed"

    def _resolve_transactions_path(self) -> Path:
        """Locate the best available transactions dataset file."""
        parquet_path = self.processed_dir / "transactions.parquet"
        if parquet_path.exists():
            return parquet_path
        
        # Check raw or fallback dataset dir
        for p in [
            self.raw_dir / "LI-Small_Trans.csv",
            self.dataset_dir / "LI-Small_Trans.csv",
            self.raw_dir / "transactions.csv",
            self.dataset_dir / "transactions.csv",
        ]:
            if p.exists():
                return p

        raise FileNotFoundError(
            f"No transaction dataset found in {self.processed_dir}, {self.raw_dir}, or {self.dataset_dir}"
        )

    def _resolve_accounts_path(self) -> Path:
        """Locate the best available accounts dataset file."""
        parquet_path = self.processed_dir / "accounts.parquet"
        if parquet_path.exists():
            return parquet_path

        # Check raw or fallback dataset dir
        for p in [
            self.raw_dir / "LI-Small_accounts.csv",
            self.dataset_dir / "LI-Small_accounts.csv",
            self.raw_dir / "accounts.csv",
            self.dataset_dir / "accounts.csv",
        ]:
            if p.exists():
                return p

        raise FileNotFoundError(
            f"No account dataset found in {self.processed_dir}, {self.raw_dir}, or {self.dataset_dir}"
        )

    def load_transactions(
        self,
        as_dataclasses: bool = False,
        limit: Optional[int] = None,
        account_id: Optional[str] = None,
    ) -> Union[pd.DataFrame, List[Transaction]]:
        """Load transaction records into DataFrame or list of Transaction objects.
        
        Args:
            as_dataclasses: If True, returns List[Transaction], else pd.DataFrame
            limit: Maximum number of rows to load
            account_id: Optional account filter (from_account or to_account)
        """
        file_path = self._resolve_transactions_path()
        logger.info(f"Loading transactions from {file_path}")

        if file_path.suffix == ".parquet":
            df = pd.read_parquet(file_path)
            if limit:
                df = df.head(limit)
        else:
            # CSV Load with standardized column names
            col_names = [
                "Timestamp", "From Bank", "Account", "To Bank", "Account.1",
                "Amount Received", "Receiving Currency", "Amount Paid",
                "Payment Currency", "Payment Format", "Is Laundering"
            ]
            df = pd.read_csv(file_path, nrows=limit)
            if "Account.1" not in df.columns and "To Account" in df.columns:
                df = df.rename(columns={
                    "From Account": "Account",
                    "To Account": "Account.1"
                })

        # Standardize column naming for internal consistency
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

        # Ensure datetime parsing if needed
        if df["timestamp"].dtype == "object":
            df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M", errors="coerce")

        # Optional account filter
        if account_id:
            df = df[(df["from_account"] == account_id) | (df["to_account"] == account_id)].copy()

        if not as_dataclasses:
            return df

        # Convert to dataclasses
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
        """Load account metadata into DataFrame or list of Account objects.
        
        Args:
            as_dataclasses: If True, returns List[Account], else pd.DataFrame
            limit: Maximum number of rows to load
            account_id: Optional account number filter
        """
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
