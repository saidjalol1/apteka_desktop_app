"""image field added

Revision ID: e8b043351ed6
Revises: 7a3214521635
Create Date: 2024-06-19 18:21:15.528527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision: str = 'e8b043351ed6'
down_revision: Union[str, None] = '7a3214521635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('check_layout',
                  Column('image', String, nullable=True)
                  )


def downgrade() -> None:
    op.drop_column('check_layout', 'image')
