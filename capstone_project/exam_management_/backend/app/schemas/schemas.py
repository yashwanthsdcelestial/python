from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
import re

from app.models.models import RoleEnum, ExamStatusEnum, AttemptStatusEnum


# ─── Auth Schemas ──────────────────────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: RoleEnum = RoleEnum.student

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_valid(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return v.strip()


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ─── User Schemas ───────────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: RoleEnum
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[UserResponse]


# ─── Question Schemas ───────────────────────────────────────────────────────────

class QuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct_answer: str
    marks: float = 5.0

    @field_validator("options")
    @classmethod
    def options_count(cls, v):
        if len(v) < 2 or len(v) > 6:
            raise ValueError("Question must have between 2 and 6 options")
        return v

    @field_validator("correct_answer")
    @classmethod
    def correct_in_options(cls, v, info):
        if "options" in info.data and v not in info.data["options"]:
            raise ValueError("correct_answer must be one of the options")
        return v


class QuestionResponse(BaseModel):
    id: int
    text: str
    options: List[str]
    marks: float
    # correct_answer is NOT exposed to students


# ─── Exam Schemas ───────────────────────────────────────────────────────────────

class ExamCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int = 60
    total_marks: float = 100
    pass_percentage: float = 50.0
    max_attempts: int = 1
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    questions: List[QuestionCreate]

    @field_validator("questions")
    @classmethod
    def questions_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Exam must have at least one question")
        return v


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    pass_percentage: Optional[float] = None
    max_attempts: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ExamStatusEnum] = None


class ExamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    duration_minutes: int
    total_marks: float
    pass_percentage: float
    status: ExamStatusEnum
    max_attempts: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_by: int
    created_at: datetime
    question_count: int = 0
    is_enrolled: bool = False


class ExamDetailResponse(ExamResponse):
    """Includes questions (without correct answers for students)"""
    questions: List[QuestionResponse] = []


class ExamAdminResponse(ExamResponse):
    """Full exam details for admin including correct answers"""
    questions: List[dict] = []


class ExamListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ExamResponse]


# ─── Enrollment Schemas ─────────────────────────────────────────────────────────

class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    exam_id: int
    registered_at: datetime
    is_active: bool


# ─── Attempt Schemas ────────────────────────────────────────────────────────────

class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: str


class AttemptStartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exam_id: int
    started_at: datetime
    duration_minutes: int
    questions: List[QuestionResponse]


class AttemptSubmitRequest(BaseModel):
    answers: List[AnswerSubmit]


class AttemptResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exam_id: int
    exam_title: str
    status: AttemptStatusEnum
    score: Optional[float]
    total_marks: float
    percentage: Optional[float]
    passed: Optional[bool]
    started_at: datetime
    submitted_at: Optional[datetime]
    time_taken_seconds: Optional[int]
    attempt_number: int


class AttemptListResponse(BaseModel):
    total: int
    items: List[AttemptResultResponse]


# ─── Error Schema ───────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None


# ─── Dashboard Stats ────────────────────────────────────────────────────────────

class AdminStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_exams: int
    published_exams: int
    total_attempts: int
    passed_attempts: int


class StudentStatsResponse(BaseModel):
    enrolled_exams: int
    completed_attempts: int
    passed_exams: int
    average_score: Optional[float]
