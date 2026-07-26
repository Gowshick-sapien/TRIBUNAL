"""Report REST API Router — Multi-format investigation reports & Investigator annotations."""

import json
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Depends, Header, Query, Response, status
from pydantic import BaseModel, Field

from api.dependencies import get_investigation_service
from api.schemas.common import ErrorResponse
from api.schemas.report import ReportResponse
from api.services.investigation_service import InvestigationService
from storage.repositories.report_repository import (
    ReportAnnotationRepository,
    render_compliance_html,
)

router = APIRouter(prefix="", tags=["Reports"])


class AnnotationRequest(BaseModel):
    """Payload for adding an investigator note annotation."""
    author: Optional[str] = Field(default="Investigator", description="Author name or role")
    text: str = Field(..., description="Note text e.g. 'Needs SAR review'")


class AnnotationSchema(BaseModel):
    """Schema representing an investigator note annotation."""
    id: int
    investigation_id: str
    author: str
    text: str
    created_at: str


@router.get(
    "/report/{id}",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve investigation report",
    description="Returns full multi-format report by investigation ID. Supports format parameter (markdown, html, pdf, json) and Accept headers.",
    responses={
        404: {"model": ErrorResponse, "description": "Investigation report not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
@router.get(
    "/reports/{id}",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def get_report(
    id: str,
    format_type: Optional[str] = Query(None, alias="format", description="Export format: markdown, html, pdf, json"),
    accept: Optional[str] = Header(default=None),
    service: InvestigationService = Depends(get_investigation_service),
) -> Union[ReportResponse, Response]:
    """Fetch report by investigation ID with multi-format content negotiation."""
    report_data = service.get_report(id)

    fmt = (format_type or "").lower()

    if fmt == "markdown" or (accept and "text/markdown" in accept):
        return Response(
            content=report_data.markdown_content,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="report_{id}.md"'},
        )
    elif fmt == "html" or fmt == "pdf" or (accept and "text/html" in accept):
        metadata = {
            "risk_level": report_data.risk_level,
            "confidence": getattr(report_data, "confidence", 0.0),
            "generated_at": report_data.generated_at,
        }
        html_out = render_compliance_html(id, "TRIBUNAL Report", report_data.markdown_content, metadata)
        filename = f"report_{id}.html" if fmt != "pdf" else f"report_{id}_print.html"
        return Response(
            content=html_out,
            media_type="text/html",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
    elif fmt == "json":
        return Response(
            content=json.dumps(report_data.json_payload or report_data.model_dump(), indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="report_{id}.json"'},
        )

    return report_data


@router.get(
    "/reports/{id}/annotations",
    response_model=List[AnnotationSchema],
    status_code=status.HTTP_200_OK,
    summary="Get investigator note annotations",
    description="Returns investigator notes attached to target investigation report.",
)
def get_annotations(id: str) -> List[AnnotationSchema]:
    """Get report annotations."""
    repo = ReportAnnotationRepository()
    items = repo.get_annotations(id)
    return [AnnotationSchema(**item.__dict__) for item in items]


@router.post(
    "/reports/{id}/annotations",
    response_model=AnnotationSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add investigator note annotation",
    description="Attaches a new investigator note annotation to a report without modifying original report data.",
)
def add_annotation(id: str, req: AnnotationRequest) -> AnnotationSchema:
    """Add report annotation."""
    repo = ReportAnnotationRepository()
    item = repo.add_annotation(id, req.author or "Investigator", req.text)
    if not item:
        return Response(status_code=400, content="Invalid annotation text")
    return AnnotationSchema(**item.__dict__)


@router.delete(
    "/reports/{id}/annotations/{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete investigator note annotation",
    description="Removes an investigator note annotation by ID.",
)
def delete_annotation(id: str, note_id: int) -> Dict[str, Any]:
    """Delete report annotation."""
    repo = ReportAnnotationRepository()
    success = repo.delete_annotation(note_id)
    return {"id": id, "note_id": note_id, "success": success}
