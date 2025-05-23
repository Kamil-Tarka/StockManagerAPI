"""Init migration

Revision ID: 226b6f30bb67
Revises: 
Create Date: 2025-03-12 14:11:52.241663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '226b6f30bb67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('last_modification_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('last_modification_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('last_modification_date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['item_category.id'], name='fk_StockItem_category_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('fk_StockItem_category_id', 'stock_item', ['category_id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('last_modification_date', sa.DateTime(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='fk_User_Role_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('fk_User_Role_id', 'user', ['role_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fk_User_Role_id', table_name='user')
    op.drop_table('user')
    op.drop_index('fk_StockItem_category_id', table_name='stock_item')
    op.drop_table('stock_item')
    op.drop_table('role')
    op.drop_table('item_category')
    # ### end Alembic commands ###
