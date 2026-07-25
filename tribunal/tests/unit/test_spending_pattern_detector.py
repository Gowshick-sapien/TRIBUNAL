"""Unit tests for SpendingPatternDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.spending_pattern_detector import SpendingPatternDetector


def test_spending_pattern_detector_shift():
    detector = SpendingPatternDetector()
    df = pd.DataFrame([
        {"from_account": "ACC_SPEND", "amount_received": 100.0, "transaction_id": "TXS1"},
        {"from_account": "ACC_SPEND", "amount_received": 200.0, "transaction_id": "TXS2"},
        {"from_account": "ACC_SPEND", "amount_received": 25000.0, "transaction_id": "TXS3"},
    ])

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "spending_pattern_change"
    assert f.affected_accounts == ["ACC_SPEND"]
    assert f.supporting_metrics["max_transaction_amount"] == 25000.0
