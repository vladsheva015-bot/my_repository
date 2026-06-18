"""add users_new

Revision ID: 2bf9b88fbeaa
Revises: 71f5946d745f
Create Date: 2026-05-21 18:34:19.038525

"""

from typing import Sequence, Union

from alembic import op

revision: str = "2bf9b88fbeaa"
down_revision: Union[str, Sequence[str], None] = "71f5946d745f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
