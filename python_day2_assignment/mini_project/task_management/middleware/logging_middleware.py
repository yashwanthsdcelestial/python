"""Logging middleware for request/response tracking."""
import time
from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and log details."""
        start_time = time.time()
        
        # Extract request info
        method = request.method
        path = request.url.path
        
        # Process request
        response: Response = await call_next(request)
        
        # Calculate timing
        duration_ms = (time.time() - start_time) * 1000
        
        # Log the entry
        log_message = f"{method} {path} | {response.status_code} | {duration_ms:.0f}ms"
        logger.info(log_message)
        
        return response
