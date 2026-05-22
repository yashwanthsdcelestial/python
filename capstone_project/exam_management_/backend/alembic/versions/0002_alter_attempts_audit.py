"""add audit columns to exam_attempts

Revision ID: 0002_alter_attempts_audit
Revises: 0001_initial
Create Date: 2025-01-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0002_alter_attempts_audit"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alters an existing table — demonstrates schema evolution
    op.add_column("exam_attempts", sa.Column("ip_address", sa.String(45), nullable=True))
    op.add_column("exam_attempts", sa.Column("user_agent", sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column("exam_attempts", "ip_address")
    op.drop_column("exam_attempts", "user_agent")
