"""Adding User model with mixin and connecting them.

Revision ID: 79aec24d1f0f
Revises: 565fa5d042c8
Create Date: 2020-04-23 00:13:11.348611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79aec24d1f0f'
down_revision = '565fa5d042c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'event', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'user_id')
    # ### end Alembic commands ###
