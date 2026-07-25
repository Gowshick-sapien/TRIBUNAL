"""Unit tests for FeatureStoreBuilder (Phase B.5)."""

import sys
from pathlib import Path
import pandas as pd
import pytest
import networkx as nx

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tribunal.tools.feature_store_builder import FeatureStoreBuilder
from tribunal.data.loader import DataLoader


@pytest.fixture
def sample_feature_data():
    transactions_df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2022-09-01 00:00:00", "2022-09-01 00:30:00", "2022-09-02 01:00:00", "2022-09-02 01:15:00"]),
        "from_bank": ["011", "011", "012", "011"],
        "from_account": ["acc_001", "acc_001", "acc_002", "acc_001"],
        "to_bank": ["012", "012", "011", "012"],
        "to_account": ["acc_002", "acc_002", "acc_001", "acc_002"],
        "amount_received": [9500.0, 9600.0, 15000.0, 9700.0],
        "receiving_currency": ["US Dollar", "US Dollar", "US Dollar", "US Dollar"],
        "amount_paid": [9500.0, 9600.0, 15000.0, 9700.0],
        "payment_currency": ["US Dollar", "US Dollar", "US Dollar", "US Dollar"],
        "payment_format": ["ACH", "ACH", "Wire", "ACH"],
        "is_laundering": [1, 1, 0, 1],
        "transaction_id": ["txn_001", "txn_002", "txn_003", "txn_004"],
    })

    G = nx.MultiDiGraph()
    G.add_node("acc_001", account_id="acc_001", bank_id="011", bank_name="Bank A")
    G.add_node("acc_002", account_id="acc_002", bank_id="012", bank_name="Bank B")
    G.add_edge("acc_001", "acc_002", key=0, transaction_id="txn_001", amount_paid=9500.0)
    G.add_edge("acc_001", "acc_002", key=1, transaction_id="txn_002", amount_paid=9600.0)
    G.add_edge("acc_002", "acc_001", key=0, transaction_id="txn_003", amount_paid=15000.0)
    G.add_edge("acc_001", "acc_002", key=2, transaction_id="txn_004", amount_paid=9700.0)

    return transactions_df, G


def test_feature_store_build(tmp_path, sample_feature_data):
    trans_df, G = sample_feature_data
    builder = FeatureStoreBuilder(dataset_dir=tmp_path)
    fs_df = builder.build(transactions_df=trans_df, graph=G)

    assert isinstance(fs_df, pd.DataFrame)
    assert len(fs_df) == 2  # acc_001 and acc_002
    assert "account_id" in fs_df.columns
    assert "rolling_sum_7d" in fs_df.columns
    assert "fan_in" in fs_df.columns
    assert "structuring_score" in fs_df.columns

    acc1_row = fs_df[fs_df["account_id"] == "acc_001"].iloc[0]
    # acc_001 has 3 sub-threshold txns ($9500, $9600, $9700) -> sub_threshold_count = 3
    assert acc1_row["sub_threshold_count"] == 3
    assert acc1_row["structuring_score"] > 0.0
    assert acc1_row["fan_out"] == 3  # 3 outgoing transaction edges
    assert acc1_row["unique_receivers"] == 1  # 1 unique receiver (acc_002)
    assert acc1_row["fan_in"] == 1   # 1 incoming transaction edge from acc_002


def test_feature_store_validate(tmp_path, sample_feature_data):
    trans_df, G = sample_feature_data
    builder = FeatureStoreBuilder(dataset_dir=tmp_path)
    builder.build(transactions_df=trans_df, graph=G)

    report = builder.validate()
    assert report["status"] == "PASSED"
    assert report["account_count"] == 2
    assert (tmp_path / "processed" / "feature_validation_report.json").exists()


def test_feature_store_profile(tmp_path, sample_feature_data):
    trans_df, G = sample_feature_data
    builder = FeatureStoreBuilder(dataset_dir=tmp_path)
    builder.build(transactions_df=trans_df, graph=G)

    profile = builder.get_feature_profile()
    assert profile["accounts_processed"] == 2
    assert profile["feature_count"] > 20
    assert (tmp_path / "processed" / "feature_store_profile.json").exists()


def test_feature_store_save_and_loader(tmp_path, sample_feature_data):
    trans_df, G = sample_feature_data
    builder = FeatureStoreBuilder(dataset_dir=tmp_path)
    builder.build(transactions_df=trans_df, graph=G)
    save_path = builder.save()

    assert save_path.exists()

    # Load via DataLoader
    loader = DataLoader(dataset_dir=tmp_path)
    loaded_df = loader.load_feature_store(account_id="acc_001")
    assert len(loaded_df) == 1
    assert loaded_df.iloc[0]["account_id"] == "acc_001"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
