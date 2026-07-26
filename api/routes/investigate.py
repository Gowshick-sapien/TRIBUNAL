"""Investigation router exposing /investigate, /query, /investigations, /investigation/{id} endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Response, status

from api.dependencies import get_investigation_service
from api.schemas.common import ErrorResponse
from api.schemas.investigation import (
    InvestigationDetailResponse,
    InvestigationListResponse,
    InvestigationRequest,
    InvestigationResponse,
    QueryRequest,
    QueryResponse,
)
from api.services.investigation_service import InvestigationService

router = APIRouter(prefix="", tags=["Investigation"])


@router.post(
    "/investigate",
    response_model=InvestigationResponse,
    status_code=status.HTTP_200_OK,
    summary="Primary investigation endpoint",
    description="Triggers full agentic investigation lifecycle and persists all execution artifacts atomically.",
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
    print("=" * 80)
    print("REQUEST RECEIVED")
    print(request.query)
    print("=" * 80)

    response = service.run_investigation(request)

    print("=" * 80)
    print("FINAL REPORT")
    print(response.report.summary if hasattr(response, "report") and response.report else response)
    print("=" * 80)

    return response


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


@router.get(
    "/investigations",
    response_model=InvestigationListResponse,
    status_code=status.HTTP_200_OK,
    summary="List persistent historical investigations",
    description="Returns a paginated list of historical persistent investigation metadata records.",
)
def list_investigations(
    limit: int = Query(default=50, ge=1, le=200, description="Max number of items"),
    offset: int = Query(default=0, ge=0, description="Offset index"),
    service: InvestigationService = Depends(get_investigation_service),
) -> InvestigationListResponse:
    """List historical investigations."""
    return service.list_investigations(limit=limit, offset=offset)


@router.get(
    "/investigation/{id}",
    response_model=InvestigationDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve investigation metadata detail",
    description="Fetches detailed investigation metadata and artifact URLs by ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation record not found"},
    },
)
def get_investigation_detail(
    id: str,
    service: InvestigationService = Depends(get_investigation_service),
) -> InvestigationDetailResponse:
    """Fetch complete investigation record metadata."""
    return service.get_investigation_detail(id)


@router.delete(
    "/investigation/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete persistent investigation",
    description="Deletes investigation metadata and files while retaining an immutable audit trail event.",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation record not found"},
    },
)
def delete_investigation(
    id: str,
    service: InvestigationService = Depends(get_investigation_service),
) -> Response:
    """Delete investigation by ID."""
    service.delete_investigation(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
