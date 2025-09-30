"""Add ordem and predecessora_id to etapas

Revision ID: 003
Revises: 002
Create Date: 2025-01-16 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # Add ordem column with default value 0
    op.add_column('etapas', sa.Column('ordem', sa.Integer(), nullable=True, default=0))
    
    # Add predecessora_id column (self-referencing foreign key)
    op.add_column('etapas', sa.Column('predecessora_id', sa.Integer(), nullable=True))
    
    # Create foreign key constraint for predecessora_id
    op.create_foreign_key('etapas_predecessora_id_fkey', 'etapas', 'etapas', ['predecessora_id'], ['id'])
    
    # Update existing records to have ordem = 0
    op.execute("UPDATE etapas SET ordem = 0 WHERE ordem IS NULL")

def downgrade():
    # Drop foreign key constraint
    op.drop_constraint('etapas_predecessora_id_fkey', 'etapas', type_='foreignkey')
    
    # Drop columns
    op.drop_column('etapas', 'predecessora_id')
    op.drop_column('etapas', 'ordem')