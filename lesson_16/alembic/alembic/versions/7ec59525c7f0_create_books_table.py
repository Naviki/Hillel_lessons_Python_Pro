"""create_books_table

Revision ID: 7ec59525c7f0
Revises: 
Create Date: 2023-08-26 23:15:45.100087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec59525c7f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('date_of_release', sa.Date(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('genre', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('books')
