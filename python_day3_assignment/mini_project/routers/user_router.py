"""User router - handles user HTTP requests/responses (SRP)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.schemas import UserCreate, UserLogin, UserResponse
from models.db_models import User as UserModel
from services.user_service import UserService
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from database import get_db
from exceptions.custom_exceptions import (
    TaskManagementException, DuplicateUserError, InvalidCredentialsError
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyRepository:
    """Dependency injection for user repository."""
    return SQLAlchemyRepository(UserModel, db)


def get_user_service(repo: SQLAlchemyRepository = Depends(get_user_repository)) -> UserService:
    """Dependency injection for user service."""
    return UserService(repo)


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Register a new user."""
    try:
        return service.register(user_data)
    except DuplicateUserError as e:
        logger.warning(f"Registration failed: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/login", response_model=UserResponse)
async def login_user(
    login_data: UserLogin,
    service: UserService = Depends(get_user_service)
):
    """Login a user."""
    try:
        return service.login(login_data)
    except InvalidCredentialsError as e:
        logger.warning(f"Login failed: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("", response_model=list[UserResponse])
async def list_users(service: UserService = Depends(get_user_service)):
    """List all users."""
    try:
        users = service.list_users()
        logger.info(f"Listed {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    try:
        return service.get_user(user_id)
    except TaskManagementException as e:
        logger.error(f"Error getting user: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{user_id}", status_code=200)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete user by ID."""
    try:
        service.delete_user(user_id)
        return {"message": f"User {user_id} deleted successfully"}
    except TaskManagementException as e:
        logger.error(f"Error deleting user: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
