"""Unit tests for ExplainabilityEngine (Phase C.7)."""

from __future__ import annotations

from tribunal.report.explainability_engine import ExplainabilityEngine


def test_explain_metric_threshold_proximity():
    engine = ExplainabilityEngine()
    exp = engine.explain_metric("threshold_proximity", 0.96)
    assert "96.0%" in exp
    assert "regulatory reporting threshold" in exp


def test_explain_metric_dormancy():
    engine = ExplainabilityEngine()
    exp = engine.explain_metric("days_since_last_transaction", 120)
    assert "120" in exp
    assert "dormant period" in exp


def test_explain_metric_currency():
    engine = ExplainabilityEngine()
    exp = engine.explain_metric("currency_switch", "EUR")
    assert "EUR" in exp
    assert "Unexpected currency shift" in exp


def test_explain_finding():
    engine = ExplainabilityEngine()
    explanations = engine.explain_finding("Structuring Activity", {"threshold_proximity": 0.95})
    assert len(explanations) == 2
    assert "Summary: Structuring Activity." in explanations[0]
