import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.repositories.exam_repository import ExamRepository, EnrollmentRepository
from app.repositories.attempt_repository import AttemptRepository
from app.models.models import AttemptStatusEnum, ExamStatusEnum
from app.schemas.schemas import AttemptSubmitRequest
from app.utils.notifications import send_result_notification

logger = logging.getLogger(__name__)


class AttemptService:
    def __init__(self, db: Session):
        self.exam_repo = ExamRepository(db)
        self.enrollment_repo = EnrollmentRepository(db)
        self.attempt_repo = AttemptRepository(db)

    def start_attempt(self, student_id: int, exam_id: int) -> dict:
        exam = self.exam_repo.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        if exam.status != ExamStatusEnum.published:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam is not available")

        # Check enrollment
        enrollment = self.enrollment_repo.get_enrollment(student_id, exam_id)
        if not enrollment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not enrolled in this exam")

        # Check existing in-progress attempt
        in_progress = self.attempt_repo.get_in_progress(student_id, exam_id)
        if in_progress:
            # Check if timed out
            started = in_progress.started_at
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            deadline = started + timedelta(minutes=exam.duration_minutes)
            if datetime.now(timezone.utc) > deadline:
                # Auto-submit as timed out
                self.attempt_repo.submit(in_progress, score=0, percentage=0, passed=False, status=AttemptStatusEnum.timed_out)
            else:
                # Resume attempt - return current attempt with questions (no correct answers)
                questions = self._strip_answers(exam.questions)
                return {
                    "id": in_progress.id,
                    "exam_id": exam.id,
                    "started_at": in_progress.started_at,
                    "duration_minutes": exam.duration_minutes,
                    "questions": questions,
                }

        # Check max attempts
        count = self.attempt_repo.count_attempts(student_id, exam_id)
        if count >= exam.max_attempts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum attempts ({exam.max_attempts}) reached",
            )

        attempt = self.attempt_repo.create(student_id=student_id, exam_id=exam_id, attempt_number=count + 1)
        questions = self._strip_answers(exam.questions)

        return {
            "id": attempt.id,
            "exam_id": exam.id,
            "started_at": attempt.started_at,
            "duration_minutes": exam.duration_minutes,
            "questions": questions,
        }

    def submit_attempt(
        self,
        attempt_id: int,
        student_id: int,
        data: AttemptSubmitRequest,
        background_tasks: BackgroundTasks,
        student_email: str,
        student_name: str,
    ) -> dict:
        attempt = self.attempt_repo.get_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
        if attempt.student_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your attempt")
        if attempt.status != AttemptStatusEnum.in_progress:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attempt already submitted")

        exam = self.exam_repo.get_by_id(attempt.exam_id)

        # Check time limit
        started = attempt.started_at
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        deadline = started + timedelta(minutes=exam.duration_minutes)
        timed_out = datetime.now(timezone.utc) > deadline

        # Build answer lookup
        answer_map = {a.question_id: a.selected_answer for a in data.answers}

        # Score the attempt
        total_score = 0.0
        processed_answers = []
        for q in exam.questions:
            qid = q["id"]
            selected = answer_map.get(qid, "")
            correct = q["correct_answer"]
            is_correct = selected == correct
            marks = q["marks"] if is_correct else 0
            total_score += marks
            processed_answers.append({
                "question_id": qid,
                "selected_answer": selected,
                "is_correct": is_correct,
                "marks_awarded": marks,
            })

        total_marks = exam.total_marks
        percentage = round((total_score / total_marks) * 100, 2) if total_marks > 0 else 0
        passed = percentage >= exam.pass_percentage
        final_status = AttemptStatusEnum.timed_out if timed_out else AttemptStatusEnum.submitted

        updated_attempt = self.attempt_repo.submit(
            attempt, score=total_score, percentage=percentage, passed=passed, status=final_status
        )
        self.attempt_repo.save_answers(attempt_id, processed_answers)

        # Background: send result notification
        background_tasks.add_task(
            send_result_notification,
            email=student_email,
            name=student_name,
            exam_title=exam.title,
            score=total_score,
            total=total_marks,
            percentage=percentage,
            passed=passed,
        )

        logger.info(f"Attempt {attempt_id} submitted: score={total_score}, passed={passed}")
        return {
            "id": updated_attempt.id,
            "exam_id": exam.id,
            "exam_title": exam.title,
            "status": updated_attempt.status,
            "score": total_score,
            "total_marks": total_marks,
            "percentage": percentage,
            "passed": passed,
            "started_at": updated_attempt.started_at,
            "submitted_at": updated_attempt.submitted_at,
            "time_taken_seconds": updated_attempt.time_taken_seconds,
            "attempt_number": updated_attempt.attempt_number,
        }

    def get_my_results(self, student_id: int, page: int = 1, page_size: int = 10) -> dict:
        skip = (page - 1) * page_size
        total, attempts = self.attempt_repo.get_student_attempts(student_id, skip=skip, limit=page_size)

        result = []
        for a in attempts:
            exam = a.exam
            result.append({
                "id": a.id,
                "exam_id": a.exam_id,
                "exam_title": exam.title if exam else "Unknown",
                "status": a.status,
                "score": a.score,
                "total_marks": exam.total_marks if exam else 0,
                "percentage": a.percentage,
                "passed": a.passed,
                "started_at": a.started_at,
                "submitted_at": a.submitted_at,
                "time_taken_seconds": a.time_taken_seconds,
                "attempt_number": a.attempt_number,
            })

        return {"total": total, "items": result}

    def _strip_answers(self, questions: list) -> list:
        """Remove correct_answer from questions before sending to student"""
        return [
            {
                "id": q["id"],
                "text": q["text"],
                "options": q["options"],
                "marks": q["marks"],
            }
            for q in questions
        ]
