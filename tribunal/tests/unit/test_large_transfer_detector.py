"""Unit tests for LargeTransferDetector."""

import pandas as pd
import pytest
from tribunal.experts.financial.large_transfer_detector import LargeTransferDetector


def test_large_transfer_detector_detection():
    detector = LargeTransferDetector(fixed_large_threshold=50000.0)
    df = pd.DataFrame(
        [
            {"from_account": "ACC_WHALE", "amount_received": 150000.0, "transaction_id": "TX_WHALE"},
            {"from_account": "ACC_NORMAL", "amount_received": 100.0, "transaction_id": "TX_NORM"},
        ]
    )

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "large_transfer"
    assert f.affected_accounts == ["ACC_WHALE"]
    assert f.score >= 0.60
