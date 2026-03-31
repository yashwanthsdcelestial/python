import time
import logging
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

Path("logs").mkdir(exist_ok=True)

app_logger = logging.getLogger("app")
if not app_logger.handlers:
    handler = logging.FileHandler("logs/app.log")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        app_logger.info(
            f"{request.method} {request.url.path} | {response.status_code} | {elapsed_ms:.0f}ms"
        )
        return response