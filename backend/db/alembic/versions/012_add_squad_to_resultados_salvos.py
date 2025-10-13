"""add_squad_to_resultados_salvos

Revision ID: 012
Revises: 011
Create Date: 2025-10-13 14:23:45.368296

"""
from alembic import op
import sqlalchemy as sa


revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('resultados_salvos', sa.Column('squad_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_resultados_salvos_squad', 'resultados_salvos', 'squads', ['squad_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_resultados_salvos_squad', 'resultados_salvos', type_='foreignkey')
    op.drop_column('resultados_salvos', 'squad_id')