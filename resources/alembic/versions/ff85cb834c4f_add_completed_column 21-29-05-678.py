"""add completed column

Revision ID: ff85cb834c4f
Revises:
Create Date: 2019-09-12 20:52:34.032735

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


# revision identifiers, used by Alembic.
revision = 'ff85cb834c4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('todos', sa.Column('completed', sa.Boolean(create_constraint=False), server_default=expression.false()))


def downgrade():
    op.drop_column('todos', 'completed')