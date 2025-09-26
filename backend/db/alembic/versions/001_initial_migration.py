"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create habilidades table
    op.create_table('habilidades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_habilidades_id'), 'habilidades', ['id'], unique=False)
    op.create_index(op.f('ix_habilidades_nome'), 'habilidades', ['nome'], unique=True)

    # Create cargos table
    op.create_table('cargos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cargos_id'), 'cargos', ['id'], unique=False)
    op.create_index(op.f('ix_cargos_nome'), 'cargos', ['nome'], unique=True)

    # Create colaboradores table
    op.create_table('colaboradores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('cargo_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['cargo_id'], ['cargos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_colaboradores_id'), 'colaboradores', ['id'], unique=False)
    op.create_index(op.f('ix_colaboradores_nome'), 'colaboradores', ['nome'], unique=False)

    # Create projetos table
    op.create_table('projetos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('color', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projetos_id'), 'projetos', ['id'], unique=False)
    op.create_index(op.f('ix_projetos_nome'), 'projetos', ['nome'], unique=False)

    # Create ausencias table
    op.create_table('ausencias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colaborador_id', sa.Integer(), nullable=True),
        sa.Column('data', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ausencias_id'), 'ausencias', ['id'], unique=False)

    # Create etapas table
    op.create_table('etapas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('duracao_dias', sa.Integer(), nullable=True),
        sa.Column('projeto_id', sa.Integer(), nullable=True),
        sa.Column('cargo_necessario_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['cargo_necessario_id'], ['cargos.id'], ),
        sa.ForeignKeyConstraint(['projeto_id'], ['projetos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_etapas_id'), 'etapas', ['id'], unique=False)

    # Create association tables
    op.create_table('colaborador_habilidade',
        sa.Column('colaborador_id', sa.Integer(), nullable=False),
        sa.Column('habilidade_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
        sa.ForeignKeyConstraint(['habilidade_id'], ['habilidades.id'], ),
        sa.PrimaryKeyConstraint('colaborador_id', 'habilidade_id')
    )

    op.create_table('etapa_habilidade',
        sa.Column('etapa_id', sa.Integer(), nullable=False),
        sa.Column('habilidade_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['etapa_id'], ['etapas.id'], ),
        sa.ForeignKeyConstraint(['habilidade_id'], ['habilidades.id'], ),
        sa.PrimaryKeyConstraint('etapa_id', 'habilidade_id')
    )

def downgrade() -> None:
    op.drop_table('etapa_habilidade')
    op.drop_table('colaborador_habilidade')
    op.drop_index(op.f('ix_etapas_id'), table_name='etapas')
    op.drop_table('etapas')
    op.drop_index(op.f('ix_ausencias_id'), table_name='ausencias')
    op.drop_table('ausencias')
    op.drop_index(op.f('ix_projetos_nome'), table_name='projetos')
    op.drop_index(op.f('ix_projetos_id'), table_name='projetos')
    op.drop_table('projetos')
    op.drop_index(op.f('ix_colaboradores_nome'), table_name='colaboradores')
    op.drop_index(op.f('ix_colaboradores_id'), table_name='colaboradores')
    op.drop_table('colaboradores')
    op.drop_index(op.f('ix_cargos_nome'), table_name='cargos')
    op.drop_index(op.f('ix_cargos_id'), table_name='cargos')
    op.drop_table('cargos')
    op.drop_index(op.f('ix_habilidades_nome'), table_name='habilidades')
    op.drop_index(op.f('ix_habilidades_id'), table_name='habilidades')
    op.drop_table('habilidades')