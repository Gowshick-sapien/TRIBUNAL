"""Unit tests for Behaviour CandidateSelector."""

import pandas as pd
import pytest
from tribunal.experts.behaviour.candidate_selector import CandidateSelector
from tribunal.models.execution_plan import ExecutionPlan


def test_candidate_selector_behaviour_empty():
    selector = CandidateSelector()
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={}, rationale="")
    result = selector.select_candidates(pd.DataFrame(), exec_plan)
    assert result.empty


def test_candidate_selector_behaviour_filter():
    selector = CandidateSelector()
    df = pd.DataFrame([
        {"from_account": "ACC_BEH1", "to_account": "ACC_BEH2", "amount_received": 1000.0},
        {"from_account": "ACC_BEH9", "to_account": "ACC_BEH8", "amount_received": 200.0},
    ])
    exec_plan = ExecutionPlan(run_eda=True, expert_sequence=["behaviour"], filters={"customer_id": "ACC_BEH1"}, rationale="")
    result = selector.select_candidates(df, exec_plan)
    assert len(result) == 1
    assert result.iloc[0]["from_account"] == "ACC_BEH1"
