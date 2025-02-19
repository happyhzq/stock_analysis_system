# migrations/versions/xxxx_add_stock_price.py
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('stock_prices',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),\
        sa.Column('symbol', sa.String(length=10), nullable=False),\
        sa.Column('date', sa.DateTime(), nullable=False),\
        sa.Column('open_price', sa.Float(), nullable=True),\
        sa.Column('close_price', sa.Float(), nullable=True),\
        sa.Column('volume', sa.Integer(), nullable=True),\
        sa.ForeignKeyConstraint(['symbol'], ['financial_reports.symbol']),\
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('stock_prices')
    