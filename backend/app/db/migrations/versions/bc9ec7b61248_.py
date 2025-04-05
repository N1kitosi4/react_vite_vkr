"""empty message

Revision ID: bc9ec7b61248
Revises: efee7e3edcb8
Create Date: 2025-02-25 09:43:26.524270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc9ec7b61248'
down_revision: Union[str, None] = 'efee7e3edcb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
