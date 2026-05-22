from datetime import datetime, timezone
from typing import Optional
import enum

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float, Text,
    ForeignKey, JSON, Enum as SAEnum, Index, func
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"


class ExamStatusEnum(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class AttemptStatusEnum(str, enum.Enum):
    in_progress = "in_progress"
    submitted = "submitted"
    timed_out = "timed_out"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SAEnum(RoleEnum), nullable=False, default=RoleEnum.student)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    exams_created = relationship("Exam", back_populates="creator", foreign_keys="Exam.created_by")
    exam_registrations = relationship("ExamRegistration", back_populates="student")
    attempts = relationship("ExamAttempt", back_populates="student")

    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
    )


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False, default=60)
    total_marks = Column(Float, nullable=False, default=100)
    pass_percentage = Column(Float, nullable=False, default=50.0)
    status = Column(SAEnum(ExamStatusEnum), nullable=False, default=ExamStatusEnum.draft)
    questions = Column(JSON, nullable=False, default=list)
    # questions format: [{"id": 1, "text": "...", "options": [...], "correct_answer": "...", "marks": 5}]
    max_attempts = Column(Integer, default=1)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="exams_created", foreign_keys=[created_by])
    exam_registrations = relationship("ExamRegistration", back_populates="exam")
    attempts = relationship("ExamAttempt", back_populates="exam")

    __table_args__ = (
        Index("ix_exams_status", "status"),
        Index("ix_exams_created_by", "created_by"),
    )


class ExamRegistration(Base):
    """Maps students to enrolled exams (many-to-many)"""
    __tablename__ = "exam_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    student = relationship("User", back_populates="exam_registrations")
    exam = relationship("Exam", back_populates="exam_registrations")

    __table_args__ = (
        Index("ix_exam_reg_student_exam", "student_id", "exam_id", unique=True),
    )


class ExamAttempt(Base):
    """Tracks each student's exam attempt"""
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    status = Column(SAEnum(AttemptStatusEnum), nullable=False, default=AttemptStatusEnum.in_progress)
    score = Column(Float)
    percentage = Column(Float)
    passed = Column(Boolean)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    submitted_at = Column(DateTime(timezone=True))
    time_taken_seconds = Column(Integer)
    attempt_number = Column(Integer, default=1)

    # Relationships
    student = relationship("User", back_populates="attempts")
    exam = relationship("Exam", back_populates="attempts")
    answers = relationship("StudentAnswer", back_populates="attempt", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_attempts_student_exam", "student_id", "exam_id"),
    )


class StudentAnswer(Base):
    """Stores answers submitted per question per attempt"""
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"), nullable=False, index=True)
    question_id = Column(Integer, nullable=False)
    selected_answer = Column(String(500))
    is_correct = Column(Boolean)
    marks_awarded = Column(Float, default=0)

    # Relationships
    attempt = relationship("ExamAttempt", back_populates="answers")

    __table_args__ = (
        Index("ix_answers_attempt_question", "attempt_id", "question_id"),
    )
