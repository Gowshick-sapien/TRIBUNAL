"""Report response schemas for TRIBUNAL REST API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ReportSectionSchema(BaseModel):
    """Schema for individual sections within an investigation report."""
    title: str = Field(..., description="Section title")
    order: int = Field(..., description="Section display index")
    content: str = Field(..., description="Markdown or text content of section")


class ReportResponse(BaseModel):
    """Structured report output payload."""
    report_id: str = Field(..., description="Unique report ID")
    investigation_id: str = Field(..., description="Associated investigation ID")
    generated_at: str = Field(..., description="ISO timestamp when report was generated")
    version: str = Field(default="1.0.0", description="Report spec version")
    markdown_content: str = Field(..., description="Full report in Markdown format")
    html_content: Optional[str] = Field(default=None, description="Full report rendered in HTML")
    sections: List[ReportSectionSchema] = Field(default_factory=list, description="Structured 10-section breakdown")
    json_payload: Dict[str, Any] = Field(default_factory=dict, description="Raw structured JSON report payload")
    risk_level: str = Field(default="MEDIUM", description="Assessed risk level")
    recommendation: str = Field(default="", description="Executive recommendation")
