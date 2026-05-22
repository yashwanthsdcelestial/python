from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_student, get_db
from app.schemas.schemas import EnrollmentResponse
from app.services.exam_service import EnrollmentService

router = APIRouter()


@router.post(
    "/{exam_id}",
    response_model=EnrollmentResponse,
    summary="Enroll in an exam (Student only)",
    description="Register a student for a published exam. Triggers enrollment notification.",
)
async def enroll_in_exam(
    exam_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = EnrollmentService(db)
    return service.enroll(
        student_id=current_user.id,
        exam_id=exam_id,
        background_tasks=background_tasks,
        student_email=current_user.email,
        student_name=current_user.full_name,
    )


@router.get(
    "",
    summary="Get my enrolled exams (Student only)",
)
async def get_my_exams(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = EnrollmentService(db)
    return service.get_my_exams(student_id=current_user.id, page=page, page_size=page_size)
