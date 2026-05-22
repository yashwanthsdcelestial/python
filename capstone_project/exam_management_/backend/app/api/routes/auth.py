import logging
from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.dependencies import get_current_user, get_db
from app.schemas.schemas import (
    UserRegisterRequest, UserLoginRequest, TokenResponse,
    UserResponse, RefreshTokenRequest,
)
from app.services.auth_service import AuthService
from app.utils.notifications import send_registration_welcome

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Register a new user",
    description="Create a new account with email, password, full name, and role (admin or student).",
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def register(
    request: Request,
    data: UserRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    user = service.register(data)
    background_tasks.add_task(send_registration_welcome, email=user.email, name=user.full_name)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get tokens",
    description="Authenticate with email and password. Returns access and refresh JWT tokens.",
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login(
    request: Request,
    data: UserLoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.login(data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Use a valid refresh token to get a new access token.",
)
async def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.refresh(data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(current_user=Depends(get_current_user)):
    return current_user
