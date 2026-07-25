"""Execution Planner module — Deterministic construction of ExecutionPlan from InvestigationPlan."""

from __future__ import annotations

from typing import Any

from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.planner.exceptions import ExecutionPlannerError
from tribunal.planner.planner_constants import (
    BEHAVIOUR,
    BEHAVIOUR_ANALYSIS,
    CASE_FILE,
    CASE_SUMMARY,
    CUSTOMER_LOOKUP,
    DATASET,
    EDA_REQUEST,
    EDA_TOOL,
    FEATURE_STORE,
    FINANCIAL,
    GRAPH,
    INVESTIGATION_REPORT,
    NETWORK_ANALYSIS,
    PATTERN_DETECTION,
    SUMMARY,
    TRANSACTION_NETWORK,
)


class ExecutionPlanner:
    """Translates an InvestigationPlan into a deterministic ExecutionPlan.
    
    Contains execution rules for assets, expert sequencing, tools, and tribunal requirements.
    Does not use AI or LLM.
    """

    def plan(self, investigation_plan: InvestigationPlan) -> ExecutionPlan:
        """Construct deterministic ExecutionPlan based on intent and investigation plan parameters."""
        if not investigation_plan or not investigation_plan.intent:
            raise ExecutionPlannerError("Invalid InvestigationPlan: intent is required")

        intent = investigation_plan.intent
        pattern = investigation_plan.target_pattern
        filters = dict(investigation_plan.filters or {})

        # Transfer entities into filters if present
        if investigation_plan.entities and "entities" not in filters:
            filters["entities"] = investigation_plan.entities
        if investigation_plan.customer_id and "customer_id" not in filters:
            filters["customer_id"] = investigation_plan.customer_id

        # Deterministic mapping execution matrix
        if intent == PATTERN_DETECTION:
            assets = [FEATURE_STORE]
            experts = [FINANCIAL, BEHAVIOUR]
            tools = []
            needs_tribunal = True
            needs_report = True
            output_format = INVESTIGATION_REPORT
            rationale = f"Pattern detection execution flow for pattern '{pattern or 'general'}' using Feature Store."

        elif intent == BEHAVIOUR_ANALYSIS:
            assets = [FEATURE_STORE]
            experts = [BEHAVIOUR]
            tools = []
            needs_tribunal = True
            needs_report = True
            output_format = INVESTIGATION_REPORT
            rationale = "Behavioural analysis execution flow focusing on account/customer anomaly detection."

        elif intent == CUSTOMER_LOOKUP:
            assets = [FEATURE_STORE, TRANSACTION_NETWORK]
            experts = [FINANCIAL, BEHAVIOUR]
            tools = []
            needs_tribunal = True
            needs_report = True
            output_format = INVESTIGATION_REPORT
            rationale = f"Customer lookup execution flow for target '{investigation_plan.customer_id or 'specified entity'}' across features and transaction graph."

        elif intent == NETWORK_ANALYSIS:
            assets = [TRANSACTION_NETWORK]
            experts = []
            tools = []
            needs_tribunal = False
            needs_report = False
            output_format = GRAPH
            rationale = "Network analysis execution flow building topological transaction graph."

        elif intent == EDA_REQUEST:
            assets = [DATASET]
            experts = []
            tools = [EDA_TOOL]
            needs_tribunal = False
            needs_report = False
            output_format = SUMMARY
            rationale = "EDA request execution flow utilizing EDA tool to compute dataset statistics."

        elif intent == CASE_SUMMARY:
            assets = [CASE_FILE]
            experts = []
            tools = []
            needs_tribunal = False
            needs_report = True
            output_format = SUMMARY
            rationale = "Case summary execution flow building narrative summary from case file."

        else:
            raise ExecutionPlannerError(f"Unsupported intent for execution planning: '{intent}'")

        return ExecutionPlan(
            run_eda=investigation_plan.run_eda,
            expert_sequence=experts,
            filters=filters,
            rationale=rationale,
            target_pattern=pattern,
            assets=assets,
            tools=tools,
            needs_tribunal=needs_tribunal,
            needs_report=needs_report,
            output_format=output_format,
        )
