import logging
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from models.db_models import Loan, User
from models.schemas import LoanCreate, LoanReview, LoanResponse
from models.enums import LoanStatus
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from exceptions.custom_exceptions import (
    LoanNotFoundError, MaxPendingLoansError, InvalidLoanReviewError
)
from decorators.timer import timer

logger = logging.getLogger(__name__)

MAX_PENDING = 3


class LoanService:
    def __init__(self, db: Session):
        self.repo = SQLAlchemyRepository(Loan, db)
        self.user_repo = SQLAlchemyRepository(User, db)

    @timer
    def apply_loan(self, user_id: int, data: LoanCreate) -> LoanResponse:
        pending_count = self.repo.count_by(user_id=user_id, status=LoanStatus.pending)
        if pending_count >= MAX_PENDING:
            logger.warning(f"User {user_id} has reached max pending loans.")
            raise MaxPendingLoansError()

        loan = Loan(
            user_id=user_id,
            amount=data.amount,
            purpose=data.purpose,
            tenure_months=data.tenure_months,
            employment_status=data.employment_status,
            status=LoanStatus.pending,
        )
        saved = self.repo.save(loan)
        logger.info(f"Loan #{saved.id} created for user {user_id}, amount={saved.amount}")
        return LoanResponse.model_validate(saved)

    @timer
    def get_my_loans(
        self,
        user_id: int,
        status: Optional[LoanStatus] = None,
        page: int = 1,
        limit: int = 10,
    ) -> List[LoanResponse]:
        filters = [Loan.user_id == user_id]
        if status:
            filters.append(Loan.status == status)
        loans = self.repo.find_all_filtered(
            filters=filters,
            order_by=Loan.applied_at.desc(),
            offset=(page - 1) * limit,
            limit=limit,
        )
        return [LoanResponse.model_validate(l) for l in loans]

    @timer
    def get_my_loan_by_id(self, user_id: int, loan_id: int) -> LoanResponse:
        loan = self.repo.find(loan_id)
        if not loan or loan.user_id != user_id:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        return LoanResponse.model_validate(loan)

    @timer
    def admin_get_all_loans(
        self,
        status: Optional[LoanStatus] = None,
        user_id: Optional[int] = None,
        purpose: Optional[str] = None,
        employment_status: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "applied_at",
        order: str = "desc",
    ) -> List[LoanResponse]:
        filters = []
        if status:
            filters.append(Loan.status == status)
        if user_id:
            filters.append(Loan.user_id == user_id)
        if purpose:
            filters.append(Loan.purpose == purpose)
        if employment_status:
            filters.append(Loan.employment_status == employment_status)

        sort_col = getattr(Loan, sort_by, Loan.applied_at)
        order_col = sort_col.desc() if order == "desc" else sort_col.asc()

        loans = self.repo.find_all_filtered(
            filters=filters,
            order_by=order_col,
            offset=(page - 1) * limit,
            limit=limit,
        )
        return [LoanResponse.model_validate(l) for l in loans]

    @timer
    def admin_get_loan_by_id(self, loan_id: int) -> LoanResponse:
        loan = self.repo.find(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        return LoanResponse.model_validate(loan)

    @timer
    def review_loan(
        self, loan_id: int, data: LoanReview, admin_username: str
    ) -> LoanResponse:
        loan = self.repo.find(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        if loan.status != LoanStatus.pending:
            logger.warning(f"Re-review attempt on loan #{loan_id} (status={loan.status})")
            raise InvalidLoanReviewError(
                f"Loan #{loan_id} is already '{loan.status.value}' and cannot be reviewed again."
            )

        loan.status = data.status
        loan.admin_remarks = data.admin_remarks
        loan.reviewed_by = admin_username
        loan.reviewed_at = datetime.now(timezone.utc)
        loan.updated_at = datetime.now(timezone.utc)

        try:
            updated = self.repo.update(loan)
        except Exception as exc:
            self.repo.db.rollback()
            logger.error(f"Transaction failed for loan #{loan_id}: {exc}")
            raise

        logger.info(f"Loan #{loan_id} {data.status.value} by admin '{admin_username}'")
        return LoanResponse.model_validate(updated)

    def get_loan_raw(self, loan_id: int) -> Loan:
        loan = self.repo.find(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan #{loan_id} not found.")
        return loan

    def get_all_loans_raw(self) -> List[Loan]:
        return self.repo.find_all_raw()

    def bulk_eligibility_check(self, loan_ids: List[int]) -> List[dict]:
        """Used by the ThreadPoolExecutor bulk-check endpoint."""
        results = []
        for lid in loan_ids:
            loan = self.repo.find(lid)
            if not loan:
                results.append({"loan_id": lid, "eligible": False, "score": 0, "reason": "not found"})
                continue
            user = self.user_repo.find(loan.user_id)
            if not user:
                results.append({"loan_id": lid, "eligible": False, "score": 0, "reason": "user not found"})
                continue
            ratio = (user.monthly_income * 12) / loan.amount if loan.amount else 0
            score = min(100, int(ratio * 10))
            eligible = ratio >= 1.0
            results.append({
                "loan_id": lid,
                "eligible": eligible,
                "score": score,
                "reason": "income-to-loan ratio ok" if eligible else "income too low relative to loan amount",
            })
        return results