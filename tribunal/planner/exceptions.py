"""Exceptions hierarchy for TRIBUNAL planner module."""

from __future__ import annotations


class PlannerError(Exception):
    """Base exception for all errors in the planner module."""
    pass


class LLMClientError(PlannerError):
    """Raised when LLM client fails to communicate, times out, or returns empty response."""
    pass


class QueryParseError(PlannerError):
    """Raised when query output cannot be parsed as valid JSON or is malformed."""
    pass


class ValidationError(PlannerError):
    """Raised when query components (intent, pattern, output, filters) fail validation."""
    pass


class ExecutionPlannerError(PlannerError):
    """Raised when deterministic execution planning fails."""
    pass
