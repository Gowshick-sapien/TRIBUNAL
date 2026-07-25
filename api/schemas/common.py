"""Common schemas for TRIBUNAL REST API."""

from __future__ import annotations

import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ExecutionOptions(BaseModel):
    """Configuration options for investigation execution."""
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence threshold for findings")
    max_depth: int = Field(default=3, ge=1, le=10, description="Maximum traversal depth for transaction networks")
    include_graph: bool = Field(default=True, description="Whether to compute and include Evidence Graph")
    include_raw_transactions: bool = Field(default=False, description="Whether to include raw transaction data in response")
    expert_override: Optional[list[str]] = Field(default=None, description="Optional explicit list of domain experts to invoke")


class ErrorResponse(BaseModel):
    """Standardized JSON error payload."""
    error: str = Field(..., description="Error type identifier")
    message: str = Field(..., description="Human-readable error description")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: str = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of the error"
    )
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional detailed error context")
