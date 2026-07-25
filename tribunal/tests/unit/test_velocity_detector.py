"""Unit tests for VelocityDetector."""

import pandas as pd
import pytest
from tribunal.experts.financial.velocity_detector import VelocityDetector


def test_velocity_detector_detection():
    detector = VelocityDetector(velocity_threshold_per_day=3.0)
    txns = [{"from_account": "ACC_VEL", "amount_received": 1000.0, "transaction_id": f"TX_{i}"} for i in range(10)]
    df = pd.DataFrame(txns)

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "velocity"
    assert f.affected_accounts == ["ACC_VEL"]
    assert f.score > 0.50
