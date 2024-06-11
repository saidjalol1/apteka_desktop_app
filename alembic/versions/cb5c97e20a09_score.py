"""score

Revision ID: cb5c97e20a09
Revises: ca7da128f6c2
Create Date: 2024-06-11 10:55:01.431569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb5c97e20a09'
down_revision: Union[str, None] = 'ca7da128f6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('user_scores')
    op.drop_table('sale')
    op.drop_table('user_salaries')
    op.drop_table('sale_items')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sale_items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('amount_from_package', sa.INTEGER(), nullable=True),
    sa.Column('total_sum', sa.FLOAT(), nullable=True),
    sa.Column('Product', sa.INTEGER(), nullable=True),
    sa.Column('Sale', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['Product'], ['products.id'], ),
    sa.ForeignKeyConstraint(['Sale'], ['sale.id'], ),
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
    op.create_table('sale',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('date_added', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.BOOLEAN(), nullable=True),
    sa.Column('payment_type', sa.VARCHAR(), nullable=True),
    sa.Column('User', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_scores',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.Column('date_scored', sa.DATETIME(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.Column('product_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
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
    sa.Column('shift', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('serial_number', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('amount_in_package', sa.INTEGER(), nullable=True),
    sa.Column('remainder', sa.INTEGER(), nullable=True),
    sa.Column('produced_location', sa.VARCHAR(), nullable=True),
    sa.Column('expiry_date', sa.DATE(), nullable=True),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
