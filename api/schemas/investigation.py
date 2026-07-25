"""Investigation request and response schemas for TRIBUNAL REST API."""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from api.schemas.common import ExecutionOptions


class InvestigationRequest(BaseModel):
    """Primary request payload for triggering a full TRIBUNAL investigation."""
    query: str = Field(..., description="Natural language query or investigation objective")
    dataset: str = Field(default="default", description="Reference identifier or path for dataset")
    options: ExecutionOptions = Field(default_factory=ExecutionOptions, description="Execution parameters")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Client-provided metadata")


class InvestigationResponse(BaseModel):
    """Response payload returned upon completing a full investigation."""
    investigation_id: str = Field(..., description="Unique investigation tracking ID")
    query: str = Field(..., description="Original user query")
    risk_level: str = Field(..., description="Assessed risk level (CRITICAL, HIGH, MEDIUM, LOW)")
    confidence: float = Field(..., description="Calibrated confidence score (0.0 - 1.0)")
    verdict: str = Field(..., description="Final tribunal verdict classification")
    winning_hypothesis: str = Field(..., description="Primary hypothesis selected by Tribunal")
    recommendation: str = Field(..., description="Actionable recommendation")
    summary: str = Field(..., description="Executive summary of investigation findings")
    report_url: str = Field(..., description="API URL path to fetch complete report")
    graph_url: str = Field(..., description="API URL path to fetch evidence graph")
    verdict_url: str = Field(..., description="API URL path to fetch detailed verdict")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Execution performance metrics (ms)")
    created_at: str = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Timestamp of investigation completion"
    )


class QueryRequest(BaseModel):
    """Lightweight conversational query request."""
    query: str = Field(..., description="Conversational query (e.g., 'Is customer 541 suspicious?')")
    dataset: str = Field(default="default", description="Dataset identifier")


class QueryResponse(BaseModel):
    """Lightweight response for conversational queries."""
    query: str = Field(..., description="Original query")
    verdict: str = Field(..., description="Consensus verdict classification")
    risk_level: str = Field(..., description="Assessed risk level")
    confidence: float = Field(..., description="Confidence score")
    winning_hypothesis: str = Field(..., description="Winning hypothesis")
    recommendation: str = Field(..., description="Actionable advice")
    short_answer: str = Field(..., description="Concise investigation answer")
    invoked_experts: List[str] = Field(default_factory=list, description="Experts invoked during query processing")
