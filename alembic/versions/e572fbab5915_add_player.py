"""Add player

Revision ID: e572fbab5915
Revises: b9aadaf8197b
Create Date: 2026-09-05 10:18:39.165337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e572fbab5915'
down_revision: Union[str, Sequence[str], None] = 'b9aadaf8197b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "player",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "age",
            sa.Integer(),
            server_default="18",
            nullable=False,
        ),
        sa.Column(
            "race",
            sa.String(),
            server_default="Human",
            nullable=False,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "awakened_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.CheckConstraint(
            "age >= 18",
            name="check_player_age",
        ),
    )

    pass


def downgrade() -> None:
    op.drop_table("player")

    pass
