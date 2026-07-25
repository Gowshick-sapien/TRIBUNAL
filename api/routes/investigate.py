"""Investigation router exposing /investigate and /query endpoints."""

from fastapi import APIRouter, Depends, status

from api.dependencies import get_investigation_service
from api.schemas.common import ErrorResponse
from api.schemas.investigation import InvestigationRequest, InvestigationResponse, QueryRequest, QueryResponse
from api.services.investigation_service import InvestigationService

router = APIRouter(prefix="", tags=["Investigation"])


@router.post(
    "/investigate",
    response_model=InvestigationResponse,
    status_code=status.HTTP_200_OK,
    summary="Primary investigation endpoint",
    description="Triggers full agentic investigation lifecycle: Planning -> Domain Experts -> Graph Builder -> Defense -> Tribunal -> Report.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query or parameters"},
        404: {"model": ErrorResponse, "description": "Dataset not found"},
        500: {"model": ErrorResponse, "description": "Internal engine failure"},
    },
)
def run_investigation(
    request: InvestigationRequest,
    service: InvestigationService = Depends(get_investigation_service),
) -> InvestigationResponse:
    """Execute complete TRIBUNAL investigation."""
    return service.run_investigation(request)


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Lightweight conversational query endpoint",
    description="Fast conversational endpoint returning concise investigation results and short answers.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query or parameters"},
        404: {"model": ErrorResponse, "description": "Dataset not found"},
        500: {"model": ErrorResponse, "description": "Internal engine failure"},
    },
)
def run_query(
    request: QueryRequest,
    service: InvestigationService = Depends(get_investigation_service),
) -> QueryResponse:
    """Execute lightweight conversational query."""
    return service.run_query(request)
