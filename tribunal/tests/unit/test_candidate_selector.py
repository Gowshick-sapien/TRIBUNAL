"""Unit tests for CandidateSelector."""

import pandas as pd
import pytest
from tribunal.experts.financial.candidate_selector import CandidateSelector
from tribunal.models.execution_plan import ExecutionPlan


def test_candidate_selector_empty():
    selector = CandidateSelector()
    exec_plan = ExecutionPlan(
        run_eda=True, expert_sequence=["financial"], filters={}, rationale=""
    )
    result = selector.select_candidates(pd.DataFrame(), exec_plan)
    assert result.empty


def test_candidate_selector_entity_filter():
    selector = CandidateSelector()
    df = pd.DataFrame(
        [
            {"from_account": "ACC100", "to_account": "ACC200", "amount_received": 5000.0},
            {"from_account": "ACC999", "to_account": "ACC888", "amount_received": 1000.0},
        ]
    )
    exec_plan = ExecutionPlan(
        run_eda=True,
        expert_sequence=["financial"],
        filters={"customer_id": "ACC100"},
        rationale="",
    )
    result = selector.select_candidates(df, exec_plan)
    assert len(result) == 1
    assert result.iloc[0]["from_account"] == "ACC100"
