"""create posts table

Revision ID: 744cf87cf77b
Revises: 
Create Date: 2024-12-13 11:18:23.052467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '744cf87cf77b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the posts table
    op.create_table(
        'posts_3',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)  # Assuming you have a users table
    )


def downgrade() -> None:
    # Drop the post_3 table
    op.drop_table('posts_3')

