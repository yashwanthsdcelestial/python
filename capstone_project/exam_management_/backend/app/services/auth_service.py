import logging
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.models.models import User

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserRegisterRequest) -> User:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed = get_password_hash(data.password)
        user = self.repo.create(
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
            role=data.role,
        )
        logger.info(f"Registered new user: {user.email}")
        return user

    def login(self, data: UserLoginRequest) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        access_token = create_access_token(
            subject=user.id,
            extra_data={"role": user.role, "email": user.email},
        )
        refresh_token = create_refresh_token(subject=user.id)
        logger.info(f"User logged in: {user.email}")
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )
        user_id = payload.get("sub")
        user = self.repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        access_token = create_access_token(
            subject=user.id,
            extra_data={"role": user.role, "email": user.email},
        )
        new_refresh = create_refresh_token(subject=user.id)
        return TokenResponse(access_token=access_token, refresh_token=new_refresh)
