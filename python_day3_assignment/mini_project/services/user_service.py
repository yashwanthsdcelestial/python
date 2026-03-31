"""User service with business logic (SRP)."""
from datetime import datetime
from typing import List, Optional
from repositories.base_repository import BaseRepository
from models.schemas import UserCreate, UserLogin, UserResponse
from exceptions.custom_exceptions import (
    UserNotFoundError, DuplicateUserError, InvalidCredentialsError
)
from utils.security import hash_password, verify_password
from utils.logger import setup_logger

logger = setup_logger(__name__)


class UserService:
    """User service - handles all user business logic (SRP + DIP)."""
    
    def __init__(self, repository: BaseRepository):
        """Initialize with injected repository (DIP)."""
        self.repository = repository
    
    def register(self, user_data: UserCreate) -> UserResponse:
        """Register a new user."""
        # Check if user already exists
        existing_users = self.repository.find_all()
        if any(u.get('username') == user_data.username for u in existing_users):
            logger.warning(f"Duplicate username: '{user_data.username}'")
            raise DuplicateUserError(user_data.username)
        
        # Create new user
        user = {
            'username': user_data.username,
            'email': user_data.email,
            'password': hash_password(user_data.password),
            'created_at': datetime.now().isoformat()
        }
        
        # Save to repository
        saved_user = self.repository.save(user)
        logger.info(f"User '{user_data.username}' registered successfully")
        
        return UserResponse(
            id=saved_user['id'],
            username=saved_user['username'],
            email=saved_user['email'],
            created_at=saved_user['created_at']
        )
    
    def login(self, login_data: UserLogin) -> UserResponse:
        """Login a user and validate credentials."""
        users = self.repository.find_all()
        
        for user in users:
            if user.get('username') == login_data.username:
                if verify_password(login_data.password, user.get('password', '')):
                    logger.info(f"User '{login_data.username}' logged in successfully")
                    return UserResponse(
                        id=user['id'],
                        username=user['username'],
                        email=user['email'],
                        created_at=user['created_at']
                    )
        
        logger.warning(f"Failed login attempt for user '{login_data.username}'")
        raise InvalidCredentialsError()
    
    def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID."""
        user = self.repository.find_by_id(user_id)
        if not user:
            logger.error(f"User ID {user_id} not found")
            raise UserNotFoundError(user_id=user_id)
        
        return UserResponse(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            created_at=user['created_at']
        )
    
    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """Get user by username."""
        users = self.repository.find_all()
        for user in users:
            if user.get('username') == username:
                return UserResponse(
                    id=user['id'],
                    username=user['username'],
                    email=user['email'],
                    created_at=user['created_at']
                )
        return None
    
    def list_users(self) -> List[UserResponse]:
        """List all users."""
        users = self.repository.find_all()
        return [
            UserResponse(
                id=u['id'],
                username=u['username'],
                email=u['email'],
                created_at=u['created_at']
            )
            for u in users
        ]
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        if not self.repository.exists(user_id):
            logger.error(f"User ID {user_id} not found for deletion")
            raise UserNotFoundError(user_id=user_id)
        
        result = self.repository.delete(user_id)
        if result:
            logger.info(f"User with ID {user_id} deleted")
        return result
