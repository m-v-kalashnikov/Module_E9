"""Adding User model with mixin.

Revision ID: 565fa5d042c8
Revises: b303a77ed21c
Create Date: 2020-04-22 23:59:13.932405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '565fa5d042c8'
down_revision = 'b303a77ed21c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
