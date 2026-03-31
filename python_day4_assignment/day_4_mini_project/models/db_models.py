from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import (
    Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from models.enums import UserRole, LoanPurpose, EmploymentStatus, LoanStatus


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    monthly_income: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole), nullable=False, default=UserRole.user
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[LoanPurpose] = mapped_column(SAEnum(LoanPurpose), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    employment_status: Mapped[EmploymentStatus] = mapped_column(
        SAEnum(EmploymentStatus), nullable=False
    )
    status: Mapped[LoanStatus] = mapped_column(
        SAEnum(LoanStatus), nullable=False, default=LoanStatus.pending
    )
    admin_remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    credit_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="loans")

    def __repr__(self):
        return f"<Loan id={self.id} user_id={self.user_id} amount={self.amount} status={self.status}>"