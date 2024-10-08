"""product model changed

Revision ID: 99029da4abd2
Revises: c4ca5226e740
Create Date: 2024-08-17 10:28:46.597653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99029da4abd2'
down_revision: Union[str, None] = 'c4ca5226e740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('return_items', 'amount_of_box')
    op.drop_column('sale_items', 'amount_of_box')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale_items', sa.Column('amount_of_box', sa.INTEGER(), nullable=True))
    op.add_column('return_items', sa.Column('amount_of_box', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
