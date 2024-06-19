"""product model changed

Revision ID: 964ee13775b7
Revises: 93fc8b8bbd22
Create Date: 2024-06-18 16:47:44.840680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '964ee13775b7'
down_revision: Union[str, None] = '93fc8b8bbd22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_scores')
    op.drop_table('users_shift')
    op.drop_table('user_salaries')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('sale_items')
    op.drop_table('sale')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sale',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('date_added', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('payment_type', sa.VARCHAR(), nullable=True),
    sa.Column('User', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sale_items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount_of_box', sa.INTEGER(), nullable=True),
    sa.Column('amount_of_package', sa.INTEGER(), nullable=True),
    sa.Column('amount_from_package', sa.INTEGER(), nullable=True),
    sa.Column('total_sum', sa.FLOAT(), nullable=True),
    sa.Column('Product', sa.INTEGER(), nullable=True),
    sa.Column('Sale', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['Product'], ['products.id'], ),
    sa.ForeignKeyConstraint(['Sale'], ['sale.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    sa.Column('shift_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['shift_id'], ['users_shift.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('serial_number', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('box', sa.INTEGER(), nullable=True),
    sa.Column('amount_in_box', sa.INTEGER(), nullable=True),
    sa.Column('amount_in_package', sa.INTEGER(), nullable=True),
    sa.Column('produced_location', sa.VARCHAR(), nullable=True),
    sa.Column('expiry_date', sa.DATE(), nullable=True),
    sa.Column('base_price', sa.FLOAT(), nullable=True),
    sa.Column('extra_price_in_percent', sa.INTEGER(), nullable=True),
    sa.Column('sale_price', sa.FLOAT(), nullable=True),
    sa.Column('sale_price_in_percent', sa.FLOAT(), nullable=True),
    sa.Column('discount_price', sa.FLOAT(), nullable=True),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_salaries',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('date_received', sa.DATETIME(), nullable=True),
    sa.Column('giver_id', sa.INTEGER(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['giver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_shift',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_scores',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.Column('date_scored', sa.DATETIME(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.Column('sale_item_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sale_item_id'], ['sale_items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###