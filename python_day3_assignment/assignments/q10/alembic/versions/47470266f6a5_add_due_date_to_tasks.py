"""add due_date to tasks

Revision ID: 47470266f6a5
Revises: 4ee055285ff5
Create Date: 2026-03-24 22:17:09.263536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '47470266f6a5'
down_revision: Union[str, Sequence[str], None] = '4ee055285ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('app_tasks', sa.Column('due_date', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('app_tasks', 'due_date')
