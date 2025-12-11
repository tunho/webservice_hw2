import time
import logging
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from collections import defaultdict
from datetime import datetime, timedelta

# Configure structured logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        log_dict = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "client_ip": request.client.host if request.client else "unknown",
            "duration_ms": round(process_time * 1000, 2)
        }
        
        # Log as JSON
        logger.info(json.dumps(log_dict))
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow()
        
        # Filter out old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > now - timedelta(seconds=self.window_seconds)
        ]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.max_requests:
            return Response(
                content=json.dumps({
                    "timestamp": now.isoformat(),
                    "path": request.url.path,
                    "status": 429,
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests"
                }),
                status_code=429,
                media_type="application/json"
            )
            
        # Add current request
        self.requests[client_ip].append(now)
        
        return await call_next(request)
