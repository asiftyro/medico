"""empty message

Revision ID: 3130feb4355a
Revises: a6be0279e2b3
Create Date: 2023-01-04 20:04:01.016229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3130feb4355a'
down_revision = 'a6be0279e2b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parcel_date_1', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('parcel_photo_1', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.drop_column('parcel_photo_1')
        batch_op.drop_column('parcel_date_1')

    # ### end Alembic commands ###
