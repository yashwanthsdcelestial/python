"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.custom_exceptions import TaskManagementException
from routers import user_router, task_router
from middleware.logging_middleware import LoggingMiddleware
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup event
    logger.info(f"✅ {settings.app_name} started | Debug: {settings.debug}")
    yield
    # Shutdown event
    logger.info(f"🛑 {settings.app_name} shutdown")


# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(LoggingMiddleware)


# Global exception handlers
@app.exception_handler(TaskManagementException)
async def task_management_exception_handler(request: Request, exc: TaskManagementException):
    """Handle custom TaskManagement exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )


# Include routers
app.include_router(user_router.router)
app.include_router(task_router.router)


@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "debug": settings.debug
    }


@app.get("/", status_code=200)
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
