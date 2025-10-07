"""add_termino_to_projetos

Revision ID: 3c718fb0c5c0
Revises: 005
Create Date: 2025-10-07 11:16:49.730004

"""
from alembic import op
import sqlalchemy as sa


revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('projetos', sa.Column('termino', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('projetos', 'termino')