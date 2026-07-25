"""Unit tests for FrequencyDetector."""

import pandas as pd
import pytest
from tribunal.experts.financial.frequency_detector import FrequencyDetector


def test_frequency_detector_detection():
    detector = FrequencyDetector(high_frequency_count=5)
    txns = [{"from_account": "ACC_FREQ", "amount_received": 500.0, "transaction_id": f"TXF_{i}"} for i in range(6)]
    df = pd.DataFrame(txns)

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "frequency"
    assert f.affected_accounts == ["ACC_FREQ"]
