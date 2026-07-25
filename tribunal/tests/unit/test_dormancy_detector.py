"""Unit tests for DormancyDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.dormancy_detector import DormancyDetector


def test_dormancy_detector_reactivation():
    detector = DormancyDetector()
    df = pd.DataFrame([
        {"from_account": "ACC_DORMANT", "amount_received": 15000.0, "days_since_last_transaction": 120.0, "transaction_id": "TXR1"},
        {"from_account": "ACC_ACTIVE", "amount_received": 100.0, "days_since_last_transaction": 2.0, "transaction_id": "TXR2"},
    ])

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "dormancy_reactivation"
    assert f.affected_accounts == ["ACC_DORMANT"]
    assert f.score >= 0.80
