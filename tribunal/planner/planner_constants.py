"""Planner vocabulary constants — single source of truth for TRIBUNAL planner.

Never hardcode string literals for intents, patterns, outputs, experts, or assets elsewhere.
"""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Intents
# -----------------------------------------------------------------------------
PATTERN_DETECTION = "pattern_detection"
BEHAVIOUR_ANALYSIS = "behaviour_analysis"
CUSTOMER_LOOKUP = "customer_lookup"
NETWORK_ANALYSIS = "network_analysis"
EDA_REQUEST = "eda_request"
CASE_SUMMARY = "case_summary"

SUPPORTED_INTENTS: set[str] = {
    PATTERN_DETECTION,
    BEHAVIOUR_ANALYSIS,
    CUSTOMER_LOOKUP,
    NETWORK_ANALYSIS,
    EDA_REQUEST,
    CASE_SUMMARY,
}

# -----------------------------------------------------------------------------
# Patterns
# -----------------------------------------------------------------------------
STRUCTURING = "structuring"
SMURFING = "smurfing"
VELOCITY = "velocity"
FAN_IN = "fan_in"
FAN_OUT = "fan_out"
SCATTER_GATHER = "scatter_gather"
GATHER_SCATTER = "gather_scatter"
HIGH_VALUE_TRANSFER = "high_value_transfer"

SUPPORTED_PATTERNS: set[str] = {
    STRUCTURING,
    SMURFING,
    VELOCITY,
    FAN_IN,
    FAN_OUT,
    SCATTER_GATHER,
    GATHER_SCATTER,
    HIGH_VALUE_TRANSFER,
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------
INVESTIGATION_REPORT = "investigation_report"
SUMMARY = "summary"
GRAPH = "graph"
TABLE = "table"

SUPPORTED_OUTPUTS: set[str] = {
    INVESTIGATION_REPORT,
    SUMMARY,
    GRAPH,
    TABLE,
}

# -----------------------------------------------------------------------------
# Experts
# -----------------------------------------------------------------------------
FINANCIAL = "financial"
BEHAVIOUR = "behaviour"
NETWORK_EXPERT = "network"  # Future expert placeholder

SUPPORTED_EXPERTS: set[str] = {
    FINANCIAL,
    BEHAVIOUR,
}

# -----------------------------------------------------------------------------
# Assets
# -----------------------------------------------------------------------------
FEATURE_STORE = "feature_store"
TRANSACTION_NETWORK = "transaction_network"
DATASET = "dataset"
CASE_FILE = "case_file"

SUPPORTED_ASSETS: set[str] = {
    FEATURE_STORE,
    TRANSACTION_NETWORK,
    DATASET,
    CASE_FILE,
}

# -----------------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------------
EDA_TOOL = "eda_tool"
FEATURE_ENGINEERING = "feature_engineering"
ANOMALY_DETECTION = "anomaly_detection"

SUPPORTED_TOOLS: set[str] = {
    EDA_TOOL,
    FEATURE_ENGINEERING,
    ANOMALY_DETECTION,
}
