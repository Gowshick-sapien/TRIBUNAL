"""Search REST API Router — Advanced Repository Explorer & Search endpoints."""

import datetime
import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query, Response, status
from pydantic import BaseModel, Field

from storage.repositories.search_repository import (
    SearchRepository,
    SearchResultItem,
    SimilarInvestigationItem,
)

router = APIRouter(prefix="", tags=["Repository Explorer & Search"])


class SearchResultSchema(BaseModel):
    """Schema describing an investigation search result item."""
    id: str
    created_at: str
    query: str
    dataset: str
    planner_intent: str
    risk_level: str
    confidence: float
    recommendation: str
    status: str
    duration_ms: float
    version: str
    winning_hypothesis: Optional[str] = None
    is_bookmarked: bool = False
    tags: List[str] = Field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0


class SearchResponse(BaseModel):
    """Response returned by GET /api/v1/search."""
    total: int = Field(..., description="Total count of matching investigations")
    limit: int = Field(..., description="Page limit")
    offset: int = Field(..., description="Page offset")
    results: List[SearchResultSchema] = Field(default_factory=list)


class SimilarItemSchema(BaseModel):
    """Schema for similar investigation result."""
    item: SearchResultSchema
    similarity_score: float
    similarity_reasons: List[str]


class SimilarListResponse(BaseModel):
    """Response returned by GET /api/v1/search/similar/{id}."""
    target_id: str
    similar: List[SimilarItemSchema]


class TagRequest(BaseModel):
    """Payload for tagging an investigation."""
    tag: str = Field(..., description="Tag text e.g. 'AML', 'Payroll', 'Escalated'")


@router.get(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Advanced Search & Filter Repository",
    description="Multi-criteria SQL search operating across persisted investigation metadata.",
)
def search_repository(
    query: Optional[str] = Query(None, description="Natural language search term"),
    risk_level: Optional[str] = Query("ALL", description="Risk level: ALL, CRITICAL, HIGH, MEDIUM, LOW"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence threshold"),
    max_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Maximum confidence threshold"),
    dataset: Optional[str] = Query("ALL", description="Dataset reference alias"),
    status_filter: Optional[str] = Query("ALL", alias="status", description="Status filter: ALL, COMPLETED, FAILED"),
    expert: Optional[str] = Query(None, description="Expert filter"),
    start_date: Optional[str] = Query(None, description="Start date ISO string"),
    end_date: Optional[str] = Query(None, description="End date ISO string"),
    only_bookmarked: bool = Query(False, description="Filter bookmarked items only"),
    sort_by: str = Query("newest", description="Sort order: newest, oldest, confidence_desc, risk_desc, fastest"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> SearchResponse:
    """Execute repository search."""
    repo = SearchRepository()
    items, total = repo.search(
        query=query,
        risk_level=risk_level,
        min_confidence=min_confidence,
        max_confidence=max_confidence,
        dataset=dataset,
        status=status_filter,
        expert=expert,
        start_date=start_date,
        end_date=end_date,
        only_bookmarked=only_bookmarked,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
    )
    schemas = [SearchResultSchema(**item.__dict__) for item in items]
    return SearchResponse(total=total, limit=limit, offset=offset, results=schemas)


@router.get(
    "/search/recent",
    response_model=List[SearchResultSchema],
    status_code=status.HTTP_200_OK,
    summary="Recent Investigations",
    description="Returns most recently executed investigations.",
)
def get_recent_investigations(limit: int = Query(10, ge=1, le=50)) -> List[SearchResultSchema]:
    """Retrieve recent investigations."""
    repo = SearchRepository()
    items = repo.get_recent(limit=limit)
    return [SearchResultSchema(**item.__dict__) for item in items]


@router.get(
    "/search/bookmarks",
    response_model=List[SearchResultSchema],
    status_code=status.HTTP_200_OK,
    summary="Bookmarked Investigations",
    description="Returns bookmarked investigation items.",
)
def get_bookmarked_investigations() -> List[SearchResultSchema]:
    """Retrieve bookmarked investigations."""
    repo = SearchRepository()
    items = repo.get_bookmarked()
    return [SearchResultSchema(**item.__dict__) for item in items]


@router.post(
    "/search/bookmarks/{id}",
    status_code=status.HTTP_200_OK,
    summary="Toggle Investigation Bookmark",
    description="Toggles bookmark status for a target investigation ID.",
)
def toggle_bookmark(id: str, notes: Optional[str] = None) -> Dict[str, Any]:
    """Toggle bookmark."""
    repo = SearchRepository()
    is_bookmarked = repo.toggle_bookmark(id, notes=notes)
    return {"id": id, "is_bookmarked": is_bookmarked}


@router.get(
    "/search/similar/{id}",
    response_model=SimilarListResponse,
    status_code=status.HTTP_200_OK,
    summary="Similar Investigations Engine",
    description="Ranks historical investigations by metadata similarity to target investigation ID.",
)
def get_similar_investigations(
    id: str,
    limit: int = Query(5, ge=1, le=20),
) -> SimilarListResponse:
    """Retrieve similar investigations."""
    repo = SearchRepository()
    sim_items = repo.get_similar(id, limit=limit)
    schemas = [
        SimilarItemSchema(
            item=SearchResultSchema(**s.item.__dict__),
            similarity_score=s.similarity_score,
            similarity_reasons=s.similarity_reasons,
        )
        for s in sim_items
    ]
    return SimilarListResponse(target_id=id, similar=schemas)


@router.post(
    "/search/tags/{id}",
    status_code=status.HTTP_200_OK,
    summary="Add Tag Annotation",
    description="Adds a user tag to an investigation record.",
)
def add_tag(id: str, req: TagRequest) -> Dict[str, Any]:
    """Add user tag."""
    repo = SearchRepository()
    success = repo.add_tag(id, req.tag)
    return {"id": id, "tag": req.tag, "success": success}


@router.delete(
    "/search/tags/{id}",
    status_code=status.HTTP_200_OK,
    summary="Remove Tag Annotation",
    description="Removes a user tag from an investigation record.",
)
def remove_tag(id: str, tag: str) -> Dict[str, Any]:
    """Remove user tag."""
    repo = SearchRepository()
    success = repo.remove_tag(id, tag)
    return {"id": id, "tag": tag, "success": success}


@router.get(
    "/search/export",
    summary="Export Search Results",
    description="Exports search results as CSV or JSON file download.",
)
def export_search_results(
    query: Optional[str] = Query(None),
    risk_level: Optional[str] = Query("ALL"),
    dataset: Optional[str] = Query("ALL"),
    format_type: str = Query("csv", alias="format", description="Export format: csv or json"),
) -> Response:
    """Export search results as file."""
    repo = SearchRepository()
    items, _ = repo.search(query=query, risk_level=risk_level, dataset=dataset, limit=500)

    if format_type.lower() == "json":
        json_data = [item.__dict__ for item in items]
        return Response(
            content=json.dumps(json_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="tribunal_search_results.json"'},
        )
    else:
        csv_data = repo.export_csv(items)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="tribunal_search_results.csv"'},
        )
