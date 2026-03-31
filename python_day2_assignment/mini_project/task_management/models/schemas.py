"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from models.enums import TaskStatus, TaskPriority


# ============== USER SCHEMAS ==============

class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=30, description="Username (3-30 chars)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    
    @field_validator('username')
    @classmethod
    def username_must_not_be_whitespace(cls, v):
        """Validate username is not just whitespace."""
        if not v or v.isspace():
            raise ValueError("Username cannot be empty or whitespace")
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def password_must_not_be_whitespace(cls, v):
        """Validate password is not just whitespace."""
        if not v or v.isspace():
            raise ValueError("Password cannot be empty or whitespace")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""
    id: int
    username: str
    email: str
    created_at: str
    
    class Config:
        """Pydantic config."""
        from_attributes = True


# ============== TASK SCHEMAS ==============

class TaskCreate(BaseModel):
    """Schema for task creation."""
    title: str = Field(..., min_length=3, max_length=100, description="Task title (3-100 chars)")
    description: Optional[str] = Field(None, max_length=500, description="Task description (max 500 chars)")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    owner: str = Field(..., description="Task owner (username)")
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_whitespace(cls, v):
        """Validate title is not just whitespace."""
        if not v or v.isspace():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @field_validator('description', mode='before')
    @classmethod
    def description_strip(cls, v):
        """Strip whitespace from description."""
        if v and isinstance(v, str):
            return v.strip() if v.strip() else None
        return v


class TaskUpdate(BaseModel):
    """Schema for task update (all fields optional)."""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    
    @field_validator('title')
    @classmethod
    def title_validate(cls, v):
        """Validate title if provided."""
        if v is not None and (not v or v.isspace()):
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else v


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner: str
    created_at: str
    updated_at: str
    
    class Config:
        """Pydantic config."""
        from_attributes = True
