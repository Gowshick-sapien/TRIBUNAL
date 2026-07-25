"""Unit tests for BehaviourExpert entry point."""

import pandas as pd
import pytest

from tribunal.experts.behaviour.behaviour_expert import BehaviourExpert
from tribunal.models.case_file import CaseFile
from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.expert_result import ExpertResult
from tribunal.models.investigation_card import InvestigationCard


def test_behaviour_expert_normal_account():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_001")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    normal_df = pd.DataFrame([
        {"from_account": "ACC_BEH_NORM", "amount_received": 100.0, "baseline_daily_amount": 100.0, "transaction_id": "TX1"},
        {"from_account": "ACC_BEH_NORM", "amount_received": 150.0, "baseline_daily_amount": 100.0, "transaction_id": "TX2"},
    ])

    result = expert.investigate(normal_df, case_file, exec_plan)
    assert isinstance(result, ExpertResult)
    assert len(result.cards) == 0


def test_behaviour_expert_dormant_reactivation():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_002")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    dormant_df = pd.DataFrame([
        {"from_account": "ACC_DORMANT_01", "amount_received": 5000.0, "days_since_last_transaction": 120.0, "transaction_id": "TXD1"},
    ])

    result = expert.investigate(dormant_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert card.source_expert == "behaviour"
    assert "ACC_DORMANT_01" in card.affected_accounts
    assert "DormancyDetector" in card.provenance["detectors"]


def test_behaviour_expert_spending_shift():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_003")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    spending_df = pd.DataFrame([
        {"from_account": "ACC_SPEND_01", "amount_received": 100.0, "transaction_id": "TXS1"},
        {"from_account": "ACC_SPEND_01", "amount_received": 150.0, "transaction_id": "TXS2"},
        {"from_account": "ACC_SPEND_01", "amount_received": 30000.0, "transaction_id": "TXS3"},
    ])

    result = expert.investigate(spending_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert card.source_expert == "behaviour"
    assert "SpendingPatternDetector" in card.provenance["detectors"]


def test_behaviour_expert_currency_change():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_004")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    currency_df = pd.DataFrame([
        {"from_account": "ACC_CURR_01", "receiving_currency": "EUR", "preferred_currency": "GBP", "transaction_id": "TXC1"},
        {"from_account": "ACC_CURR_01", "receiving_currency": "USD", "preferred_currency": "GBP", "transaction_id": "TXC2"},
    ])

    result = expert.investigate(currency_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert "CurrencyChangeDetector" in card.provenance["detectors"]


def test_behaviour_expert_payment_format_change():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_005")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    payment_df = pd.DataFrame([
        {"from_account": "ACC_PAY_01", "payment_format": "Wire", "preferred_payment_format": "ach", "transaction_id": "TXP1"},
        {"from_account": "ACC_PAY_01", "payment_format": "Cash", "preferred_payment_format": "ach", "transaction_id": "TXP2"},
    ])

    result = expert.investigate(payment_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert "PaymentPatternDetector" in card.provenance["detectors"]


def test_behaviour_expert_multiple_anomalies():
    expert = BehaviourExpert()
    case_file = CaseFile(case_id="case_beh_006")
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")

    multi_df = pd.DataFrame([
        {
            "from_account": "ACC_MULTI",
            "to_account": "REC_1",
            "amount_received": 25000.0,
            "baseline_daily_amount": 1000.0,
            "receiving_currency": "EUR",
            "preferred_currency": "GBP",
            "payment_format": "Wire",
            "preferred_payment_format": "ach",
            "days_since_last_transaction": 120.0,
            "transaction_id": "TXM1",
        },
        {
            "from_account": "ACC_MULTI",
            "to_account": "REC_2",
            "amount_received": 28000.0,
            "baseline_daily_amount": 1000.0,
            "receiving_currency": "USD",
            "preferred_currency": "GBP",
            "payment_format": "Cash",
            "preferred_payment_format": "ach",
            "days_since_last_transaction": 120.0,
            "transaction_id": "TXM2",
        },
    ])

    result = expert.investigate(multi_df, case_file, exec_plan)
    assert len(result.cards) >= 1
    card = result.cards[0]
    assert card.confidence >= 0.90
    assert card.severity == "CRITICAL"
    assert len(card.provenance["detectors"]) >= 3
