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
    # Add new foreign key constraints with RESTRICT (drop and recreate)
    with op.batch_alter_table('colaboradores') as batch_op:
        batch_op.drop_constraint('colaboradores_cargo_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('colaboradores_cargo_id_fkey', 'cargos', ['cargo_id'], ['id'], ondelete='RESTRICT')
    
    with op.batch_alter_table('etapas') as batch_op:
        batch_op.drop_constraint('etapas_cargo_necessario_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('etapas_cargo_necessario_id_fkey', 'cargos', ['cargo_necessario_id'], ['id'], ondelete='RESTRICT')
    
    with op.batch_alter_table('colaborador_habilidade') as batch_op:
        batch_op.drop_constraint('colaborador_habilidade_habilidade_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('colaborador_habilidade_habilidade_id_fkey', 'habilidades', ['habilidade_id'], ['id'], ondelete='RESTRICT')
    
    with op.batch_alter_table('etapa_habilidade') as batch_op:
        batch_op.drop_constraint('etapa_habilidade_habilidade_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('etapa_habilidade_habilidade_id_fkey', 'habilidades', ['habilidade_id'], ['id'], ondelete='RESTRICT')

def downgrade():
    # Restore original foreign key constraints without RESTRICT
    with op.batch_alter_table('colaboradores') as batch_op:
        batch_op.drop_constraint('colaboradores_cargo_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('colaboradores_cargo_id_fkey', 'cargos', ['cargo_id'], ['id'])
    
    with op.batch_alter_table('etapas') as batch_op:
        batch_op.drop_constraint('etapas_cargo_necessario_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('etapas_cargo_necessario_id_fkey', 'cargos', ['cargo_necessario_id'], ['id'])
    
    with op.batch_alter_table('colaborador_habilidade') as batch_op:
        batch_op.drop_constraint('colaborador_habilidade_habilidade_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('colaborador_habilidade_habilidade_id_fkey', 'habilidades', ['habilidade_id'], ['id'])
    
    with op.batch_alter_table('etapa_habilidade') as batch_op:
        batch_op.drop_constraint('etapa_habilidade_habilidade_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('etapa_habilidade_habilidade_id_fkey', 'habilidades', ['habilidade_id'], ['id'])