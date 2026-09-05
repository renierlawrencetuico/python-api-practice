"""Add more columns to powers

Revision ID: 2b357bf3269a
Revises: da79ba885f0a
Create Date: 2026-09-05 10:50:58.336371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b357bf3269a'
down_revision: Union[str, Sequence[str], None] = 'da79ba885f0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "powers",
        sa.Column(
            "damage",
            sa.Integer(),
            server_default="0",
            nullable=False
        )
    )

    op.add_column(
        "powers",
        sa.Column(
            "learned_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        )
    )

    op.add_column(
        "powers",
        sa.Column(
            "player_id",
            sa.Integer(),
            nullable=False
        )
    )

    op.create_foreign_key(
        "power_player_id",
        "powers",
        "player",
        ["player_id"],
        ["id"],
        ondelete="CASCADE"
    )

    pass


def downgrade() -> None:
    op.drop_constraint(
        None,
        "powers",
        type_="foreignkey"
    )

    op.drop_column("powers", "player_id")
    op.drop_column("powers", "learned_at")
    op.drop_column("powers", "damage")

    pass
