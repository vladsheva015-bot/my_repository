"""add users

Revision ID: 71f5946d745f
Revises: a1b5e3ad293d
Create Date: 2026-05-21 17:46:24.839369

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "71f5946d745f"
down_revision: Union[str, Sequence[str], None] = "a1b5e3ad293d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
