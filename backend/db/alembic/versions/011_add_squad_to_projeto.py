"""add_squad_to_projeto

Revision ID: 011
Revises: 010
Create Date: 2025-10-10 16:39:28.878006

"""
from alembic import op
import sqlalchemy as sa


revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('projetos', sa.Column('squad_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projetos_squad', 'projetos', 'squads', ['squad_id'], ['id'], ondelete='RESTRICT')


def downgrade() -> None:
    op.drop_constraint('fk_projetos_squad', 'projetos', type_='foreignkey')
    op.drop_column('projetos', 'squad_id')