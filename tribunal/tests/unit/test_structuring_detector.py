"""Unit tests for StructuringDetector."""

import pandas as pd
import pytest
from tribunal.experts.financial.structuring_detector import StructuringDetector


def test_structuring_detector_detection():
    detector = StructuringDetector(threshold=10000.0, proximity_ratio=0.80)
    df = pd.DataFrame(
        [
            {"from_account": "ACC_STRUCT", "amount_received": 9500.0, "transaction_id": "TX1"},
            {"from_account": "ACC_STRUCT", "amount_received": 9800.0, "transaction_id": "TX2"},
            {"from_account": "ACC_STRUCT", "amount_received": 9200.0, "transaction_id": "TX3"},
            {"from_account": "ACC_NORMAL", "amount_received": 500.0, "transaction_id": "TX4"},
        ]
    )

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "structuring"
    assert f.affected_accounts == ["ACC_STRUCT"]
    assert f.score >= 0.80
    assert len(f.transaction_ids) == 3


def test_structuring_detector_no_findings():
    detector = StructuringDetector(threshold=10000.0, proximity_ratio=0.80)
    df = pd.DataFrame(
        [
            {"from_account": "ACC1", "amount_received": 100.0},
            {"from_account": "ACC1", "amount_received": 200.0},
        ]
    )
    findings = detector.detect(df)
    assert len(findings) == 0
