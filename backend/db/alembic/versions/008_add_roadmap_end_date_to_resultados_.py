"""add_roadmap_end_date_to_resultados_salvos

Revision ID: 008
Revises: 007
Create Date: 2025-10-09 16:32:43.112603

"""
from alembic import op
import sqlalchemy as sa


revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('resultados_salvos', sa.Column('roadmap_end_date', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('resultados_salvos', 'roadmap_end_date')