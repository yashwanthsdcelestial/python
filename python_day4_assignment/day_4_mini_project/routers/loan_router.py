import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import LoanCreate, LoanResponse
from models.enums import LoanStatus
from services.loan_service import LoanService
from decorators.auth import require_role
from utils.notifications import log_new_application

router = APIRouter(prefix="/loans", tags=["User Loans"])


@router.post("", response_model=LoanResponse, status_code=201)
def apply_loan(
    data: LoanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("user")),
):
    user_id = current_user["user_id"]
    username = current_user["username"]
    service = LoanService(db)
    loan = service.apply_loan(user_id, data)
    background_tasks.add_task(
        log_new_application, loan.id, username, loan.purpose, loan.amount
    )
    return loan


@router.get("/my", response_model=list[LoanResponse])
def get_my_loans(
    status: Optional[LoanStatus] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("user")),
):
    return LoanService(db).get_my_loans(
        user_id=current_user["user_id"],
        status=status,
        page=page,
        limit=limit,
    )


@router.get("/my/{loan_id}", response_model=LoanResponse)
def get_my_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("user")),
):
    return LoanService(db).get_my_loan_by_id(current_user["user_id"], loan_id)