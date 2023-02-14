"""empty message

Revision ID: 33a70e24647f
Revises: 523d8bb794f2
Create Date: 2023-01-09 05:09:53.200496

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33a70e24647f'
down_revision = '523d8bb794f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paymentdescription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_description', sa.String(length=128), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_paymentdescription_payment_description'), ['payment_description'])
        batch_op.drop_column('description')

    with op.batch_alter_table('paymentmethod', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_paymentmethod_payment_method'), ['payment_method'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paymentmethod', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_paymentmethod_payment_method'), type_='unique')

    with op.batch_alter_table('paymentdescription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', mysql.VARCHAR(length=128), nullable=True))
        batch_op.drop_constraint(batch_op.f('uq_paymentdescription_payment_description'), type_='unique')
        batch_op.drop_column('payment_description')

    # ### end Alembic commands ###