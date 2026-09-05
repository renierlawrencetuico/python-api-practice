"""Create powers table

Revision ID: 3de60e5f53b3
Revises: 
Create Date: 2026-09-05 09:59:15.910859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3de60e5f53b3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('powers', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('name', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('powers')
    pass
