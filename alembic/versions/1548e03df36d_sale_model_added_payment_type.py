"""Sale model added payment_type

Revision ID: 1548e03df36d
Revises: 7d5a45fc85b2
Create Date: 2024-06-23 14:27:40.712580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1548e03df36d'
down_revision: Union[str, None] = '7d5a45fc85b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale', sa.Column('payment_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sale', 'payment_type')
    # ### end Alembic commands ###
