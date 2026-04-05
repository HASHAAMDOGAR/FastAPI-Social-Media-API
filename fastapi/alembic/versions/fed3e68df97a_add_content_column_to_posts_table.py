"""add content column to posts table

Revision ID: fed3e68df97a
Revises: 929e55f82db8
Create Date: 2026-04-05 13:25:26.854775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed3e68df97a'
down_revision: Union[str, Sequence[str], None] = '929e55f82db8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
