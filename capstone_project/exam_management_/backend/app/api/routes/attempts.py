import logging
from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_student, get_db
from app.schemas.schemas import AttemptSubmitRequest
from app.services.attempt_service import AttemptService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/start/{exam_id}",
    summary="Start an exam attempt (Student only)",
    description="Begin a timed exam attempt. Returns questions without correct answers.",
)
async def start_attempt(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = AttemptService(db)
    return service.start_attempt(student_id=current_user.id, exam_id=exam_id)


@router.post(
    "/{attempt_id}/submit",
    summary="Submit an exam attempt (Student only)",
    description="Submit answers for scoring. Auto-scores and sends result notification in background.",
)
async def submit_attempt(
    attempt_id: int,
    data: AttemptSubmitRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = AttemptService(db)
    return service.submit_attempt(
        attempt_id=attempt_id,
        student_id=current_user.id,
        data=data,
        background_tasks=background_tasks,
        student_email=current_user.email,
        student_name=current_user.full_name,
    )


@router.get(
    "/my-results",
    summary="Get my exam results (Student only)",
    description="Returns paginated list of the student's past attempts and scores.",
)
async def get_my_results(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = AttemptService(db)
    return service.get_my_results(student_id=current_user.id, page=page, page_size=page_size)


@router.get(
    "/{attempt_id}",
    summary="Get a specific attempt result (Student only)",
)
async def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_student),
):
    service = AttemptService(db)
    attempt = service.attempt_repo.get_by_id(attempt_id)
    from fastapi import HTTPException, status
    if not attempt or attempt.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    exam = attempt.exam
    return {
        "id": attempt.id,
        "exam_id": attempt.exam_id,
        "exam_title": exam.title if exam else "Unknown",
        "status": attempt.status,
        "score": attempt.score,
        "total_marks": exam.total_marks if exam else 0,
        "percentage": attempt.percentage,
        "passed": attempt.passed,
        "started_at": attempt.started_at,
        "submitted_at": attempt.submitted_at,
        "time_taken_seconds": attempt.time_taken_seconds,
        "attempt_number": attempt.attempt_number,
        "answers": [
            {
                "question_id": a.question_id,
                "selected_answer": a.selected_answer,
                "is_correct": a.is_correct,
                "marks_awarded": a.marks_awarded,
            }
            for a in attempt.answers
        ],
    }
