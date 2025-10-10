"""add_tribos_and_squads

Revision ID: 009
Revises: 008
Create Date: 2025-01-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tribos table
    op.create_table('tribos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tribos_id'), 'tribos', ['id'], unique=False)
    op.create_index(op.f('ix_tribos_nome'), 'tribos', ['nome'], unique=True)
    
    # Create squads table
    op.create_table('squads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('tribo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tribo_id'], ['tribos.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_squads_id'), 'squads', ['id'], unique=False)
    op.create_index(op.f('ix_squads_nome'), 'squads', ['nome'], unique=False)
    
    # Add squad_id to colaboradores
    op.add_column('colaboradores', sa.Column('squad_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_colaboradores_squad_id', 'colaboradores', 'squads', ['squad_id'], ['id'], ondelete='RESTRICT')


def downgrade() -> None:
    op.drop_constraint('fk_colaboradores_squad_id', 'colaboradores', type_='foreignkey')
    op.drop_column('colaboradores', 'squad_id')
    op.drop_index(op.f('ix_squads_nome'), table_name='squads')
    op.drop_index(op.f('ix_squads_id'), table_name='squads')
    op.drop_table('squads')
    op.drop_index(op.f('ix_tribos_nome'), table_name='tribos')
    op.drop_index(op.f('ix_tribos_id'), table_name='tribos')
    op.drop_table('tribos')
