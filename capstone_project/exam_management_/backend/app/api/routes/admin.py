import logging
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.dependencies import require_admin, get_db
from app.models.models import RoleEnum
from app.repositories.user_repository import UserRepository
from app.repositories.exam_repository import ExamRepository, EnrollmentRepository
from app.repositories.attempt_repository import AttemptRepository
from app.schemas.schemas import AdminStatsResponse, UserListResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/stats",
    response_model=AdminStatsResponse,
    summary="Get admin dashboard stats (Admin only)",
)
async def get_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    user_repo = UserRepository(db)
    exam_repo = ExamRepository(db)
    attempt_repo = AttemptRepository(db)
    from app.models.models import ExamStatusEnum

    return {
        "total_users": user_repo.count_by_role(RoleEnum.admin) + user_repo.count_by_role(RoleEnum.student),
        "total_students": user_repo.count_by_role(RoleEnum.student),
        "total_exams": exam_repo.count_all(),
        "published_exams": exam_repo.count_by_status(ExamStatusEnum.published),
        "total_attempts": attempt_repo.count_total(),
        "passed_attempts": attempt_repo.count_passed(),
    }


@router.get(
    "/users",
    response_model=UserListResponse,
    summary="List all users (Admin only)",
)
async def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    role: Optional[RoleEnum] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    repo = UserRepository(db)
    skip = (page - 1) * page_size
    total, users = repo.get_all(skip=skip, limit=page_size, role=role)
    return {"total": total, "page": page, "page_size": page_size, "items": users}


@router.patch(
    "/users/{user_id}/deactivate",
    summary="Deactivate a user account (Admin only)",
)
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate yourself")
    repo = UserRepository(db)
    user = repo.deactivate(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": f"User {user.email} deactivated"}


@router.get(
    "/exam-results/{exam_id}",
    summary="Get all attempt results for an exam (Admin only)",
)
async def get_exam_results(
    exam_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    exam_repo = ExamRepository(db)
    exam = exam_repo.get_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    skip = (page - 1) * page_size
    from app.models.models import ExamAttempt
    query = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id)
    total = query.count()
    attempts = query.order_by(ExamAttempt.started_at.desc()).offset(skip).limit(page_size).all()

    return {
        "exam_title": exam.title,
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "attempt_id": a.id,
                "student_id": a.student_id,
                "student_name": a.student.full_name if a.student else "Unknown",
                "student_email": a.student.email if a.student else "Unknown",
                "score": a.score,
                "total_marks": exam.total_marks,
                "percentage": a.percentage,
                "passed": a.passed,
                "status": a.status,
                "started_at": a.started_at,
                "submitted_at": a.submitted_at,
                "attempt_number": a.attempt_number,
            }
            for a in attempts
        ],
    }


@router.get(
    "/view/student-exam-summary",
    summary="Query DB view: student exam summary (Admin only)",
    description="Uses the `vw_student_exam_summary` database view.",
)
async def student_exam_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        result = db.execute(text("SELECT * FROM vw_student_exam_summary LIMIT 100"))
        rows = result.mappings().all()
        return {"items": [dict(r) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
