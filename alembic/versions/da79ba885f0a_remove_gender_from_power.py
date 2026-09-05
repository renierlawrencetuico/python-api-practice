"""remove gender from power

Revision ID: da79ba885f0a
Revises: 60449a02fafa
Create Date: 2026-09-05 10:47:33.876765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da79ba885f0a'
down_revision: Union[str, Sequence[str], None] = '60449a02fafa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('powers', 'gender')
    op.add_column('player', sa.Column('gender', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('powers', sa.Column('gender', sa.String(), nullable=False))
    pass
