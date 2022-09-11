"""create relations table

Revision ID: be96f5df5d95
Revises: 556533be7244
Create Date: 2022-09-12 00:21:40.646566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be96f5df5d95'
down_revision = '556533be7244'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relations_table',
    sa.Column('parent_id', sa.String(), nullable=False),
    sa.Column('child_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['child_id'], ['nodes.id'], name=op.f('fk__relations_table__child_id__nodes')),
    sa.ForeignKeyConstraint(['parent_id'], ['nodes.id'], name=op.f('fk__relations_table__parent_id__nodes')),
    sa.PrimaryKeyConstraint('parent_id', 'child_id', name=op.f('pk__relations_table'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relations_table')
    # ### end Alembic commands ###