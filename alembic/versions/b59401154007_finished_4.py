"""finished 4

Revision ID: b59401154007
Revises: 104aec26f3d3
Create Date: 2024-07-30 10:13:14.183701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b59401154007'
down_revision: Union[str, None] = '104aec26f3d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card_id', sa.Column('number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card_id', 'number')
    # ### end Alembic commands ###
