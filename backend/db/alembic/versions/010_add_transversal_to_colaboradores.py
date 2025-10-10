"""add_transversal_to_colaboradores

Revision ID: 010
Revises: 009
Create Date: 2025-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('colaboradores', sa.Column('transversal', sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    op.drop_column('colaboradores', 'transversal')
