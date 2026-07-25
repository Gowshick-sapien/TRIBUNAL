"""Global Exception handling middleware and handlers for TRIBUNAL REST API."""

import datetime
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.schemas.common import ErrorResponse
from api.services.investigation_service import (
    DatasetNotFoundError,
    InvalidQueryError,
    InvestigationExecutionError,
    InvestigationNotFoundError,
    ServiceError,
)

logger = logging.getLogger("tribunal.api.middleware.exceptions")


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on FastAPI application."""

    @app.exception_handler(DatasetNotFoundError)
    async def dataset_not_found_handler(request: Request, exc: DatasetNotFoundError) -> JSONResponse:
        logger.warning(f"Dataset Not Found: {exc}")
        payload = ErrorResponse(
            error="DatasetNotFound",
            message=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload.model_dump())

    @app.exception_handler(InvestigationNotFoundError)
    async def investigation_not_found_handler(request: Request, exc: InvestigationNotFoundError) -> JSONResponse:
        logger.warning(f"Investigation Not Found: {exc}")
        payload = ErrorResponse(
            error="InvestigationNotFound",
            message=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload.model_dump())

    @app.exception_handler(InvalidQueryError)
    async def invalid_query_handler(request: Request, exc: InvalidQueryError) -> JSONResponse:
        logger.warning(f"Invalid Query: {exc}")
        payload = ErrorResponse(
            error="InvalidQuery",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload.model_dump())

    @app.exception_handler(ServiceError)
    async def generic_service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
        logger.error(f"Service Error: {exc}", exc_info=True)
        payload = ErrorResponse(
            error="ServiceError",
            message=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        payload = ErrorResponse(
            error="InternalServerError",
            message="An unexpected internal server error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            details={"type": type(exc).__name__, "description": str(exc)},
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump())
