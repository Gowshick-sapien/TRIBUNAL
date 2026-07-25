"""Unit tests for BehaviourDriftDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.behaviour_drift_detector import BehaviourDriftDetector


def test_behaviour_drift_detector_detection():
    detector = BehaviourDriftDetector(drift_multiplier_threshold=2.5)
    df = pd.DataFrame([
        {"from_account": "ACC_DRIFT", "amount_received": 10000.0, "baseline_daily_amount": 1000.0, "transaction_id": "TXD1"},
        {"from_account": "ACC_DRIFT", "amount_received": 8000.0, "baseline_daily_amount": 1000.0, "transaction_id": "TXD2"},
        {"from_account": "ACC_NORMAL", "amount_received": 100.0, "baseline_daily_amount": 100.0, "transaction_id": "TXD3"},
    ])

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "behaviour_drift"
    assert f.affected_accounts == ["ACC_DRIFT"]
    assert f.supporting_metrics["behaviour_deviation_ratio"] >= 2.5
