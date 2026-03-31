"""Logging middleware for HTTP requests/responses."""
import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Log request details and response status.
        
        Args:
            request: HTTP request
            call_next: Next middleware/route handler
        
        Returns:
            HTTP response
        """
        # Log request
        start_time = time.time()
        
        # Get request details
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params) if request.query_params else {}
        
        logger.info(f"📨 {method} {path} | Params: {query_params}")
        
        try:
            # Call next middleware/route
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            status_code = response.status_code
            status_emoji = "✅" if 200 <= status_code < 300 else "⚠️" if 400 <= status_code < 500 else "❌"
            
            logger.info(f"{status_emoji} {method} {path} | Status: {status_code} | Time: {process_time:.3f}s")
            
            return response
            
        except Exception as e:
            # Log errors
            process_time = time.time() - start_time
            logger.error(f"❌ {method} {path} | Error: {str(e)} | Time: {process_time:.3f}s")
            raise
