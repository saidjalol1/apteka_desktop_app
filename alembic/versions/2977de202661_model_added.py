from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '2977de202661'
down_revision = 'e8b043351ed6'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Create category table
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Create products_new table with type_id
    op.create_table(
        'products_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('serial_number', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('box', sa.Integer(), nullable=True),
        sa.Column('amount_in_box', sa.Integer(), nullable=True),
        sa.Column('amount_in_package', sa.Integer(), nullable=True),
        sa.Column('produced_location', sa.String(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=True),
        sa.Column('extra_price_in_percent', sa.Integer(), nullable=True),
        sa.Column('sale_price', sa.Float(), nullable=True),
        sa.Column('sale_price_in_percent', sa.Float(), nullable=True),
        sa.Column('discount_price', sa.Float(), nullable=True),
        sa.Column('overall_amount', sa.Integer(), nullable=True, default=0),
        sa.Column('type_id', sa.Integer(), sa.ForeignKey('category.id'), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True)
    )

    # Step 3: Copy data from products to products_new
    op.execute("INSERT INTO products_new SELECT * FROM products")

    # Step 4: Drop the original products table
    op.drop_table('products')

    # Step 5: Rename products_new to products
    op.rename_table('products_new', 'products')

def downgrade():
    # Step 1: Drop products table
    op.drop_table('products')

    # Step 2: Create products table without type_id
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('serial_number', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('box', sa.Integer(), nullable=True),
        sa.Column('amount_in_box', sa.Integer(), nullable=True),
        sa.Column('amount_in_package', sa.Integer(), nullable=True),
        sa.Column('produced_location', sa.String(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=True),
        sa.Column('extra_price_in_percent', sa.Integer(), nullable=True),
        sa.Column('sale_price', sa.Float(), nullable=True),
        sa.Column('sale_price_in_percent', sa.Float(), nullable=True),
        sa.Column('discount_price', sa.Float(), nullable=True),
        sa.Column('overall_amount', sa.Integer(), nullable=True, default=0),
        sa.Column('score', sa.Integer(), nullable=True)
    )

    # Step 3: Copy data from products_new to products
    op.execute("INSERT INTO products SELECT * FROM products_new")

    # Step 4: Drop the original products_new table
    op.drop_table('products_new')

    # Step 5: Drop category table
    op.drop_table('category')
