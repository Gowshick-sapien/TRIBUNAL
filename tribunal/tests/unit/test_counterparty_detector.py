"""Unit tests for CounterpartyBehaviourDetector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.counterparty_behaviour_detector import CounterpartyBehaviourDetector


def test_counterparty_detector_expansion():
    detector = CounterpartyBehaviourDetector(counterparty_expansion_threshold=4)
    txns = [{"from_account": "ACC_NET", "to_account": f"RECP_{i}", "transaction_id": f"TXN_{i}"} for i in range(6)]
    df = pd.DataFrame(txns)

    findings = detector.detect(df)
    assert len(findings) == 1
    f = findings[0]
    assert f.pattern_name == "counterparty_expansion"
    assert f.affected_accounts == ["ACC_NET"]
    assert f.supporting_metrics["unique_counterparties"] == 6.0
