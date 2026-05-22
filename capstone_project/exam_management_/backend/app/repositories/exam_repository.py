import logging
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.models import Exam, ExamRegistration, ExamStatusEnum

logger = logging.getLogger(__name__)


class ExamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, exam_id: int) -> Optional[Exam]:
        return self.db.query(Exam).filter(Exam.id == exam_id, Exam.is_deleted == False).first()

    def create(self, data: dict) -> Exam:
        exam = Exam(**data)
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        logger.info(f"Created exam: {exam.title}")
        return exam

    def update(self, exam: Exam, data: dict) -> Exam:
        for key, value in data.items():
            if value is not None:
                setattr(exam, key, value)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def soft_delete(self, exam: Exam) -> Exam:
        exam.is_deleted = True
        self.db.commit()
        return exam

    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[ExamStatusEnum] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> Tuple[int, List[Exam]]:
        query = self.db.query(Exam).filter(Exam.is_deleted == False)

        if status:
            query = query.filter(Exam.status == status)
        if search:
            query = query.filter(
                or_(Exam.title.ilike(f"%{search}%"), Exam.description.ilike(f"%{search}%"))
            )

        col = getattr(Exam, sort_by, Exam.created_at)
        query = query.order_by(col.desc() if sort_desc else col.asc())

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def count_all(self) -> int:
        return self.db.query(func.count(Exam.id)).filter(Exam.is_deleted == False).scalar()

    def count_by_status(self, status: ExamStatusEnum) -> int:
        return self.db.query(func.count(Exam.id)).filter(
            Exam.status == status, Exam.is_deleted == False
        ).scalar()


class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_enrollment(self, student_id: int, exam_id: int) -> Optional[ExamRegistration]:
        return self.db.query(ExamRegistration).filter(
            ExamRegistration.student_id == student_id,
            ExamRegistration.exam_id == exam_id,
            ExamRegistration.is_active == True,
        ).first()

    def create(self, student_id: int, exam_id: int) -> ExamRegistration:
        reg = ExamRegistration(student_id=student_id, exam_id=exam_id)
        self.db.add(reg)
        self.db.commit()
        self.db.refresh(reg)
        return reg

    def get_student_enrollments(self, student_id: int, skip: int = 0, limit: int = 20) -> Tuple[int, List[ExamRegistration]]:
        query = self.db.query(ExamRegistration).filter(
            ExamRegistration.student_id == student_id,
            ExamRegistration.is_active == True,
        )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items

    def get_exam_enrollments(self, exam_id: int) -> List[ExamRegistration]:
        return self.db.query(ExamRegistration).filter(
            ExamRegistration.exam_id == exam_id,
            ExamRegistration.is_active == True,
        ).all()
