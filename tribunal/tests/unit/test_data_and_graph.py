"""Unit tests for DataLoader, DataValidator, Transaction/Account models, and TransactionGraph."""

import sys
from pathlib import Path

# Enable direct script execution via 'python path/to/test_data_and_graph.py'
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from datetime import datetime
import pandas as pd
import pytest

from tribunal.models.account import Account
from tribunal.models.transaction import Transaction
from tribunal.data.validator import DataValidator
from tribunal.investigation.transaction_graph import TransactionGraph


def test_transaction_model_instantiation():
    now = datetime.now()
    txn = Transaction(
        timestamp=now,
        from_bank="011",
        from_account="acc_1",
        to_bank="012",
        to_account="acc_2",
        amount_received=5000.0,
        receiving_currency="US Dollar",
        amount_paid=5000.0,
        payment_currency="US Dollar",
        payment_format="ACH",
        is_laundering=0,
        transaction_id="txn_1001"
    )
    assert txn.from_account == "acc_1"
    assert txn.to_account == "acc_2"
    assert txn.amount_paid == 5000.0
    
    d = txn.to_dict()
    assert d["from_account"] == "acc_1"
    
    reconstructed = Transaction.from_dict(d)
    assert reconstructed.from_account == txn.from_account
    assert reconstructed.amount_paid == txn.amount_paid


def test_account_model_instantiation():
    acc = Account(
        bank_name="Test Bank",
        bank_id="011",
        account_number="acc_1",
        entity_id="entity_1",
        entity_name="Corporation #123"
    )
    assert acc.bank_name == "Test Bank"
    assert acc.account_number == "acc_1"
    
    d = acc.to_dict()
    reconstructed = Account.from_dict(d)
    assert reconstructed.account_number == acc.account_number


def test_data_validator(tmp_path):
    df_trans = pd.DataFrame({
        "Timestamp": ["2022/09/01 00:00", "2022/09/01 01:00"],
        "From Bank": ["011", "012"],
        "Account": ["acc_1", "acc_2"],
        "To Bank": ["012", "013"],
        "Account.1": ["acc_2", "acc_3"],
        "Amount Received": [1000.0, 2000.0],
        "Receiving Currency": ["US Dollar", "US Dollar"],
        "Amount Paid": [1000.0, 2000.0],
        "Payment Currency": ["US Dollar", "US Dollar"],
        "Payment Format": ["ACH", "Wire"],
        "Is Laundering": [0, 0]
    })
    
    df_acc = pd.DataFrame({
        "Bank Name": ["Test Bank"],
        "Bank ID": ["011"],
        "Account Number": ["acc_1"],
        "Entity ID": ["ent_1"],
        "Entity Name": ["Corp 1"]
    })

    validator = DataValidator(output_dir=tmp_path)
    passed, report = validator.validate(df_trans, df_acc)
    assert passed is True
    assert report["status"] == "PASSED"
    assert (tmp_path / "validation_report.json").exists()


def test_transaction_graph():
    df_trans = pd.DataFrame({
        "timestamp": pd.to_datetime(["2022-09-01 00:00:00", "2022-09-01 01:00:00", "2022-09-01 02:00:00"]),
        "from_account": ["acc_1", "acc_2", "acc_1"],
        "to_account": ["acc_3", "acc_3", "acc_2"],
        "amount_paid": [9500.0, 9600.0, 15000.0],
        "payment_format": ["ACH", "ACH", "Wire"]
    })

    tg = TransactionGraph()
    tg.build_from_dataframe(df_trans)

    # acc_3 receives from acc_1 and acc_2 -> fan_in = 2
    assert tg.get_fan_in("acc_3") == 2
    assert tg.get_fan_out("acc_3") == 0

    # acc_1 sends to acc_3 and acc_2 -> fan_out = 2
    assert tg.get_fan_out("acc_1") == 2
    assert tg.get_fan_in("acc_1") == 0

    # Total degree of acc_2 (sends to acc_3, receives from acc_1) = 2
    assert tg.get_degree("acc_2") == 2

    metrics = tg.get_account_graph_metrics("acc_3")
    assert metrics["fan_in"] == 2
    assert metrics["fan_out"] == 0
    assert metrics["total_degree"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
