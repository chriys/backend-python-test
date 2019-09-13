"""set username column unique

Revision ID: cf49cde51836
Revises: ff85cb834c4f
Create Date: 2019-09-13 06:59:23.933137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf49cde51836'
down_revision = 'ff85cb834c4f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint('uq_users_username', ['username'])


def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_constraint('uq_users_username', type_='unique')

