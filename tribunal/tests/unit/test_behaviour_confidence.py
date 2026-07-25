"""Unit tests for Behaviour ConfidenceAggregator."""

import pytest
from tribunal.experts.behaviour.confidence import ConfidenceAggregator
from tribunal.experts.behaviour.pattern_finding import PatternFinding


def test_behaviour_confidence_aggregator():
    agg = ConfidenceAggregator()
    findings = [
        PatternFinding(
            pattern_name="behaviour_drift",
            score=0.75,
            supporting_features=["behaviour_deviation"],
            supporting_metrics={"behaviour_deviation_ratio": 3.0},
            provenance={"detectors": ["BehaviourDriftDetector"]},
            detector_name="BehaviourDriftDetector",
            affected_accounts=["ACC_BEH_MIX"],
            evidence_details=["Drift detected"],
        ),
        PatternFinding(
            pattern_name="currency_change",
            score=0.80,
            supporting_features=["preferred_currency"],
            supporting_metrics={"currency_switch_frequency": 2.0},
            provenance={"detectors": ["CurrencyChangeDetector"]},
            detector_name="CurrencyChangeDetector",
            affected_accounts=["ACC_BEH_MIX"],
            evidence_details=["Unexpected currency EUR"],
        ),
    ]

    results = agg.aggregate(findings)
    assert len(results) == 1
    r = results[0]
    assert r.primary_account == "ACC_BEH_MIX"
    # 1 - (1-0.75)*(1-0.80) = 1 - 0.25*0.2 = 0.95 -> CRITICAL
    assert r.combined_confidence >= 0.90
    assert r.severity == "CRITICAL"
    assert "behaviour_deviation" in r.supporting_features
    assert "preferred_currency" in r.supporting_features
    assert r.supporting_metrics["currency_switch_frequency"] == 2.0
    assert "BehaviourDriftDetector" in r.provenance["detectors"]
    assert "CurrencyChangeDetector" in r.provenance["detectors"]
