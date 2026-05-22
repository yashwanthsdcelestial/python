import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import auth, exams, attempts, admin, enrollments
from app.core.config import settings
from app.db.session import engine, Base
from app.middleware.logging import RequestLoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Online Exam Management System")
    yield
    logger.info("Shutting down Online Exam Management System")


app = FastAPI(
    title="Online Exam Management System",
    description="""
    A full-stack web application managing the complete lifecycle of online examinations.
    
    ## Features
    - JWT Authentication with RBAC (Admin / Student)
    - Exam creation and management (Admin)
    - Student enrollment and timed exam attempts
    - Automated scoring and result history
    - Background task notifications
    """,
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Auth", "description": "Registration, login, token refresh"},
        {"name": "Exams", "description": "Browse and manage exams"},
        {"name": "Enrollments", "description": "Enroll in exams"},
        {"name": "Attempts", "description": "Start, submit, and view exam attempts"},
        {"name": "Admin", "description": "Admin-only management endpoints"},
    ],
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(exams.router, prefix="/api/exams", tags=["Exams"])
app.include_router(enrollments.router, prefix="/api/enrollments", tags=["Enrollments"])
app.include_router(attempts.router, prefix="/api/attempts", tags=["Attempts"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Online Exam Management System API"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
