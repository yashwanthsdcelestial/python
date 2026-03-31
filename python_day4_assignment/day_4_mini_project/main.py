import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import settings
from database import engine, SessionLocal, verify_connection
from models import db_models  # noqa: F401 — ensures tables are imported before create_all
from middleware.logging_middleware import LoggingMiddleware
from exceptions.custom_exceptions import register_exception_handlers
from routers.auth_router import router as auth_router
from routers.loan_router import router as loan_router
from routers.admin_router import router as admin_router
from routers.analytics_router import router as analytics_router
from services.user_service import UserService

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify DB connection with @retry
    verify_connection(engine)

    # Seed admin user
    db = SessionLocal()
    try:
        UserService(db).seed_admin(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            email=settings.ADMIN_EMAIL,
        )
    finally:
        db.close()

    logger.info(f"{settings.APP_NAME} startup complete.")
    yield
    logger.info(f"{settings.APP_NAME} shutdown.")


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

# Middleware
app.add_middleware(LoggingMiddleware)

# Exception handlers
register_exception_handlers(app)


# Pydantic validation error → standard format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": str(exc.errors()),
            "status_code": 422,
        },
    )


# Health check
@app.get("/health", tags=["Utility"])
def health_check():
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "app": settings.APP_NAME}


# Mount routers
app.include_router(auth_router)
app.include_router(loan_router)
app.include_router(admin_router)
app.include_router(analytics_router)