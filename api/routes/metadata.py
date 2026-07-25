"""Metadata router exposing /metadata endpoint."""

import datetime
from typing import Any, Dict, List
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="", tags=["System & Health"])


class MetadataResponse(BaseModel):
    """Platform metadata response schema."""
    title: str = Field("TRIBUNAL Investigation Engine Platform", description="Platform title")
    version: str = Field("1.0.0", description="Engine version")
    api_version: str = Field("v1", description="REST API version")
    supported_experts: List[str] = Field(
        default_factory=lambda: ["financial", "behaviour"],
        description="Supported domain investigator experts"
    )
    supported_aml_patterns: List[str] = Field(
        default_factory=lambda: [
            "structuring",
            "velocity",
            "large_transfer",
            "frequency",
            "behaviour_drift",
            "counterparty_behaviour",
            "currency_change",
            "dormancy",
            "payment_pattern",
            "spending_pattern",
        ],
        description="Supported AML pattern detection algorithms"
    )
    build_information: Dict[str, Any] = Field(
        default_factory=lambda: {
            "environment": "production",
            "framework": "FastAPI",
            "phase": "D.1 — Investigation Service Layer & REST API",
        },
        description="Build metadata"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Response timestamp"
    )


@router.get(
    "/metadata",
    response_model=MetadataResponse,
    status_code=status.HTTP_200_OK,
    summary="Platform & Engine Metadata",
    description="Returns platform capability metadata, supported experts, and AML pattern detection algorithms.",
)
def get_metadata() -> MetadataResponse:
    """Retrieve platform metadata capabilities."""
    return MetadataResponse()
