"""empty message

Revision ID: 9004ba3c948c
Revises: 33a70e24647f
Create Date: 2023-01-10 04:49:09.372178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9004ba3c948c'
down_revision = '33a70e24647f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paymenttracker', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_description', sa.String(length=128), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paymenttracker', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', mysql.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('payment_description')

    # ### end Alembic commands ###
