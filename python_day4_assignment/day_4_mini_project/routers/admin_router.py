import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import LoanResponse, LoanReview
from models.enums import LoanStatus
from services.loan_service import LoanService
from services.user_service import UserService
from decorators.auth import require_role
from decorators.timer import timer
from utils.notifications import send_review_notification

router = APIRouter(prefix="/admin", tags=["Admin"])

_review_counter = {"today": 0}
executor = ThreadPoolExecutor(max_workers=4)


@router.get("/loans", response_model=List[LoanResponse])
def admin_list_loans(
    status: Optional[LoanStatus] = None,
    user_id: Optional[int] = None,
    purpose: Optional[str] = None,
    employment_status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "applied_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    return LoanService(db).admin_get_all_loans(
        status=status,
        user_id=user_id,
        purpose=purpose,
        employment_status=employment_status,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def admin_get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    return LoanService(db).admin_get_loan_by_id(loan_id)


@router.patch("/loans/{loan_id}/review", response_model=LoanResponse)
def review_loan(
    loan_id: int,
    data: LoanReview,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    admin_username = current_user["username"]
    service = LoanService(db)
    updated = service.review_loan(loan_id, data, admin_username)

    user = UserService(db).get_user_by_id(updated.user_id)

    async def _notify():
        await send_review_notification(loan_id, user.username, updated.status)

    background_tasks.add_task(asyncio.run, _notify())
    _review_counter["today"] += 1
    return updated 


@router.post("/loans/bulk-check")
def bulk_eligibility_check(
    loan_ids: List[int],
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """ThreadPoolExecutor: concurrently compute eligibility for each loan ID."""
    service = LoanService(db)

    @timer
    def run_bulk():
        futures = [executor.submit(service.bulk_eligibility_check, [lid]) for lid in loan_ids]
        results = []
        for f in futures:
            results.extend(f.result())
        return results

    return {"results": run_bulk()}