"""Graph and Verdict router exposing /graph/{id} and /verdict/{id} endpoints."""

from fastapi import APIRouter, Depends, status

from api.dependencies import get_investigation_service
from api.schemas.common import ErrorResponse
from api.schemas.graph import GraphResponse, VerdictResponse
from api.services.investigation_service import InvestigationService

router = APIRouter(prefix="", tags=["Graph & Verdict"])


@router.get(
    "/graph/{id}",
    response_model=GraphResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Evidence Graph",
    description="Returns serialized node-edge Evidence Graph for visualization and network analysis.",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation or graph not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_graph(
    id: str,
    service: InvestigationService = Depends(get_investigation_service),
) -> GraphResponse:
    """Fetch Evidence Graph by investigation ID."""
    return service.get_graph(id)


@router.get(
    "/verdict/{id}",
    response_model=VerdictResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Tribunal Verdict",
    description="Returns concise Tribunal consensus verdict, confidence, margin, and deliberation trace.",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation or verdict not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_verdict(
    id: str,
    service: InvestigationService = Depends(get_investigation_service),
) -> VerdictResponse:
    """Fetch Tribunal Verdict by investigation ID."""
    return service.get_verdict(id)
