"""Unit tests for TransactionNetworkBuilder (Phase B.4)."""

import sys
from pathlib import Path
import pandas as pd
import pytest
import networkx as nx

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tribunal.investigation.transaction_network_builder import TransactionNetworkBuilder


@pytest.fixture
def sample_data():
    transactions_df = pd.DataFrame({
        "timestamp": ["2022/09/01 00:00", "2022/09/01 01:00", "2022/09/02 02:00"],
        "from_bank": ["011", "011", "012"],
        "from_account": ["8001F9760", "8001F9760", "8002F9761"],
        "to_bank": ["012", "012", "8001F9760"],
        "to_account": ["8002F9761", "8002F9761", "8001F9760"],
        "amount_received": [5000.0, 3000.0, 1000.0],
        "receiving_currency": ["US Dollar", "US Dollar", "US Dollar"],
        "amount_paid": [5000.0, 3000.0, 1000.0],
        "payment_currency": ["US Dollar", "US Dollar", "US Dollar"],
        "payment_format": ["ACH", "ACH", "Wire"],
        "is_laundering": [1, 1, 0],
        "transaction_id": ["txn_001", "txn_002", "txn_003"],
    })

    accounts_df = pd.DataFrame({
        "bank_name": ["Bank A", "Bank B"],
        "bank_id": ["011", "012"],
        "account_number": ["8001F9760", "8002F9761"],
        "entity_id": ["ent_1", "ent_2"],
        "entity_name": ["Corp A", "Corp B"],
    })

    return transactions_df, accounts_df


def test_network_builder_build(tmp_path, sample_data):
    trans_df, acc_df = sample_data
    builder = TransactionNetworkBuilder(dataset_dir=tmp_path)
    graph = builder.build(transactions_df=trans_df, accounts_df=acc_df)

    assert isinstance(graph, nx.MultiDiGraph)
    # Check total nodes == 2 unique accounts
    assert graph.number_of_nodes() == 2
    # Check total edges == 3 transactions
    assert graph.number_of_edges() == 3

    # Check node attributes
    assert graph.nodes["8001F9760"]["bank_name"] == "Bank A"
    assert graph.nodes["8001F9760"]["out_degree"] == 2
    assert graph.nodes["8001F9760"]["in_degree"] == 1

    # Check MultiDiGraph edge multiplicity between 8001F9760 -> 8002F9761 (should be 2 edges)
    edges_between = graph.get_edge_data("8001F9760", "8002F9761")
    assert len(edges_between) == 2


def test_network_builder_validate(tmp_path, sample_data):
    trans_df, acc_df = sample_data
    builder = TransactionNetworkBuilder(dataset_dir=tmp_path)
    builder.build(transactions_df=trans_df, accounts_df=acc_df)
    
    report = builder.validate()
    assert report["status"] == "PASSED"
    assert report["node_count"] == 2
    assert report["edge_count"] == 3
    assert (tmp_path / "processed" / "network_validation_report.json").exists()


def test_network_builder_statistics(tmp_path, sample_data):
    trans_df, acc_df = sample_data
    builder = TransactionNetworkBuilder(dataset_dir=tmp_path)
    builder.build(transactions_df=trans_df, accounts_df=acc_df)

    stats = builder.get_network_statistics()
    assert stats["total_nodes"] == 2
    assert stats["total_edges"] == 3
    assert stats["weakly_connected_components_count"] == 1
    assert stats["repeated_transaction_pairs_count"] == 1  # 8001F9760 -> 8002F9761 has 2 txns
    assert (tmp_path / "processed" / "network_profile.json").exists()


def test_network_builder_save_and_load(tmp_path, sample_data):
    trans_df, acc_df = sample_data
    builder = TransactionNetworkBuilder(dataset_dir=tmp_path)
    original_graph = builder.build(transactions_df=trans_df, accounts_df=acc_df)

    save_path = builder.save()
    assert save_path.exists()

    # Load in new builder instance
    new_builder = TransactionNetworkBuilder(dataset_dir=tmp_path)
    loaded_graph = new_builder.load(path=save_path)

    assert loaded_graph.number_of_nodes() == original_graph.number_of_nodes()
    assert loaded_graph.number_of_edges() == original_graph.number_of_edges()
    assert loaded_graph.nodes["8001F9760"]["bank_name"] == "Bank A"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
