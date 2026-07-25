"""FastAPI Application Entry Point for TRIBUNAL REST API & Service Layer."""

from __future__ import annotations

import logging
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.middleware.exceptions import register_exception_handlers
from api.middleware.logging import RequestLoggingMiddleware
from api.middleware.timing import RequestTimingMiddleware
from api.routes.graph import router as graph_router
from api.routes.health import router as health_router
from api.routes.investigate import router as investigate_router
from api.routes.metadata import router as metadata_router
from api.routes.reports import router as reports_router

logger = logging.getLogger("tribunal.api")


def create_app() -> FastAPI:
    """Construct and configure the TRIBUNAL FastAPI application instance."""
    app = FastAPI(
        title="TRIBUNAL Investigation Engine API",
        description=(
            "Phase D.1 Investigation Service Layer & REST API. "
            "Exposes multi-expert agentic investigation capabilities, evidence graph generation, "
            "adversarial tribunal consensus, and explainable report generation."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # 1. Register CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Register Logging & Timing Middlewares
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestTimingMiddleware)

    # 3. Register Custom Exception Handlers
    register_exception_handlers(app)

    # 4. Construct Versioned API Router (/api/v1)
    v1_router = APIRouter(prefix="/api/v1")
    v1_router.include_router(investigate_router)
    v1_router.include_router(reports_router)
    v1_router.include_router(graph_router)
    v1_router.include_router(health_router)
    v1_router.include_router(metadata_router)

    app.include_router(v1_router)

    @app.get("/", tags=["System & Health"])
    def root():
        """Root API welcome & discovery endpoint."""
        return {
            "name": "TRIBUNAL Investigation Engine REST API",
            "version": "1.0.0",
            "api_version": "v1",
            "documentation": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json",
        }

    return app


app = create_app()
