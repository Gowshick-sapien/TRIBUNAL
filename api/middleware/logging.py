"""Structured HTTP request logging middleware for TRIBUNAL REST API."""

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger("tribunal.api.middleware.logging")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests, status codes, and execution duration."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        logger.info(f"Incoming HTTP request: {method} {path} from {client_host}")

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(f"Completed HTTP response: {method} {path} status={response.status_code} duration={duration_ms}ms")
            return response
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(f"Failed HTTP request: {method} {path} error={exc} duration={duration_ms}ms")
            raise exc
