"""add rooms

Revision ID: a1b5e3ad293d
Revises: e940e79add56
Create Date: 2026-05-18 11:21:01.665576

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a1b5e3ad293d"
down_revision: Union[str, Sequence[str], None] = "e940e79add56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
