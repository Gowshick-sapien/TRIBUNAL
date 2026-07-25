"""Unit tests for PaymentPatternDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.payment_pattern_detector import PaymentPatternDetector


def test_payment_pattern_detector_unexpected_format():
    detector = PaymentPatternDetector()
    df = pd.DataFrame([
        {"from_account": "ACC_PAY", "payment_format": "Wire", "preferred_payment_format": "ach", "transaction_id": "TXP1"},
        {"from_account": "ACC_PAY", "payment_format": "Cash", "preferred_payment_format": "ach", "transaction_id": "TXP2"},
    ])

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "payment_pattern_change"
    assert f.affected_accounts == ["ACC_PAY"]
    assert f.score >= 0.70
