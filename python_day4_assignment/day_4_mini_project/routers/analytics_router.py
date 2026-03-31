from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import AnalyticsSummary
from services.analytics_service import AnalyticsService
from decorators.auth import require_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    return AnalyticsService(db).get_summary()