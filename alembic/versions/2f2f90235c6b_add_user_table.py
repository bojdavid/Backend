"""add user table

Revision ID: 2f2f90235c6b
Revises: 744cf87cf77b
Create Date: 2024-12-13 11:31:56.305099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2f90235c6b'
down_revision: Union[str, None] = '744cf87cf77b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
   # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False)
    )

def downgrade():
    # Drop the users table
    op.drop_table('users')
