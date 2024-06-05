"""UserSalary changed

Revision ID: f6250f15f4e0
Revises: 500f2c562778
Create Date: 2024-06-05 08:32:09.825495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6250f15f4e0'
down_revision: Union[str, None] = '500f2c562778'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_scores')
    op.drop_table('user_salaries')
    op.drop_table('products')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('born_date', sa.DATE(), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), nullable=True),
    sa.Column('address', sa.VARCHAR(), nullable=True),
    sa.Column('shift', sa.INTEGER(), nullable=True),
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
    op.create_table('user_salaries',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('date_received', sa.DATE(), nullable=True),
    sa.Column('giver_id', sa.INTEGER(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['giver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_scores',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.Column('date_scored', sa.DATE(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
