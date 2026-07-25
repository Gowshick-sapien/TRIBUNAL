"""Planner orchestrator — Main entry point for query planning in TRIBUNAL."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import time
from typing import Optional, Union

from tribunal.models.execution_plan import ExecutionPlan
from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.models.planning_result import PlanningResult
from tribunal.models.user_query import UserQuery
from tribunal.planner.exceptions import LLMClientError, PlannerError
from tribunal.planner.execution_planner import ExecutionPlanner
from tribunal.planner.llm_client import LLMClient
from tribunal.planner.query_parser import QueryParser

logger = logging.getLogger("tribunal.planner")


@dataclass
class PlannerContext:
    """Internal context holding state and metrics across the planning pipeline."""
    raw_query: str
    llm_response: Optional[str] = None
    investigation_plan: Optional[InvestigationPlan] = None
    execution_plan: Optional[ExecutionPlan] = None
    validation_errors: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)


class Planner:
    """Orchestrates natural language query understanding and execution plan construction."""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        query_parser: Optional[QueryParser] = None,
        execution_planner: Optional[ExecutionPlanner] = None,
    ):
        self.llm_client = llm_client or LLMClient()
        self.query_parser = query_parser or QueryParser()
        self.execution_planner = execution_planner or ExecutionPlanner()

    def plan(self, query: Union[UserQuery, str]) -> PlanningResult:
        """Pipeline entry point: UserQuery -> LLM / Parser -> InvestigationPlan -> ExecutionPlan."""
        return self.create_execution(query)

    def create_plan(self, query: Union[UserQuery, str]) -> InvestigationPlan:
        """Parse query and return structured InvestigationPlan."""
        raw_text = query.text if isinstance(query, UserQuery) else query
        ctx = PlannerContext(raw_query=raw_text)
        self._parse_query_with_metrics(ctx, raw_text)
        return ctx.investigation_plan

    def create_execution(self, query: Union[UserQuery, str]) -> PlanningResult:
        """Parse query and return PlanningResult containing plans, context, and metrics."""
        t_total_start = time.perf_counter()
        raw_text = query.text if isinstance(query, UserQuery) else query
        ctx = PlannerContext(raw_query=raw_text)

        # 1 & 2: LLM and Parser phase with timing metrics
        self._parse_query_with_metrics(ctx, raw_text)

        # 3: Execution Planner phase
        t_planner_start = time.perf_counter()
        ctx.execution_plan = self.execution_planner.plan(ctx.investigation_plan)
        t_planner_end = time.perf_counter()

        planner_ms = round((t_planner_end - t_planner_start) * 1000, 3)
        total_ms = round((t_planner_end - t_total_start) * 1000, 3)

        ctx.metrics["planner_ms"] = planner_ms
        ctx.metrics["total_ms"] = total_ms

        return PlanningResult(
            investigation_plan=ctx.investigation_plan,
            execution_plan=ctx.execution_plan,
            planner_context=ctx,
            metrics=ctx.metrics,
        )

    def _parse_query_with_metrics(self, ctx: PlannerContext, raw_text: str) -> None:
        """Internal helper to execute LLM inference and query parsing with microsecond profiling."""
        # LLM Phase
        t_llm_start = time.perf_counter()
        try:
            ctx.llm_response = self.llm_client.parse_query(raw_text)
            t_llm_end = time.perf_counter()
            llm_ms = round((t_llm_end - t_llm_start) * 1000, 3)

            # Parser Phase
            t_parser_start = time.perf_counter()
            ctx.investigation_plan = self.query_parser.parse_json(ctx.llm_response, raw_query=raw_text)
            t_parser_end = time.perf_counter()
            parser_ms = round((t_parser_end - t_parser_start) * 1000, 3)

        except (LLMClientError, PlannerError) as err:
            t_llm_end = time.perf_counter()
            llm_ms = round((t_llm_end - t_llm_start) * 1000, 3)
            logger.info(f"LLM Client / Parsing error, invoking fallback parser: {err}")
            ctx.validation_errors.append(str(err))

            t_parser_start = time.perf_counter()
            ctx.investigation_plan = self.query_parser.parse_text_rule_based(raw_text)
            t_parser_end = time.perf_counter()
            parser_ms = round((t_parser_end - t_parser_start) * 1000, 3)

        ctx.metrics["llm_ms"] = llm_ms
        ctx.metrics["parser_ms"] = parser_ms
