import logging
from typing import Optional, List

from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.repositories.exam_repository import ExamRepository, EnrollmentRepository
from app.repositories.attempt_repository import AttemptRepository
from app.schemas.schemas import ExamCreate, ExamUpdate
from app.models.models import Exam, ExamRegistration, ExamStatusEnum, User
from app.utils.notifications import send_enrollment_notification

logger = logging.getLogger(__name__)


class ExamService:
    def __init__(self, db: Session):
        self.repo = ExamRepository(db)
        self.enrollment_repo = EnrollmentRepository(db)

    def create_exam(self, data: ExamCreate, admin_id: int) -> Exam:
        questions_data = [q.model_dump() for q in data.questions]
        # Assign sequential IDs to questions
        for i, q in enumerate(questions_data, start=1):
            q["id"] = i

        # Calculate total_marks from questions
        total = sum(q["marks"] for q in questions_data)

        exam_dict = {
            "title": data.title,
            "description": data.description,
            "duration_minutes": data.duration_minutes,
            "total_marks": total,
            "pass_percentage": data.pass_percentage,
            "max_attempts": data.max_attempts,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "questions": questions_data,
            "created_by": admin_id,
            "status": ExamStatusEnum.draft,
        }
        exam = self.repo.create(exam_dict)
        logger.info(f"Admin {admin_id} created exam: {exam.title}")
        return exam

    def update_exam(self, exam_id: int, data: ExamUpdate, admin_id: int) -> Exam:
        exam = self.repo.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        if exam.created_by != admin_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your exam")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(exam, update_data)

    def delete_exam(self, exam_id: int, admin_id: int) -> None:
        exam = self.repo.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        self.repo.soft_delete(exam)
        logger.info(f"Admin {admin_id} deleted exam: {exam_id}")

    def get_exam(self, exam_id: int) -> Exam:
        exam = self.repo.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        return exam

    def list_exams(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[ExamStatusEnum] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
        student_id: Optional[int] = None,
    ):
        skip = (page - 1) * page_size
        total, exams = self.repo.get_all(
            skip=skip, limit=page_size, status=status, search=search, sort_by=sort_by, sort_desc=sort_desc
        )

        # Check enrollment for student
        enrolled_exam_ids = set()
        if student_id:
            _, enrollments = self.enrollment_repo.get_student_enrollments(student_id, skip=0, limit=1000)
            enrolled_exam_ids = {e.exam_id for e in enrollments}

        result = []
        for exam in exams:
            exam_dict = {
                "id": exam.id,
                "title": exam.title,
                "description": exam.description,
                "duration_minutes": exam.duration_minutes,
                "total_marks": exam.total_marks,
                "pass_percentage": exam.pass_percentage,
                "status": exam.status,
                "max_attempts": exam.max_attempts,
                "start_time": exam.start_time,
                "end_time": exam.end_time,
                "created_by": exam.created_by,
                "created_at": exam.created_at,
                "question_count": len(exam.questions) if exam.questions else 0,
                "is_enrolled": exam.id in enrolled_exam_ids,
            }
            result.append(exam_dict)

        return {"total": total, "page": page, "page_size": page_size, "items": result}


class EnrollmentService:
    def __init__(self, db: Session):
        self.exam_repo = ExamRepository(db)
        self.enrollment_repo = EnrollmentRepository(db)

    def enroll(self, student_id: int, exam_id: int, background_tasks: BackgroundTasks, student_email: str, student_name: str) -> ExamRegistration:
        exam = self.exam_repo.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        if exam.status != ExamStatusEnum.published:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam is not published")

        existing = self.enrollment_repo.get_enrollment(student_id, exam_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already enrolled in this exam")

        reg = self.enrollment_repo.create(student_id=student_id, exam_id=exam_id)

        # Background task: send enrollment notification
        background_tasks.add_task(
            send_enrollment_notification,
            email=student_email,
            name=student_name,
            exam_title=exam.title,
        )

        logger.info(f"Student {student_id} enrolled in exam {exam_id}")
        return reg

    def get_my_exams(self, student_id: int, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        total, enrollments = self.enrollment_repo.get_student_enrollments(student_id, skip=skip, limit=page_size)

        result = []
        for reg in enrollments:
            exam = reg.exam
            result.append({
                "enrollment_id": reg.id,
                "exam_id": exam.id,
                "title": exam.title,
                "description": exam.description,
                "duration_minutes": exam.duration_minutes,
                "total_marks": exam.total_marks,
                "pass_percentage": exam.pass_percentage,
                "status": exam.status,
                "registered_at": reg.registered_at,
            })

        return {"total": total, "page": page, "page_size": page_size, "items": result}
