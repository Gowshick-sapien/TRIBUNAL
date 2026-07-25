"""Feature Definitions and Schema Contracts for TRIBUNAL.

Defines feature requirements and formal specifications for Financial Expert,
Behaviour Expert, and Graph-Derived Features.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass(frozen=True)
class FeatureSpec:
    """Formal specification of an analytical feature."""

    name: str
    category: str  # "financial" | "behavioural" | "graph"
    description: str
    required_inputs: List[str]
    consumer_expert: str  # "financial_expert" | "behaviour_expert" | "both"


# Formal Registry of Defined Features
FINANCIAL_EXPERT_FEATURES: List[FeatureSpec] = [
    FeatureSpec(
        name="rolling_sum_7d",
        category="financial",
        description="Rolling sum of transaction amounts over a 7-day window",
        required_inputs=["timestamp", "amount_paid"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="rolling_count_7d",
        category="financial",
        description="Rolling count of transactions over a 7-day window",
        required_inputs=["timestamp"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="velocity",
        category="financial",
        description="Daily transaction velocity (transactions per active day)",
        required_inputs=["timestamp"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="avg_amount",
        category="financial",
        description="Average transaction amount in evaluation window",
        required_inputs=["amount_paid"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="std_amount",
        category="financial",
        description="Standard deviation of transaction amounts in evaluation window",
        required_inputs=["amount_paid"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="threshold_proximity",
        category="financial",
        description="Ratio of transactions falling in threshold-adjacent band (e.g. $9,000 - $9,999)",
        required_inputs=["amount_paid"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="unique_counterparties",
        category="financial",
        description="Count of distinct counterparties interacted with in evaluation window",
        required_inputs=["to_account"],
        consumer_expert="financial_expert",
    ),
    FeatureSpec(
        name="payment_format_frequency",
        category="financial",
        description="Frequency distribution of payment channels (ACH, Cheque, Wire, etc.)",
        required_inputs=["payment_format"],
        consumer_expert="financial_expert",
    ),
]

BEHAVIOUR_EXPERT_FEATURES: List[FeatureSpec] = [
    FeatureSpec(
        name="baseline_daily_amount",
        category="behavioural",
        description="Historical 90-day average daily transaction volume",
        required_inputs=["timestamp", "amount_paid"],
        consumer_expert="behaviour_expert",
    ),
    FeatureSpec(
        name="baseline_frequency",
        category="behavioural",
        description="Historical 90-day average daily transaction count",
        required_inputs=["timestamp"],
        consumer_expert="behaviour_expert",
    ),
    FeatureSpec(
        name="deviation_score",
        category="behavioural",
        description="Percentage change of current activity vs. historical baseline",
        required_inputs=["amount_paid", "timestamp"],
        consumer_expert="behaviour_expert",
    ),
    FeatureSpec(
        name="active_days",
        category="behavioural",
        description="Number of distinct active transaction days in evaluation window",
        required_inputs=["timestamp"],
        consumer_expert="behaviour_expert",
    ),
    FeatureSpec(
        name="currency_changes",
        category="behavioural",
        description="Count of distinct payment currencies used by account",
        required_inputs=["payment_currency"],
        consumer_expert="behaviour_expert",
    ),
]

GRAPH_DERIVED_FEATURES: List[FeatureSpec] = [
    FeatureSpec(
        name="fan_in",
        category="graph",
        description="In-degree of account node in transaction graph (count of incoming unique payees)",
        required_inputs=["from_account", "to_account"],
        consumer_expert="both",
    ),
    FeatureSpec(
        name="fan_out",
        category="graph",
        description="Out-degree of account node in transaction graph (count of outgoing unique beneficiaries)",
        required_inputs=["from_account", "to_account"],
        consumer_expert="both",
    ),
    FeatureSpec(
        name="repeated_counterparties",
        category="graph",
        description="Count of counterparties with transaction frequency > threshold",
        required_inputs=["from_account", "to_account"],
        consumer_expert="both",
    ),
    FeatureSpec(
        name="total_degree",
        category="graph",
        description="Total distinct counterparty connections (fan_in + fan_out)",
        required_inputs=["from_account", "to_account"],
        consumer_expert="both",
    ),
    FeatureSpec(
        name="neighbourhood_size",
        category="graph",
        description="Count of 2-hop reachable accounts in transaction network",
        required_inputs=["from_account", "to_account"],
        consumer_expert="both",
    ),
]

ALL_FEATURE_SPECS: List[FeatureSpec] = (
    FINANCIAL_EXPERT_FEATURES + BEHAVIOUR_EXPERT_FEATURES + GRAPH_DERIVED_FEATURES
)
