"""Column type changed

Revision ID: 6a7f75432ce4
Revises: 1b9cb5938e63
Create Date: 2024-06-23 16:13:09.896253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a7f75432ce4'
down_revision: Union[str, None] = '1b9cb5938e63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_new')
    op.drop_column('products', 'expiry_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('expiry_date', sa.DATE(), nullable=True))
    op.create_table('products_new',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('serial_number', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('box', sa.INTEGER(), nullable=True),
    sa.Column('amount_in_box', sa.INTEGER(), nullable=True),
    sa.Column('amount_in_package', sa.INTEGER(), nullable=True),
    sa.Column('produced_location', sa.VARCHAR(), nullable=True),
    sa.Column('expiry_date', sa.VARCHAR(), nullable=True),
    sa.Column('base_price', sa.FLOAT(), nullable=True),
    sa.Column('extra_price_in_percent', sa.INTEGER(), nullable=True),
    sa.Column('sale_price', sa.FLOAT(), nullable=True),
    sa.Column('sale_price_in_percent', sa.FLOAT(), nullable=True),
    sa.Column('discount_price', sa.FLOAT(), nullable=True),
    sa.Column('overall_amount', sa.INTEGER(), nullable=True),
    sa.Column('type_id', sa.INTEGER(), nullable=True),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###