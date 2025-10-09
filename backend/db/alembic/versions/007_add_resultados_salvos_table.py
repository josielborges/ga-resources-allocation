"""add_resultados_salvos_table

Revision ID: 007
Revises: 006
Create Date: 2025-10-09 15:02:46.499880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'resultados_salvos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('algoritmo', sa.String(), nullable=False),
        sa.Column('data_execucao', sa.DateTime(), nullable=True),
        sa.Column('melhor_fitness', sa.Float(), nullable=True),
        sa.Column('tarefas', JSON, nullable=True),
        sa.Column('historico_fitness', JSON, nullable=True),
        sa.Column('penalidades', JSON, nullable=True),
        sa.Column('ocorrencias_penalidades', JSON, nullable=True),
        sa.Column('parametros', JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resultados_salvos_id'), 'resultados_salvos', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_resultados_salvos_id'), table_name='resultados_salvos')
    op.drop_table('resultados_salvos')