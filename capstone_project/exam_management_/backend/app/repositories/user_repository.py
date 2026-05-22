import logging
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import User, RoleEnum

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email, User.is_deleted == False).first()

    def create(self, email: str, hashed_password: str, full_name: str, role: RoleEnum) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"Created user: {email} with role: {role}")
        return user

    def get_all(self, skip: int = 0, limit: int = 20, role: Optional[RoleEnum] = None) -> Tuple[int, List[User]]:
        query = self.db.query(User).filter(User.is_deleted == False)
        if role:
            query = query.filter(User.role == role)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def deactivate(self, user_id: int) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            self.db.refresh(user)
        return user

    def count_by_role(self, role: RoleEnum) -> int:
        return self.db.query(func.count(User.id)).filter(User.role == role, User.is_deleted == False).scalar()
