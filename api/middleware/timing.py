"""Request timing middleware for TRIBUNAL REST API."""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Measures total request processing latency and attaches X-Response-Time-Ms header."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 3)
        response.headers["X-Response-Time-Ms"] = str(duration_ms)
        return response
