"""Add gender column on player

Revision ID: 60449a02fafa
Revises: e572fbab5915
Create Date: 2026-09-05 10:42:30.692790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60449a02fafa'
down_revision: Union[str, Sequence[str], None] = 'e572fbab5915'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('powers', sa.Column('gender', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('player', 'gender')
    pass
