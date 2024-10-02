"""empty message

Revision ID: e5502c4b2d26
Revises: 5163e80d12d4
Create Date: 2024-09-30 19:22:21.538049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5502c4b2d26'
down_revision = '5163e80d12d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.add_column(sa.Column('binImage', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand', schema=None) as batch_op:
        batch_op.drop_column('binImage')

    # ### end Alembic commands ###
