from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f667b8b34583'
down_revision: Union[str, None] = '5743b97f3018'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

  pass


def downgrade() -> None:
    # Recreate the return_products table
    op.create_table('return_products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('box', sa.Integer(), nullable=True),
        sa.Column('amount_in_box', sa.Integer(), nullable=True),
        sa.Column('amount_in_package', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Use batch operations for products table
    with op.batch_alter_table('products') as batch_op:
        batch_op.add_column(sa.Column('ReturnProducts', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_products_return_products', 'return_products', ['ReturnProducts'], ['id'])
