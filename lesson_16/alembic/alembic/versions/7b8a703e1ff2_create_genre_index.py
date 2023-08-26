"""create_genre_index

Revision ID: 7b8a703e1ff2
Revises: 7ec59525c7f0
Create Date: 2023-08-26 23:20:16.367719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8a703e1ff2'
down_revision: Union[str, None] = '7ec59525c7f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index('idx_genre', 'books', ['genre'], unique=False)


def downgrade():
    op.drop_index('ix_genre', table_name='books')
