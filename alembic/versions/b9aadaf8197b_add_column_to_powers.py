"""Add column to powers

Revision ID: b9aadaf8197b
Revises: 3de60e5f53b3
Create Date: 2026-09-05 10:10:04.919952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9aadaf8197b'
down_revision: Union[str, Sequence[str], None] = '3de60e5f53b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('powers', sa.Column('description', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('powers', 'description')
    pass
