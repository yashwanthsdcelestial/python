import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin, get_db
from app.models.models import ExamStatusEnum, RoleEnum
from app.schemas.schemas import (
    ExamCreate, ExamUpdate, ExamListResponse, ExamDetailResponse, ExamAdminResponse, ExamResponse
)
from app.services.exam_service import ExamService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "",
    summary="List all published exams",
    description="Returns paginated list of exams. Students see only published exams.",
)
async def list_exams(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=50, description="Items per page"),
    search: Optional[str] = Query(default=None, description="Search by title or description"),
    sort_by: str = Query(default="created_at", description="Sort field"),
    sort_desc: bool = Query(default=True, description="Sort descending"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ExamService(db)
    # Students only see published, admins see all
    status_filter = None if current_user.role == RoleEnum.admin else ExamStatusEnum.published
    student_id = current_user.id if current_user.role == RoleEnum.student else None
    return service.list_exams(
        page=page, page_size=page_size, status=status_filter,
        search=search, sort_by=sort_by, sort_desc=sort_desc, student_id=student_id,
    )


@router.get(
    "/{exam_id}",
    summary="Get exam details",
    description="Returns exam details. Students don't see correct answers.",
)
async def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ExamService(db)
    exam = service.get_exam(exam_id)

    questions = exam.questions or []

    if current_user.role == RoleEnum.admin:
        # Admin sees full data including correct answers
        return {
            "id": exam.id, "title": exam.title, "description": exam.description,
            "duration_minutes": exam.duration_minutes, "total_marks": exam.total_marks,
            "pass_percentage": exam.pass_percentage, "status": exam.status,
            "max_attempts": exam.max_attempts, "start_time": exam.start_time,
            "end_time": exam.end_time, "created_by": exam.created_by, "created_at": exam.created_at,
            "question_count": len(questions), "is_enrolled": False,
            "questions": questions,
        }
    else:
        # Strip correct answers for students
        safe_questions = [{"id": q["id"], "text": q["text"], "options": q["options"], "marks": q["marks"]} for q in questions]
        return {
            "id": exam.id, "title": exam.title, "description": exam.description,
            "duration_minutes": exam.duration_minutes, "total_marks": exam.total_marks,
            "pass_percentage": exam.pass_percentage, "status": exam.status,
            "max_attempts": exam.max_attempts, "start_time": exam.start_time,
            "end_time": exam.end_time, "created_by": exam.created_by, "created_at": exam.created_at,
            "question_count": len(questions), "is_enrolled": False,
            "questions": safe_questions,
        }


@router.post(
    "",
    summary="Create a new exam (Admin only)",
    description="Create an exam with questions. Only admins can create exams.",
)
async def create_exam(
    data: ExamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    service = ExamService(db)
    return service.create_exam(data, admin_id=current_user.id)


@router.put(
    "/{exam_id}",
    summary="Update exam (Admin only)",
)
async def update_exam(
    exam_id: int,
    data: ExamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    service = ExamService(db)
    return service.update_exam(exam_id, data, admin_id=current_user.id)


@router.delete(
    "/{exam_id}",
    summary="Delete exam (Admin only)",
)
async def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    service = ExamService(db)
    service.delete_exam(exam_id, admin_id=current_user.id)
    return {"message": "Exam deleted successfully"}
