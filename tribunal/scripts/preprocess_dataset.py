"""Dataset Preprocessing Script for TRIBUNAL.

Converts raw CSV datasets (LI-Small_Trans.csv, LI-Small_accounts.csv) into optimized
Parquet format (transactions.parquet, accounts.parquet), runs data validation checks,
and generates validation_report.json.

Usage:
    python -m tribunal.scripts.preprocess_dataset
    OR
    python preprocess_dataset.py
"""

import os
import sys
import shutil
import json
import logging
from pathlib import Path
import pandas as pd

# Handle imports when running from root or module context
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tribunal.data.validator import DataValidator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("preprocess_dataset")


def run_preprocessing(dataset_dir: str = "datasets"):
    base_dir = Path(dataset_dir)
    raw_dir = base_dir / "raw"
    processed_dir = base_dir / "processed"

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. Organize Raw Datasets
    logger.info("Organizing raw dataset files into datasets/raw/...")

    trans_raw_candidates = [
        raw_dir / "LI-Small_Trans.csv",
        base_dir / "LI-Small_Trans.csv",
        raw_dir / "transactions.csv",
        base_dir / "transactions.csv",
    ]
    trans_csv_path = None
    for p in trans_raw_candidates:
        if p.exists():
            trans_csv_path = p
            break

    accounts_raw_candidates = [
        raw_dir / "LI-Small_accounts.csv",
        base_dir / "LI-Small_accounts.csv",
        raw_dir / "accounts.csv",
        base_dir / "accounts.csv",
    ]
    accounts_csv_path = None
    for p in accounts_raw_candidates:
        if p.exists():
            accounts_csv_path = p
            break

    if not trans_csv_path or not accounts_csv_path:
        logger.error(f"Could not locate raw CSV datasets in {base_dir} or {raw_dir}")
        sys.exit(1)

    # Move to raw/ if currently in root datasets/
    target_trans_raw = raw_dir / "LI-Small_Trans.csv"
    if trans_csv_path != target_trans_raw and not target_trans_raw.exists():
        logger.info(f"Copying {trans_csv_path} -> {target_trans_raw}")
        shutil.copy(trans_csv_path, target_trans_raw)
        trans_csv_path = target_trans_raw

    target_acc_raw = raw_dir / "LI-Small_accounts.csv"
    if accounts_csv_path != target_acc_raw and not target_acc_raw.exists():
        logger.info(f"Copying {accounts_csv_path} -> {target_acc_raw}")
        shutil.copy(accounts_csv_path, target_acc_raw)
        accounts_csv_path = target_acc_raw

    # 2. Load Raw CSVs
    logger.info(f"Reading transaction CSV: {trans_csv_path}...")
    trans_df = pd.read_csv(trans_csv_path)

    logger.info(f"Reading accounts CSV: {accounts_csv_path}...")
    accounts_df = pd.read_csv(accounts_csv_path)

    # 3. Validate Raw Data
    logger.info("Running Data Validation Suite...")
    validator = DataValidator(output_dir=processed_dir)
    passed, report = validator.validate(trans_df, accounts_df)
    logger.info(f"Validation Result: {report['status']}")
    logger.info(f"Validation Report saved to: {processed_dir / 'validation_report.json'}")

    # 4. Process Transactions
    logger.info("Preprocessing and standardizing Transactions DataFrame...")
    
    # Rename columns to standard schema
    rename_trans = {
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
    trans_df = trans_df.rename(columns={k: v for k, v in rename_trans.items() if k in trans_df.columns})

    # Parse datetime and sort chronologically
    trans_df["timestamp"] = pd.to_datetime(trans_df["timestamp"], format="%Y/%m/%d %H:%M", errors="coerce")
    trans_df = trans_df.sort_values(by="timestamp").reset_index(drop=True)

    # Add transaction_id if not present
    if "transaction_id" not in trans_df.columns:
        trans_df["transaction_id"] = [f"txn_{i+1:07d}" for i in range(len(trans_df))]

    # Ensure types
    trans_df["from_bank"] = trans_df["from_bank"].astype(str)
    trans_df["from_account"] = trans_df["from_account"].astype(str)
    trans_df["to_bank"] = trans_df["to_bank"].astype(str)
    trans_df["to_account"] = trans_df["to_account"].astype(str)
    trans_df["amount_received"] = trans_df["amount_received"].astype(float)
    trans_df["receiving_currency"] = trans_df["receiving_currency"].astype(str)
    trans_df["amount_paid"] = trans_df["amount_paid"].astype(float)
    trans_df["payment_currency"] = trans_df["payment_currency"].astype(str)
    trans_df["payment_format"] = trans_df["payment_format"].astype(str)
    trans_df["is_laundering"] = trans_df["is_laundering"].astype(int)

    # 5. Process Accounts
    logger.info("Preprocessing and standardizing Accounts DataFrame...")
    rename_acc = {
        "Bank Name": "bank_name",
        "Bank ID": "bank_id",
        "Account Number": "account_number",
        "Entity ID": "entity_id",
        "Entity Name": "entity_name",
    }
    accounts_df = accounts_df.rename(columns={k: v for k, v in rename_acc.items() if k in accounts_df.columns})
    accounts_df["bank_name"] = accounts_df["bank_name"].astype(str)
    accounts_df["bank_id"] = accounts_df["bank_id"].astype(str)
    accounts_df["account_number"] = accounts_df["account_number"].astype(str)
    accounts_df["entity_id"] = accounts_df["entity_id"].astype(str)
    accounts_df["entity_name"] = accounts_df["entity_name"].astype(str)

    # 6. Save as Parquet
    trans_parquet = processed_dir / "transactions.parquet"
    acc_parquet = processed_dir / "accounts.parquet"

    logger.info(f"Saving Parquet: {trans_parquet} ({len(trans_df)} rows)...")
    trans_df.to_parquet(trans_parquet, index=False, engine="pyarrow")

    logger.info(f"Saving Parquet: {acc_parquet} ({len(accounts_df)} rows)...")
    accounts_df.to_parquet(acc_parquet, index=False, engine="pyarrow")

    logger.info("Preprocessing complete! Dataset successfully converted to Parquet.")
    logger.info(f"Processed directory: {processed_dir.resolve()}")


if __name__ == "__main__":
    # Determine default dataset dir based on cwd
    dataset_path = "datasets"
    if not Path(dataset_path).exists() and Path("tribunal/datasets").exists():
        dataset_path = "tribunal/datasets"
    run_preprocessing(dataset_path)
