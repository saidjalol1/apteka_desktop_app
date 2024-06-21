"""Move person column from product to sale

Revision ID: 372a9ceac0ec
Revises: 
Create Date: 2024-06-21 14:36:28.224937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '372a9ceac0ec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('products', 'person')

def downgrade() -> None:
    op.add_column('products', sa.Column('person', sa.String(), nullable=True))