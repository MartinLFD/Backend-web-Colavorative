"""empty message

Revision ID: 827b3b58d2b1
Revises: 41046fc0aeb7
Create Date: 2024-09-04 21:48:21.092469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827b3b58d2b1'
down_revision = '41046fc0aeb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campsite_image',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('campsite_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['campsite_id'], ['campsite.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campsite_rule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('campsite_id', sa.Integer(), nullable=False),
    sa.Column('rule', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['campsite_id'], ['campsite.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('campsite_detail')
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('contact_number')
        batch_op.drop_column('full_name')
        batch_op.drop_column('contact_email')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=15), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('phone')

    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_email', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('full_name', sa.VARCHAR(length=200), nullable=False))
        batch_op.add_column(sa.Column('contact_number', sa.VARCHAR(length=15), nullable=False))

    op.create_table('campsite_detail',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('campsite_id', sa.INTEGER(), nullable=False),
    sa.Column('image', sa.VARCHAR(length=100), nullable=False),
    sa.Column('rule', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['campsite_id'], ['campsite.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('campsite_rule')
    op.drop_table('campsite_image')
    # ### end Alembic commands ###
