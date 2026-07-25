"""Health check router exposing /health endpoint."""

import datetime
import time
from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from api.dependencies import get_investigation_service
from api.services.investigation_service import InvestigationService

router = APIRouter(prefix="", tags=["System & Health"])

SERVER_START_TIME = time.time()


class HealthResponse(BaseModel):
    """Health status response payload."""
    status: str = Field("healthy", description="Service status (healthy, degraded, unhealthy)")
    version: str = Field("1.0.0", description="Application release version")
    api_version: str = Field("v1", description="REST API version")
    uptime_seconds: float = Field(..., description="Server uptime in seconds")
    planner_ready: bool = Field(True, description="Whether Planner module is operational")
    engine_ready: bool = Field(True, description="Whether Investigation Engine is operational")
    timestamp: str = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Current UTC timestamp"
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="System Health & Status",
    description="Returns runtime system health status, uptime, and component readiness.",
)
def get_health(
    service: InvestigationService = Depends(get_investigation_service),
) -> HealthResponse:
    """Retrieve system health indicators."""
    uptime = round(time.time() - SERVER_START_TIME, 2)
    planner_ready = service.planner is not None
    engine_ready = service.tribunal is not None and service.financial_expert is not None

    return HealthResponse(
        status="healthy" if (planner_ready and engine_ready) else "degraded",
        version="1.0.0",
        api_version="v1",
        uptime_seconds=uptime,
        planner_ready=planner_ready,
        engine_ready=engine_ready,
    )
