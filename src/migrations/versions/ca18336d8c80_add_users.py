"""add users

Revision ID: ca18336d8c80
Revises: 
Create Date: 2026-07-12 18:23:07.911000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca18336d8c80'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('hashed_password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms')
    op.drop_table('users')
    op.drop_table('hotels')

