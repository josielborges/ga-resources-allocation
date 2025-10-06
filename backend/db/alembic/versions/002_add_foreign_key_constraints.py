"""Add foreign key constraints

Revision ID: 002
Revises: 001
Create Date: 2025-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Add RESTRICT to existing foreign key constraints
    try:
        op.drop_constraint('colaboradores_cargo_id_fkey', 'colaboradores', type_='foreignkey')
    except:
        pass
    op.create_foreign_key('colaboradores_cargo_id_fkey', 'colaboradores', 'cargos', ['cargo_id'], ['id'], ondelete='RESTRICT')
    
    try:
        op.drop_constraint('etapas_cargo_necessario_id_fkey', 'etapas', type_='foreignkey')
    except:
        pass
    op.create_foreign_key('etapas_cargo_necessario_id_fkey', 'etapas', 'cargos', ['cargo_necessario_id'], ['id'], ondelete='RESTRICT')
    
    try:
        op.drop_constraint('colaborador_habilidade_habilidade_id_fkey', 'colaborador_habilidade', type_='foreignkey')
    except:
        pass
    op.create_foreign_key('colaborador_habilidade_habilidade_id_fkey', 'colaborador_habilidade', 'habilidades', ['habilidade_id'], ['id'], ondelete='RESTRICT')
    
    try:
        op.drop_constraint('etapa_habilidade_habilidade_id_fkey', 'etapa_habilidade', type_='foreignkey')
    except:
        pass
    op.create_foreign_key('etapa_habilidade_habilidade_id_fkey', 'etapa_habilidade', 'habilidades', ['habilidade_id'], ['id'], ondelete='RESTRICT')

def downgrade():
    op.drop_constraint('colaboradores_cargo_id_fkey', 'colaboradores', type_='foreignkey')
    op.create_foreign_key('colaboradores_cargo_id_fkey', 'colaboradores', 'cargos', ['cargo_id'], ['id'])
    
    op.drop_constraint('etapas_cargo_necessario_id_fkey', 'etapas', type_='foreignkey')
    op.create_foreign_key('etapas_cargo_necessario_id_fkey', 'etapas', 'cargos', ['cargo_necessario_id'], ['id'])
    
    op.drop_constraint('colaborador_habilidade_habilidade_id_fkey', 'colaborador_habilidade', type_='foreignkey')
    op.create_foreign_key('colaborador_habilidade_habilidade_id_fkey', 'colaborador_habilidade', 'habilidades', ['habilidade_id'], ['id'])
    
    op.drop_constraint('etapa_habilidade_habilidade_id_fkey', 'etapa_habilidade', type_='foreignkey')
    op.create_foreign_key('etapa_habilidade_habilidade_id_fkey', 'etapa_habilidade', 'habilidades', ['habilidade_id'], ['id'])