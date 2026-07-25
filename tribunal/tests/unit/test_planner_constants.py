"""Unit tests for planner constants."""

import pytest
from tribunal.planner.planner_constants import (
    BEHAVIOUR_ANALYSIS,
    CASE_SUMMARY,
    CUSTOMER_LOOKUP,
    EDA_REQUEST,
    NETWORK_ANALYSIS,
    PATTERN_DETECTION,
    STRUCTURING,
    SUPPORTED_ASSETS,
    SUPPORTED_EXPERTS,
    SUPPORTED_INTENTS,
    SUPPORTED_OUTPUTS,
    SUPPORTED_PATTERNS,
)


def test_supported_intents():
    assert "pattern_detection" in SUPPORTED_INTENTS
    assert "behaviour_analysis" in SUPPORTED_INTENTS
    assert "customer_lookup" in SUPPORTED_INTENTS
    assert "network_analysis" in SUPPORTED_INTENTS
    assert "eda_request" in SUPPORTED_INTENTS
    assert "case_summary" in SUPPORTED_INTENTS
    assert len(SUPPORTED_INTENTS) == 6


def test_supported_patterns():
    assert STRUCTURING in SUPPORTED_PATTERNS
    assert "velocity" in SUPPORTED_PATTERNS
    assert "scatter_gather" in SUPPORTED_PATTERNS
    assert "high_value_transfer" in SUPPORTED_PATTERNS


def test_supported_outputs_and_experts():
    assert "investigation_report" in SUPPORTED_OUTPUTS
    assert "summary" in SUPPORTED_OUTPUTS
    assert "financial" in SUPPORTED_EXPERTS
    assert "behaviour" in SUPPORTED_EXPERTS
    assert "feature_store" in SUPPORTED_ASSETS
