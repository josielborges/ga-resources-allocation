"""add_ativo_to_colaboradores

Revision ID: 013
Revises: 012
Create Date: 2025-01-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('colaboradores', sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    op.drop_column('colaboradores', 'ativo')
