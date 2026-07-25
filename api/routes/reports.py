"""Report router exposing /report/{id} endpoint."""

from typing import Optional, Union
from fastapi import APIRouter, Depends, Header, Response, status

from api.dependencies import get_investigation_service
from api.schemas.common import ErrorResponse
from api.schemas.report import ReportResponse
from api.services.investigation_service import InvestigationService

router = APIRouter(prefix="", tags=["Reports"])


@router.get(
    "/report/{id}",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve investigation report",
    description="Returns full multi-format report by investigation ID. Respects Accept header ('text/markdown', 'application/json').",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation report not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_report(
    id: str,
    accept: Optional[str] = Header(default=None),
    service: InvestigationService = Depends(get_investigation_service),
) -> Union[ReportResponse, Response]:
    """Fetch report by investigation ID."""
    report_data = service.get_report(id)
    if accept and "text/markdown" in accept:
        return Response(content=report_data.markdown_content, media_type="text/markdown")
    return report_data
