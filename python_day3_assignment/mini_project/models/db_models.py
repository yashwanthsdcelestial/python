"""SQLAlchemy ORM models for database."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.enums import TaskStatus, TaskPriority


class User(Base):
    """User model for SQLAlchemy ORM."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    tasks = relationship("Task", back_populates="owner_user", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at.isoformat()
        }


class Task(Base):
    """Task model for SQLAlchemy ORM."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    owner = Column(String(30), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to user
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    owner_user = relationship("User", back_populates="tasks")
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'owner': self.owner,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
