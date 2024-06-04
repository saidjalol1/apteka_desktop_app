"""usermodel changed

Revision ID: f6fce83bed63
Revises: f11a4ad2b6b1
Create Date: 2024-06-04 16:11:02.501703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6fce83bed63'
down_revision: Union[str, None] = 'f11a4ad2b6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('user_salaries')
    op.drop_table('user_scores')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_scores',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.Column('date_scored', sa.DATE(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_salaries',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('date_received', sa.DATE(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=True),
    sa.Column('amount_in_package', sa.INTEGER(), nullable=True),
    sa.Column('remainder', sa.INTEGER(), nullable=True),
    sa.Column('produced_location', sa.VARCHAR(), nullable=True),
    sa.Column('expiry_date', sa.DATE(), nullable=True),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
