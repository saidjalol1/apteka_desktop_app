"""Sale model changed

Revision ID: 68f4ed11e4b6
Revises: 2bd2b83d3e43
Create Date: 2024-06-24 17:27:45.319631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68f4ed11e4b6'
down_revision: Union[str, None] = '2bd2b83d3e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
