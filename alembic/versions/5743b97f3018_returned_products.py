from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5743b97f3018'
down_revision: Union[str, None] = 'eeab32d9bd34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the table if it exists
    conn = op.get_bind()
    if conn.dialect.has_table(conn, 'return_products'):
        op.drop_table('return_products')

    # Create the table
    op.create_table('return_products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('box', sa.Integer(), nullable=True),
        sa.Column('amount_in_box', sa.Integer(), nullable=True),
        sa.Column('amount_in_package', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add the column and foreign key to the products table
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ReturnProducts', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_products_return_products', 'return_products', ['ReturnProducts'], ['id'])


def downgrade() -> None:
    # Drop the foreign key and column from the products table
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('fk_products_return_products', type_='foreignkey')
        batch_op.drop_column('ReturnProducts')

    # Drop the return_products table
    op.drop_table('return_products')
