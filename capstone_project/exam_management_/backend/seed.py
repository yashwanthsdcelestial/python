"""
Seed script — populates the database with realistic test data.
Run: python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.models import (
    User, Exam, ExamRegistration, ExamAttempt, StudentAnswer,
    RoleEnum, ExamStatusEnum, AttemptStatusEnum,
)
from datetime import datetime, timezone, timedelta


def seed():
    db = SessionLocal()
    try:
        # ── Users ──────────────────────────────────────────────────────────────
        admin1 = User(
            email="admin@examportal.com",
            hashed_password=get_password_hash("Admin@1234"),
            full_name="Alice Admin",
            role=RoleEnum.admin,
            is_active=True,
        )
        admin2 = User(
            email="proctor@examportal.com",
            hashed_password=get_password_hash("Admin@1234"),
            full_name="Bob Proctor",
            role=RoleEnum.admin,
            is_active=True,
        )
        student1 = User(
            email="student1@example.com",
            hashed_password=get_password_hash("Student@1234"),
            full_name="Charlie Brown",
            role=RoleEnum.student,
            is_active=True,
        )
        student2 = User(
            email="student2@example.com",
            hashed_password=get_password_hash("Student@1234"),
            full_name="Diana Prince",
            role=RoleEnum.student,
            is_active=True,
        )
        student3 = User(
            email="student3@example.com",
            hashed_password=get_password_hash("Student@1234"),
            full_name="Eve Johnson",
            role=RoleEnum.student,
            is_active=True,
        )

        db.add_all([admin1, admin2, student1, student2, student3])
        db.flush()

        # ── Exams ──────────────────────────────────────────────────────────────
        python_exam = Exam(
            title="Python Fundamentals",
            description="Test your knowledge of Python basics including data types, loops, and functions.",
            duration_minutes=45,
            total_marks=50,
            pass_percentage=60.0,
            max_attempts=2,
            status=ExamStatusEnum.published,
            created_by=admin1.id,
            questions=[
                {"id": 1, "text": "What is the output of print(type([]))?", "options": ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>", "<class 'set'>"], "correct_answer": "<class 'list'>", "marks": 5},
                {"id": 2, "text": "Which keyword is used to define a function in Python?", "options": ["func", "def", "function", "define"], "correct_answer": "def", "marks": 5},
                {"id": 3, "text": "What does len([1,2,3]) return?", "options": ["2", "3", "4", "0"], "correct_answer": "3", "marks": 5},
                {"id": 4, "text": "Which of these is immutable?", "options": ["list", "dict", "tuple", "set"], "correct_answer": "tuple", "marks": 5},
                {"id": 5, "text": "What is 2 ** 3 in Python?", "options": ["6", "8", "9", "5"], "correct_answer": "8", "marks": 5},
                {"id": 6, "text": "How do you start a comment in Python?", "options": ["//", "/*", "#", "--"], "correct_answer": "#", "marks": 5},
                {"id": 7, "text": "Which method adds an item to a list?", "options": ["add()", "append()", "insert_last()", "push()"], "correct_answer": "append()", "marks": 5},
                {"id": 8, "text": "What is the result of bool(0)?", "options": ["True", "False", "None", "0"], "correct_answer": "False", "marks": 5},
                {"id": 9, "text": "Which loop is used when number of iterations is known?", "options": ["while", "for", "do-while", "repeat"], "correct_answer": "for", "marks": 5},
                {"id": 10, "text": "What does range(3) produce?", "options": ["[1,2,3]", "[0,1,2]", "[0,1,2,3]", "[1,2]"], "correct_answer": "[0,1,2]", "marks": 5},
            ],
        )

        sql_exam = Exam(
            title="SQL Basics",
            description="Covers SELECT, JOIN, GROUP BY, and basic SQL concepts.",
            duration_minutes=30,
            total_marks=40,
            pass_percentage=50.0,
            max_attempts=1,
            status=ExamStatusEnum.published,
            created_by=admin1.id,
            questions=[
                {"id": 1, "text": "Which SQL clause filters rows?", "options": ["HAVING", "WHERE", "GROUP BY", "ORDER BY"], "correct_answer": "WHERE", "marks": 10},
                {"id": 2, "text": "Which JOIN returns all rows from both tables?", "options": ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"], "correct_answer": "FULL OUTER JOIN", "marks": 10},
                {"id": 3, "text": "What does COUNT(*) do?", "options": ["Counts non-null values", "Counts all rows", "Counts distinct values", "Sums values"], "correct_answer": "Counts all rows", "marks": 10},
                {"id": 4, "text": "Which clause is used with aggregate functions?", "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"], "correct_answer": "HAVING", "marks": 10},
            ],
        )

        draft_exam = Exam(
            title="Data Structures Advanced",
            description="Trees, graphs, and dynamic programming.",
            duration_minutes=90,
            total_marks=100,
            pass_percentage=70.0,
            max_attempts=1,
            status=ExamStatusEnum.draft,
            created_by=admin2.id,
            questions=[
                {"id": 1, "text": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "correct_answer": "O(log n)", "marks": 10},
            ],
        )

        db.add_all([python_exam, sql_exam, draft_exam])
        db.flush()

        # ── Enrollments ────────────────────────────────────────────────────────
        reg1 = ExamRegistration(student_id=student1.id, exam_id=python_exam.id)
        reg2 = ExamRegistration(student_id=student1.id, exam_id=sql_exam.id)
        reg3 = ExamRegistration(student_id=student2.id, exam_id=python_exam.id)
        reg4 = ExamRegistration(student_id=student3.id, exam_id=sql_exam.id)

        db.add_all([reg1, reg2, reg3, reg4])
        db.flush()

        # ── Attempts ───────────────────────────────────────────────────────────
        now = datetime.now(timezone.utc)

        attempt1 = ExamAttempt(
            student_id=student1.id,
            exam_id=python_exam.id,
            status=AttemptStatusEnum.submitted,
            score=40.0,
            percentage=80.0,
            passed=True,
            started_at=now - timedelta(hours=2),
            submitted_at=now - timedelta(hours=1, minutes=30),
            time_taken_seconds=1800,
            attempt_number=1,
        )
        attempt2 = ExamAttempt(
            student_id=student2.id,
            exam_id=python_exam.id,
            status=AttemptStatusEnum.submitted,
            score=25.0,
            percentage=50.0,
            passed=False,
            started_at=now - timedelta(hours=3),
            submitted_at=now - timedelta(hours=2, minutes=30),
            time_taken_seconds=1500,
            attempt_number=1,
        )
        attempt3 = ExamAttempt(
            student_id=student1.id,
            exam_id=sql_exam.id,
            status=AttemptStatusEnum.submitted,
            score=30.0,
            percentage=75.0,
            passed=True,
            started_at=now - timedelta(days=1),
            submitted_at=now - timedelta(days=1) + timedelta(minutes=25),
            time_taken_seconds=1500,
            attempt_number=1,
        )

        db.add_all([attempt1, attempt2, attempt3])
        db.flush()

        # ── Answers for attempt1 (student1 on python_exam) ────────────────────
        answers_a1 = [
            StudentAnswer(attempt_id=attempt1.id, question_id=1, selected_answer="<class 'list'>", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=2, selected_answer="def", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=3, selected_answer="3", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=4, selected_answer="tuple", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=5, selected_answer="8", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=6, selected_answer="#", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=7, selected_answer="append()", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=8, selected_answer="False", is_correct=True, marks_awarded=5),
            StudentAnswer(attempt_id=attempt1.id, question_id=9, selected_answer="while", is_correct=False, marks_awarded=0),
            StudentAnswer(attempt_id=attempt1.id, question_id=10, selected_answer="[1,2,3]", is_correct=False, marks_awarded=0),
        ]
        db.add_all(answers_a1)
        db.commit()

        print("✅ Seed complete!")
        print("\n📋 Sample Credentials:")
        print("  Admin:   admin@examportal.com   / Admin@1234")
        print("  Admin:   proctor@examportal.com / Admin@1234")
        print("  Student: student1@example.com   / Student@1234")
        print("  Student: student2@example.com   / Student@1234")
        print("  Student: student3@example.com   / Student@1234")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
