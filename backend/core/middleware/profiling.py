import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)

class EnterpriseProfilerMiddleware(BaseHTTPMiddleware):
    """
    Globally profiles every REST API endpoint in the platform.
    Automatically logs endpoints that breach Service Level Agreement (SLA) thresholds.
    """
    def __init__(self, app, slow_threshold_ms: float = 500.0):
        super().__init__(app)
        self.slow_threshold_ms = slow_threshold_ms

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Execute Request
        response = await call_next(request)
        
        process_time_ms = (time.time() - start_time) * 1000
        
        # Inject standard telemetry header
        response.headers["X-Process-Time-Ms"] = str(round(process_time_ms, 2))
        
        # Bottleneck detection
        if process_time_ms > self.slow_threshold_ms:
            logger.warning(
                f"[SLA BREACH] Endpoint {request.method} {request.url.path} "
                f"took {process_time_ms:.2f}ms (Threshold: {self.slow_threshold_ms}ms)"
            )
        else:
            logger.debug(f"{request.method} {request.url.path} executed in {process_time_ms:.2f}ms")
            
        return response
