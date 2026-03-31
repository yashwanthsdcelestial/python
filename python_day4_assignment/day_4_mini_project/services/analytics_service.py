import logging
from sqlalchemy.orm import Session
from models.db_models import Loan, User
from models.schemas import AnalyticsSummary
from models.enums import LoanStatus
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from decorators.timer import timer

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, db: Session):
        self.loan_repo = SQLAlchemyRepository(Loan, db)
        self.user_repo = SQLAlchemyRepository(User, db)

    @timer
    def get_summary(self) -> AnalyticsSummary:
        all_loans: list[Loan] = self.loan_repo.find_all_raw()
        all_users: list[User] = self.user_repo.find_all_raw()

        # Status breakdown — dict comprehension
        status_counts = {
            status.value: len([l for l in all_loans if l.status == status])
            for status in LoanStatus
        }

        # Loans by purpose — dict comprehension
        loans_by_purpose = {
            purpose: len([l for l in all_loans if l.purpose.value == purpose])
            for purpose in {l.purpose.value for l in all_loans}
        }

        # Loans by employment — dict comprehension
        loans_by_employment = {
            emp: len([l for l in all_loans if l.employment_status.value == emp])
            for emp in {l.employment_status.value for l in all_loans}
        }

        # Average loan amount — list comprehension
        amounts = [l.amount for l in all_loans]
        avg_amount = sum(amounts) / len(amounts) if amounts else 0.0

        # Total disbursed — list comprehension with filter (approved loans only)
        total_disbursed = sum(
            [l.amount for l in all_loans if l.status == LoanStatus.approved]
        )

        logger.info("Analytics summary computed.")
        return AnalyticsSummary(
            total_users=len(all_users),
            total_loans=len(all_loans),
            pending_loans=status_counts.get("pending", 0),
            approved_loans=status_counts.get("approved", 0),
            rejected_loans=status_counts.get("rejected", 0),
            total_disbursed_amount=total_disbursed,
            loans_by_purpose=loans_by_purpose,
            loans_by_employment=loans_by_employment,
            avg_loan_amount=round(avg_amount, 2),
        )