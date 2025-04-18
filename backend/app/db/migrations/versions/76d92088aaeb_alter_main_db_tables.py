"""alter main_db tables

Revision ID: 76d92088aaeb
Revises: abfb1ca2cc4c
Create Date: 2025-03-28 14:41:31.737743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '76d92088aaeb'
down_revision: Union[str, None] = 'abfb1ca2cc4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review_ratings',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('review_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('rating', sa.Float(), nullable=False),
                    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_review_ratings_id'), 'review_ratings', ['id'], unique=False)
    op.alter_column('reviews', 'review_rating',
                    existing_type=sa.INTEGER(),
                    type_=sa.Float(),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'review_rating',
                    existing_type=sa.Float(),
                    type_=sa.INTEGER(),
                    existing_nullable=False)
    op.drop_index(op.f('ix_review_ratings_id'), table_name='review_ratings')
    op.drop_table('review_ratings')
    # ### end Alembic commands ###
