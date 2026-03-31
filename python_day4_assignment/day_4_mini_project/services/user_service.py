import logging
from sqlalchemy.orm import Session
from models.db_models import User
from models.schemas import UserCreate, UserResponse, LoginResponse
from models.enums import UserRole
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from exceptions.custom_exceptions import (
    DuplicateUserError, InvalidCredentialsError, UserNotFoundError
)
from decorators.timer import timer
from utils.jwt_handler import hash_password, verify_password

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.repo = SQLAlchemyRepository(User, db)

    @timer
    def register(self, data: UserCreate) -> UserResponse:
        if self.repo.find_by(username=data.username):
            logger.warning(f"Duplicate username attempt: {data.username}")
            raise DuplicateUserError(f"Username '{data.username}' is already taken.")
        if self.repo.find_by(email=data.email):
            logger.warning(f"Duplicate email attempt: {data.email}")
            raise DuplicateUserError(f"Email '{data.email}' is already registered.")

        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
            phone=data.phone,
            monthly_income=data.monthly_income,
            role=UserRole.user,
        )
        saved = self.repo.save(user)
        logger.info(f"New user registered: {saved.username} (id={saved.id})")
        return UserResponse.model_validate(saved)

    @timer
    def login(self, username: str, password: str) -> LoginResponse:
        user = self.repo.find_by(username=username)
        if not user or not verify_password(password, user.password):
            logger.error(f"Login failed for username: {username}")
            raise InvalidCredentialsError("Invalid username or password.")
        logger.info(f"User logged in: {username} (role={user.role})")
        return LoginResponse(
            message="Login successful",
            user_id=user.id,
            username=user.username,
            role=user.role.value,
        )

    def get_user_by_username(self, username: str) -> User:
        user = self.repo.find_by(username=username)
        if not user:
            raise UserNotFoundError(f"User '{username}' not found.")
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.find(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found.")
        return user

    def count_all_users(self) -> int:
        return len(self.repo.find_all_raw())

    def seed_admin(self, username: str, password: str, email: str):
        if self.repo.find_by(username=username):
            logger.info("Admin user already exists.")
            return
        admin = User(
            username=username,
            email=email,
            password=hash_password(password),
            phone="0000000000",
            monthly_income=0,
            role=UserRole.admin,
        )
        self.repo.save(admin)
        logger.info("Admin user seeded successfully.")