"""Graph and verdict response schemas for TRIBUNAL REST API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NodeSchema(BaseModel):
    """Evidence graph node representation."""
    id: str = Field(..., description="Unique node identifier")
    label: str = Field(..., description="Display label")
    type: str = Field(..., description="Node category (account, entity, pattern, card)")
    expert: Optional[str] = Field(default="system", description="Source expert identifier (financial, behaviour, defense, system, tribunal)")
    risk_score: float = Field(default=0.0, description="Risk or confidence score (0.0 - 1.0)")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom node attributes")



class EdgeSchema(BaseModel):
    """Evidence graph directed edge representation."""
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    relation: str = Field(..., description="Relationship label")
    weight: float = Field(default=1.0, description="Edge weight or strength")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom edge attributes")


class GraphStatsSchema(BaseModel):
    """Evidence graph topological statistics."""
    node_count: int = Field(..., description="Total number of nodes")
    edge_count: int = Field(..., description="Total number of edges")
    density: float = Field(default=0.0, description="Graph edge density")
    pattern_clusters: int = Field(default=0, description="Number of identified pattern subgraphs")


class GraphResponse(BaseModel):
    """Serialized Evidence Graph payload for visualization tools."""
    investigation_id: str = Field(..., description="Associated investigation ID")
    nodes: List[NodeSchema] = Field(default_factory=list, description="List of graph nodes")
    edges: List[EdgeSchema] = Field(default_factory=list, description="List of graph edges")
    statistics: GraphStatsSchema = Field(..., description="Graph metrics summary")


class VerdictResponse(BaseModel):
    """Concise Tribunal Verdict response schema."""
    investigation_id: str = Field(..., description="Associated investigation ID")
    verdict: str = Field(..., description="Final verdict (LIKELY_MALICIOUS, POSSIBLY_MALICIOUS, LIKELY_LEGITIMATE, INCONCLUSIVE)")
    winning_hypothesis: str = Field(..., description="Winning primary hypothesis")
    winning_score: float = Field(..., description="Score of winning hypothesis")
    confidence: float = Field(..., description="Overall calibrated confidence")
    confidence_gap: float = Field(default=0.0, description="Margin between winning and runner-up hypothesis")
    runner_up_hypothesis: Optional[str] = Field(default=None, description="Runner-up alternative hypothesis")
    runner_up_confidence: Optional[float] = Field(default=None, description="Confidence of runner-up hypothesis")
    recommendation: str = Field(..., description="Actionable recommendation")
    deliberation_trace: List[Dict[str, Any]] = Field(default_factory=list, description="Step-by-step Tribunal deliberation log")
    reasoning_metadata: Dict[str, Any] = Field(default_factory=dict, description="Supporting expert and evidence metadata")
