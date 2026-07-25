"""Unit tests for ConfidenceAggregator."""

import pytest
from tribunal.experts.financial.confidence import ConfidenceAggregator
from tribunal.experts.financial.pattern_finding import PatternFinding


def test_confidence_aggregator_severity_levels():
    agg = ConfidenceAggregator()
    assert agg.calculate_severity(0.95) == "CRITICAL"
    assert agg.calculate_severity(0.85) == "HIGH"
    assert agg.calculate_severity(0.65) == "MEDIUM"
    assert agg.calculate_severity(0.45) == "LOW"


def test_confidence_aggregator_combination():
    agg = ConfidenceAggregator()
    findings = [
        PatternFinding(
            pattern_name="structuring",
            score=0.80,
            supporting_features=["threshold_proximity"],
            affected_accounts=["ACC_MIX"],
            evidence_details=["Detail 1"],
        ),
        PatternFinding(
            pattern_name="velocity",
            score=0.70,
            supporting_features=["burst_score"],
            affected_accounts=["ACC_MIX"],
            evidence_details=["Detail 2"],
        ),
    ]

    results = agg.aggregate(findings)
    assert len(results) == 1
    r = results[0]
    assert r.primary_account == "ACC_MIX"
    # 1 - (1-0.8)*(1-0.7) = 1 - 0.2*0.3 = 0.94 -> CRITICAL
    assert r.combined_confidence >= 0.90
    assert r.severity == "CRITICAL"
    assert "threshold_proximity" in r.supporting_features
    assert "burst_score" in r.supporting_features
