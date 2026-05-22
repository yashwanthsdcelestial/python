import logging
from typing import Optional, List, Tuple
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import ExamAttempt, StudentAnswer, AttemptStatusEnum

logger = logging.getLogger(__name__)


class AttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, attempt_id: int) -> Optional[ExamAttempt]:
        return self.db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()

    def get_in_progress(self, student_id: int, exam_id: int) -> Optional[ExamAttempt]:
        return self.db.query(ExamAttempt).filter(
            ExamAttempt.student_id == student_id,
            ExamAttempt.exam_id == exam_id,
            ExamAttempt.status == AttemptStatusEnum.in_progress,
        ).first()

    def count_attempts(self, student_id: int, exam_id: int) -> int:
        return self.db.query(func.count(ExamAttempt.id)).filter(
            ExamAttempt.student_id == student_id,
            ExamAttempt.exam_id == exam_id,
        ).scalar()

    def create(self, student_id: int, exam_id: int, attempt_number: int) -> ExamAttempt:
        attempt = ExamAttempt(
            student_id=student_id,
            exam_id=exam_id,
            attempt_number=attempt_number,
            status=AttemptStatusEnum.in_progress,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def submit(
        self,
        attempt: ExamAttempt,
        score: float,
        percentage: float,
        passed: bool,
        status: AttemptStatusEnum = AttemptStatusEnum.submitted,
    ) -> ExamAttempt:
        now = datetime.now(timezone.utc)
        attempt.status = status
        attempt.score = score
        attempt.percentage = percentage
        attempt.passed = passed
        attempt.submitted_at = now
        if attempt.started_at:
            started = attempt.started_at
            if started.tzinfo is None:
                from datetime import timezone as tz
                started = started.replace(tzinfo=tz.utc)
            attempt.time_taken_seconds = int((now - started).total_seconds())
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def save_answers(self, attempt_id: int, answers: List[dict]) -> None:
        for ans in answers:
            answer = StudentAnswer(
                attempt_id=attempt_id,
                question_id=ans["question_id"],
                selected_answer=ans["selected_answer"],
                is_correct=ans["is_correct"],
                marks_awarded=ans["marks_awarded"],
            )
            self.db.add(answer)
        self.db.commit()

    def get_student_attempts(self, student_id: int, skip: int = 0, limit: int = 20) -> Tuple[int, List[ExamAttempt]]:
        query = self.db.query(ExamAttempt).filter(ExamAttempt.student_id == student_id)
        total = query.count()
        items = query.order_by(ExamAttempt.started_at.desc()).offset(skip).limit(limit).all()
        return total, items

    def count_total(self) -> int:
        return self.db.query(func.count(ExamAttempt.id)).scalar()

    def count_passed(self) -> int:
        return self.db.query(func.count(ExamAttempt.id)).filter(ExamAttempt.passed == True).scalar()

    def get_student_stats(self, student_id: int) -> dict:
        total = self.db.query(func.count(ExamAttempt.id)).filter(
            ExamAttempt.student_id == student_id,
            ExamAttempt.status != AttemptStatusEnum.in_progress,
        ).scalar()
        passed = self.db.query(func.count(ExamAttempt.id)).filter(
            ExamAttempt.student_id == student_id,
            ExamAttempt.passed == True,
        ).scalar()
        avg_score = self.db.query(func.avg(ExamAttempt.percentage)).filter(
            ExamAttempt.student_id == student_id,
            ExamAttempt.percentage.isnot(None),
        ).scalar()
        return {"completed": total, "passed": passed, "avg_score": round(avg_score, 2) if avg_score else None}
