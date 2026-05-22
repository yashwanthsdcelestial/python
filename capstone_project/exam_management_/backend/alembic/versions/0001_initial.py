"""initial schema with all tables and view

Revision ID: 0001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("admin", "student", name="roleenum"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_email_active", "users", ["email", "is_active"])

    # ── exams ──────────────────────────────────────────────────────────────────
    op.create_table(
        "exams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("total_marks", sa.Float(), nullable=False, server_default="100"),
        sa.Column("pass_percentage", sa.Float(), nullable=False, server_default="50.0"),
        sa.Column("status", sa.Enum("draft", "published", "archived", name="examstatusenum"), nullable=False, server_default="draft"),
        sa.Column("questions", postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("max_attempts", sa.Integer(), server_default="1"),
        sa.Column("start_time", sa.DateTime(timezone=True)),
        sa.Column("end_time", sa.DateTime(timezone=True)),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_exams_title", "exams", ["title"])
    op.create_index("ix_exams_status", "exams", ["status"])
    op.create_index("ix_exams_created_by", "exams", ["created_by"])

    # ── exam_registrations ─────────────────────────────────────────────────────
    op.create_table(
        "exam_registrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exam_id", sa.Integer(), sa.ForeignKey("exams.id"), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_exam_reg_student_exam", "exam_registrations", ["student_id", "exam_id"], unique=True)

    # ── exam_attempts ──────────────────────────────────────────────────────────
    op.create_table(
        "exam_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exam_id", sa.Integer(), sa.ForeignKey("exams.id"), nullable=False),
        sa.Column("status", sa.Enum("in_progress", "submitted", "timed_out", name="attemptstatusenum"), nullable=False, server_default="in_progress"),
        sa.Column("score", sa.Float()),
        sa.Column("percentage", sa.Float()),
        sa.Column("passed", sa.Boolean()),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True)),
        sa.Column("time_taken_seconds", sa.Integer()),
        sa.Column("attempt_number", sa.Integer(), server_default="1"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attempts_student_exam", "exam_attempts", ["student_id", "exam_id"])

    # ── student_answers ────────────────────────────────────────────────────────
    op.create_table(
        "student_answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("exam_attempts.id"), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("selected_answer", sa.String(500)),
        sa.Column("is_correct", sa.Boolean()),
        sa.Column("marks_awarded", sa.Float(), server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_answers_attempt_question", "student_answers", ["attempt_id", "question_id"])

    # ── Database VIEW ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE OR REPLACE VIEW vw_student_exam_summary AS
        SELECT
            u.id          AS student_id,
            u.full_name   AS student_name,
            u.email       AS student_email,
            e.id          AS exam_id,
            e.title       AS exam_title,
            COUNT(ea.id)  AS total_attempts,
            MAX(ea.score) AS best_score,
            e.total_marks,
            ROUND(CAST(MAX(ea.percentage) AS NUMERIC), 2) AS best_percentage,
            BOOL_OR(ea.passed)  AS ever_passed,
            er.registered_at
        FROM exam_registrations er
        JOIN users u   ON u.id  = er.student_id
        JOIN exams e   ON e.id  = er.exam_id
        LEFT JOIN exam_attempts ea ON ea.student_id = er.student_id AND ea.exam_id = er.exam_id
        WHERE u.is_deleted = false AND e.is_deleted = false
        GROUP BY u.id, u.full_name, u.email, e.id, e.title, e.total_marks, er.registered_at
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS vw_student_exam_summary")
    op.drop_table("student_answers")
    op.drop_table("exam_attempts")
    op.drop_table("exam_registrations")
    op.drop_table("exams")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS attemptstatusenum")
    op.execute("DROP TYPE IF EXISTS examstatusenum")
    op.execute("DROP TYPE IF EXISTS roleenum")
