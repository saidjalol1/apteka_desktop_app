"""Sale model changed

Revision ID: eeab32d9bd34
Revises: 68f4ed11e4b6
Create Date: 2024-06-24 17:28:53.545719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eeab32d9bd34'
down_revision: Union[str, None] = '68f4ed11e4b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sale', 'debt')
    op.drop_column('sale', 'card')
    op.drop_column('sale', 'cash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale', sa.Column('cash', sa.FLOAT(), nullable=True))
    op.add_column('sale', sa.Column('card', sa.FLOAT(), nullable=True))
    op.add_column('sale', sa.Column('debt', sa.FLOAT(), nullable=True))
    # ### end Alembic commands ###
