"""empty message

Revision ID: c7ca3a1f95cb
Revises: 
Create Date: 2023-01-04 01:13:11.486342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ca3a1f95cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('fullname', sa.String(length=64), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('sex', sa.String(length=1), nullable=False),
    sa.Column('blood', sa.String(length=3), nullable=True),
    sa.Column('reference', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('avatar', sa.String(length=128), nullable=True),
    sa.Column('analysis', sa.Text(), nullable=True),
    sa.Column('case_photo_1', sa.String(length=128), nullable=True),
    sa.Column('case_photo_2', sa.String(length=128), nullable=True),
    sa.Column('case_photo_3', sa.String(length=128), nullable=True),
    sa.Column('case_photo_4', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.SmallInteger(), nullable=False),
    sa.Column('active', sa.SmallInteger(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_user_author_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('conversation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conversation', sa.String(length=128), nullable=True),
    sa.Column('read', sa.SmallInteger(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], name=op.f('fk_conversation_admin_id_user')),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_conversation_author_user')),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], name=op.f('fk_conversation_patient_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_conversation'))
    )
    op.create_table('medicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medicine', sa.String(length=128), nullable=True),
    sa.Column('potency', sa.String(length=128), nullable=True),
    sa.Column('short_name', sa.String(length=128), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_medicine_author_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_medicine')),
    sa.UniqueConstraint('short_name', name=op.f('uq_medicine_short_name'))
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('logo', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_organization_author_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_organization'))
    )
    op.create_table('prescription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prescription', sa.Text(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('follow_up_date', sa.Date(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_prescription_author_user')),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], name=op.f('fk_prescription_patient_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_prescription'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prescription')
    op.drop_table('organization')
    op.drop_table('medicine')
    op.drop_table('conversation')
    op.drop_table('user')
    # ### end Alembic commands ###
