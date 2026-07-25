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


class InvestigationRecordSchema(BaseModel):
    """Schema representing an investigation record item in list responses."""
    id: str = Field(..., description="Unique investigation ID")
    query: str = Field(..., description="Original query")
    dataset: str = Field(..., description="Dataset reference")
    created_at: str = Field(..., description="ISO creation timestamp")
    planner_intent: str = Field(..., description="Parsed planner intent")
    risk_level: str = Field(..., description="Risk level")
    confidence: float = Field(..., description="Confidence score")
    recommendation: str = Field(..., description="Recommendation")
    status: str = Field(..., description="Execution status")
    duration_ms: float = Field(..., description="Execution duration in milliseconds")
    version: str = Field("1.0.0", description="Record schema version")


class InvestigationListResponse(BaseModel):
    """Paginated list of persistent investigation records."""
    total: int = Field(..., description="Total count of items returned")
    limit: int = Field(..., description="Page limit")
    offset: int = Field(..., description="Page offset")
    investigations: List[InvestigationRecordSchema] = Field(default_factory=list, description="List of investigation records")


class InvestigationDetailResponse(BaseModel):
    """Detailed investigation record response including artifact URLs."""
    record: InvestigationRecordSchema = Field(..., description="Core investigation record metadata")
    report_url: str = Field(..., description="URL path to report artifact")
    graph_url: str = Field(..., description="URL path to graph artifact")
    verdict_url: str = Field(..., description="URL path to verdict artifact")
    has_case_file: bool = Field(False, description="Whether case file artifact is persisted")
