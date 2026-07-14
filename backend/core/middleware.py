import time
import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
from core.config import settings
from core.redis_client import get_redis

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.redis = get_redis()
        
    async def dispatch(self, request: Request, call_next):
        # 1. Request Size Limits (100 MB max for file uploads)
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 100 * 1024 * 1024:
            return JSONResponse(status_code=413, content={"detail": "Payload Too Large"})

        # 2. Redis-based Rate Limiting (Production)
        client_ip = request.client.host
        path = request.url.path
        
        # Rate limit only API endpoints, not health checks
        if path.startswith("/api/v1/"):
            try:
                redis_key = f"rate_limit:{client_ip}"
                # Redis rate limiting: Increment and set expire if new
                current_requests = self.redis.incr(redis_key)
                if current_requests == 1:
                    self.redis.expire(redis_key, 60) # 1 minute window
                
                if current_requests > self.rate_limit:
                    return JSONResponse(status_code=429, content={"detail": "Too many requests"})
            except Exception as e:
                # Fallback gracefully if Redis is temporarily unreachable
                pass

        # 3. Security Headers (Helmet Equivalent)
        response = await call_next(request)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
