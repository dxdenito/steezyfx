"""changed user table

Revision ID: d1961ba221d8
Revises: 
Create Date: 2025-07-06 00:20:40.008442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1961ba221d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=256), nullable=False))
        batch_op.drop_column('check_password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check_password_hash', sa.VARCHAR(length=256), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
