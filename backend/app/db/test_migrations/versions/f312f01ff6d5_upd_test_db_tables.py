"""Upd test_db tables

Revision ID: f312f01ff6d5
Revises: 3c0f787a60ed
Create Date: 2025-03-08 16:23:39.883599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f312f01ff6d5'
down_revision: Union[str, None] = '3c0f787a60ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###
