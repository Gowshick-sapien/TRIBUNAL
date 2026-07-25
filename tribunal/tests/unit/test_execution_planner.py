"""Unit tests for ExecutionPlanner."""

import pytest
from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.planner.execution_planner import ExecutionPlanner


def test_execution_plan_pattern_detection():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Find structuring",
        intent="pattern_detection",
        experts=["financial", "behaviour"],
        run_eda=True,
        target_pattern="structuring",
    )
    exec_plan = planner.plan(inv_plan)

    assert isinstance(exec_plan, ExecutionPlan)
    assert exec_plan.expert_sequence == ["financial", "behaviour"]
    assert exec_plan.assets == ["feature_store"]
    assert exec_plan.needs_tribunal is True
    assert exec_plan.needs_report is True
    assert exec_plan.target_pattern == "structuring"


def test_execution_plan_behaviour_analysis():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Show behavioural anomalies",
        intent="behaviour_analysis",
        experts=["behaviour"],
        run_eda=True,
    )
    exec_plan = planner.plan(inv_plan)

    assert exec_plan.expert_sequence == ["behaviour"]
    assert exec_plan.assets == ["feature_store"]
    assert exec_plan.needs_tribunal is True
    assert exec_plan.needs_report is True


def test_execution_plan_customer_lookup():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Investigate account 8000A94C0",
        intent="customer_lookup",
        experts=["financial", "behaviour"],
        run_eda=True,
        customer_id="8000A94C0",
        entities=["8000A94C0"],
    )
    exec_plan = planner.plan(inv_plan)

    assert exec_plan.expert_sequence == ["financial", "behaviour"]
    assert "feature_store" in exec_plan.assets
    assert "transaction_network" in exec_plan.assets
    assert exec_plan.needs_tribunal is True
    assert exec_plan.needs_report is True
    assert exec_plan.filters["customer_id"] == "8000A94C0"


def test_execution_plan_network_analysis():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Analyze transaction graph",
        intent="network_analysis",
        experts=[],
        run_eda=False,
    )
    exec_plan = planner.plan(inv_plan)

    assert exec_plan.assets == ["transaction_network"]
    assert exec_plan.expert_sequence == []
    assert exec_plan.needs_tribunal is False
    assert exec_plan.output_format == "graph"


def test_execution_plan_eda_request():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Show payment format distribution",
        intent="eda_request",
        experts=[],
        run_eda=True,
    )
    exec_plan = planner.plan(inv_plan)

    assert exec_plan.assets == ["dataset"]
    assert exec_plan.tools == ["eda_tool"]
    assert exec_plan.needs_tribunal is False
    assert exec_plan.output_format == "summary"


def test_execution_plan_case_summary():
    planner = ExecutionPlanner()
    inv_plan = InvestigationPlan(
        raw_query="Summarize investigation",
        intent="case_summary",
        experts=[],
        run_eda=False,
    )
    exec_plan = planner.plan(inv_plan)

    assert exec_plan.assets == ["case_file"]
    assert exec_plan.expert_sequence == []
    assert exec_plan.needs_tribunal is False
    assert exec_plan.needs_report is True
    assert exec_plan.output_format == "summary"
