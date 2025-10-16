"""add_work_period_and_vacation_to_colaborador

Revision ID: 017
Revises: 016
Create Date: 2025-10-15 17:05:18.063644

"""
from alembic import op
import sqlalchemy as sa


revision = '017'
down_revision = '016'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add work period columns to colaboradores
    op.add_column('colaboradores', sa.Column('inicio', sa.Date(), nullable=True))
    op.add_column('colaboradores', sa.Column('termino', sa.Date(), nullable=True))
    
    # Create ferias table
    op.create_table(
        'ferias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('colaborador_id', sa.Integer(), nullable=False),
        sa.Column('inicio', sa.Date(), nullable=False),
        sa.Column('termino', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ferias_id'), 'ferias', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_ferias_id'), table_name='ferias')
    op.drop_table('ferias')
    op.drop_column('colaboradores', 'termino')
    op.drop_column('colaboradores', 'inicio')