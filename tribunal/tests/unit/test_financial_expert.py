"""Unit tests for FinancialExpert entry point."""

import pandas as pd
import pytest

from tribunal.experts.financial.financial_expert import FinancialExpert
from tribunal.models.case_file import CaseFile
from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.expert_result import ExpertResult
from tribunal.models.investigation_card import InvestigationCard


def test_financial_expert_normal_account():
    expert = FinancialExpert()
    case_file = CaseFile(case_id="case_001")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["financial"], filters={}, rationale="")

    normal_df = pd.DataFrame([
        {"from_account": "ACC_NORMAL", "amount_received": 100.0, "transaction_id": "TX1"},
        {"from_account": "ACC_NORMAL", "amount_received": 150.0, "transaction_id": "TX2"},
    ])

    result = expert.investigate(normal_df, case_file, exec_plan)
    assert isinstance(result, ExpertResult)
    assert len(result.cards) == 0


def test_financial_expert_known_structuring():
    expert = FinancialExpert()
    case_file = CaseFile(case_id="case_002")
    exec_plan = ExecutionPlan(
        run_eda=True,
        expert_sequence=["financial"],
        filters={"customer_id": "ACC_STRUCT"},
        rationale="",
    )

    struct_df = pd.DataFrame([
        {"from_account": "ACC_STRUCT", "amount_received": 9800.0, "transaction_id": "TX1"},
        {"from_account": "ACC_STRUCT", "amount_received": 9500.0, "transaction_id": "TX2"},
        {"from_account": "ACC_STRUCT", "amount_received": 9900.0, "transaction_id": "TX3"},
    ])

    result = expert.investigate(struct_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert isinstance(card, InvestigationCard)
    assert card.source_expert == "financial"
    assert "ACC_STRUCT" in card.affected_accounts
    assert "structuring" in card.hypothesis.lower() or "anomaly" in card.hypothesis.lower()
    assert card.confidence >= 0.75
    assert card.severity in ("HIGH", "CRITICAL")

    # Assert Provenance & Supporting Metrics
    assert "provenance" in card.to_dict()
    assert "StructuringDetector" in card.provenance["detectors"]
    assert len(card.provenance["transaction_ids"]) == 3
    assert "threshold_proximity" in card.supporting_metrics
    assert card.supporting_metrics["threshold_proximity"] > 0.90


def test_financial_expert_velocity_spike():
    expert = FinancialExpert()
    case_file = CaseFile(case_id="case_003")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["financial"], filters={}, rationale="")

    velocity_txns = [{"from_account": "ACC_VEL", "amount_received": 500.0, "transaction_id": f"TXV_{i}"} for i in range(10)]
    vel_df = pd.DataFrame(velocity_txns)

    result = expert.investigate(vel_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert "ACC_VEL" in card.affected_accounts
    assert "VelocityDetector" in card.provenance["detectors"]
    assert "velocity_score" in card.supporting_metrics


def test_financial_expert_mixed_pattern():
    expert = FinancialExpert()
    case_file = CaseFile(case_id="case_004")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["financial"], filters={}, rationale="")

    mixed_txns = [
        {"from_account": "ACC_MIXED", "amount_received": 9500.0, "transaction_id": f"TXM_{i}"} for i in range(6)
    ]
    mixed_df = pd.DataFrame(mixed_txns)

    result = expert.investigate(mixed_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert card.confidence >= 0.90
    assert card.severity == "CRITICAL"
    assert len(card.provenance["detectors"]) >= 2


def test_financial_expert_empty_dataset():
    expert = FinancialExpert()
    case_file = CaseFile(case_id="case_005")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["financial"], filters={}, rationale="")

    result = expert.investigate(pd.DataFrame(), case_file, exec_plan)
    assert len(result.cards) == 0
