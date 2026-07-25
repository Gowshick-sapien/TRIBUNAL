"""Unit tests for CurrencyChangeDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.currency_change_detector import CurrencyChangeDetector


def test_currency_change_detector_unexpected_currency():
    detector = CurrencyChangeDetector()
    df = pd.DataFrame([
        {"from_account": "ACC_CURR", "receiving_currency": "EUR", "preferred_currency": "GBP", "transaction_id": "TXC1"},
        {"from_account": "ACC_CURR", "receiving_currency": "USD", "preferred_currency": "GBP", "transaction_id": "TXC2"},
    ])

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "currency_change"
    assert f.affected_accounts == ["ACC_CURR"]
    assert f.score >= 0.75
