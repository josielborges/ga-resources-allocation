"""add_inicio_field_to_projetos

Revision ID: 018
Revises: 017
Create Date: 2025-10-17 11:10:31.258681

"""
from alembic import op
import sqlalchemy as sa


revision = '018'
down_revision = '017'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('projetos', sa.Column('inicio', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('projetos', 'inicio')