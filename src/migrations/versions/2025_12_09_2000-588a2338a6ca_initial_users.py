"""initial Users

Revision ID: 588a2338a6ca
Revises: 75529248da3b
Create Date: 2025-12-09 20:00:09.597338

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "588a2338a6ca"
down_revision: Union[str, Sequence[str], None] = "75529248da3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_passworld", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
