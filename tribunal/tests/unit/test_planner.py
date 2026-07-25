"""Unit tests for Planner orchestrator."""

import pytest
from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.models.planning_result import PlanningResult
from tribunal.models.user_query import UserQuery
from tribunal.planner.llm_client import LLMClient
from tribunal.planner.planner import Planner, PlannerContext


def test_planner_with_mock_llm():
    def mock_caller(prompt: str) -> str:
        return """{
            "intent": "pattern_detection",
            "pattern": "structuring",
            "filters": {"date_range": "last_30_days"},
            "requested_output": "investigation_report"
        }"""

    client = LLMClient(custom_caller=mock_caller)
    planner = Planner(llm_client=client)

    result = planner.plan("Find structuring during the last month")
    assert isinstance(result, PlanningResult)
    assert isinstance(result.investigation_plan, InvestigationPlan)
    assert isinstance(result.execution_plan, ExecutionPlan)
    assert isinstance(result.planner_context, PlannerContext)

    # Check ExecutionPlan versioning
    assert result.execution_plan.schema_version == "1.0"
    assert result.execution_plan.planner_version == "C.1"
    assert result.execution_plan.expert_sequence == ["financial", "behaviour"]
    assert result.execution_plan.needs_tribunal is True
    assert result.execution_plan.target_pattern == "structuring"

    # Check Profiling Metrics
    assert "llm_ms" in result.metrics
    assert "parser_ms" in result.metrics
    assert "planner_ms" in result.metrics
    assert "total_ms" in result.metrics
    assert result.metrics["total_ms"] >= 0


def test_planner_create_execution():
    def mock_caller(prompt: str) -> str:
        return '{"intent": "behaviour_analysis"}'

    client = LLMClient(custom_caller=mock_caller)
    planner = Planner(llm_client=client)

    output = planner.create_execution(UserQuery(text="Show behavioural anomalies"))
    assert isinstance(output, PlanningResult)
    assert isinstance(output.investigation_plan, InvestigationPlan)
    assert isinstance(output.execution_plan, ExecutionPlan)
    assert output.execution_plan.expert_sequence == ["behaviour"]
    assert output.execution_plan.schema_version == "1.0"
    assert output.execution_plan.planner_version == "C.1"


def test_planner_fallback_when_ollama_unreachable():
    client = LLMClient(endpoint="http://localhost:59999/unreachable", timeout=0.1)
    planner = Planner(llm_client=client)

    result = planner.plan("Show payment format distribution")
    assert isinstance(result, PlanningResult)
    assert result.execution_plan.assets == ["dataset"]
    assert result.execution_plan.tools == ["eda_tool"]
    assert len(result.planner_context.validation_errors) > 0


@pytest.mark.parametrize(
    "query_text,expected_experts,expected_assets,expected_tribunal",
    [
        (
            "Find structuring during the last month",
            ["financial", "behaviour"],
            ["feature_store"],
            True,
        ),
        (
            "Show behavioural anomalies",
            ["behaviour"],
            ["feature_store"],
            True,
        ),
        (
            "Investigate account 8000A94C0",
            ["financial", "behaviour"],
            ["feature_store", "transaction_network"],
            True,
        ),
        (
            "Show payment format distribution",
            [],
            ["dataset"],
            False,
        ),
        (
            "Summarize investigation",
            [],
            ["case_file"],
            False,
        ),
    ],
)
def test_verification_matrix_queries(query_text, expected_experts, expected_assets, expected_tribunal):
    planner = Planner()  # Uses fallback rule-based parser
    result = planner.plan(query_text)
    exec_plan = result.execution_plan

    assert exec_plan.expert_sequence == expected_experts
    for asset in expected_assets:
        assert asset in exec_plan.assets
    assert exec_plan.needs_tribunal == expected_tribunal
