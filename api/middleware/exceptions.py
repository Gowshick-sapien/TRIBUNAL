"""Global Exception handling middleware and handlers for TRIBUNAL REST API."""

import datetime
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.schemas.common import ErrorResponse
from api.services.investigation_service import (
    InvalidQueryError,
    InvestigationExecutionError,
    InvestigationNotFoundError,
    ServiceError,
    UnsupportedQueryError,
)
from tribunal.data.dataset_resolver import DatasetNotFoundError
from storage.sqlite.sqlite_repository import (
    DatabaseUnavailableError,
    InvestigationAlreadyExistsError,
    PersistenceFailureError,
    StorageError,
)

logger = logging.getLogger("tribunal.api.middleware.exceptions")


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on FastAPI application."""

    @app.exception_handler(UnsupportedQueryError)
    async def unsupported_query_handler(request: Request, exc: UnsupportedQueryError) -> JSONResponse:
        logger.warning(f"Unsupported Domain Query Rejected: {exc}")
        payload = ErrorResponse(
            error="UnsupportedQuery",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload.model_dump())

    @app.exception_handler(DatasetNotFoundError)
    async def dataset_not_found_handler(request: Request, exc: DatasetNotFoundError) -> JSONResponse:
        logger.warning(f"Dataset Not Found: {exc}")
        details = {}
        if hasattr(exc, "searched_locations") and exc.searched_locations:
            details["searched_locations"] = exc.searched_locations
        if hasattr(exc, "hint") and exc.hint:
            details["hint"] = exc.hint
        if hasattr(exc, "dataset_ref") and exc.dataset_ref:
            details["dataset_reference"] = exc.dataset_ref

        payload = ErrorResponse(
            error="DatasetNotFound",
            message=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            details=details if details else None,
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

    @app.exception_handler(DatabaseUnavailableError)
    async def db_unavailable_handler(request: Request, exc: DatabaseUnavailableError) -> JSONResponse:
        logger.error(f"Database Unavailable: {exc}")
        payload = ErrorResponse(
            error="DatabaseUnavailable",
            message=str(exc),
            status_code=status.HTTP_533_SERVICE_UNAVAILABLE if hasattr(status, 'HTTP_533') else status.HTTP_503_SERVICE_UNAVAILABLE,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=payload.model_dump())

    @app.exception_handler(InvestigationAlreadyExistsError)
    async def already_exists_handler(request: Request, exc: InvestigationAlreadyExistsError) -> JSONResponse:
        logger.warning(f"Investigation Already Exists: {exc}")
        payload = ErrorResponse(
            error="InvestigationAlreadyExists",
            message=str(exc),
            status_code=status.HTTP_409_CONFLICT,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=payload.model_dump())

    @app.exception_handler(PersistenceFailureError)
    async def persistence_failure_handler(request: Request, exc: PersistenceFailureError) -> JSONResponse:
        logger.error(f"Persistence Failure: {exc}", exc_info=True)
        payload = ErrorResponse(
            error="PersistenceFailure",
            message=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump())

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
