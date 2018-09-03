"""empty message

Revision ID: 7171cd370743
Revises: 8e6e581f314c
Create Date: 2018-08-31 15:09:41.031660

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7171cd370743'
down_revision = '8e6e581f314c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###