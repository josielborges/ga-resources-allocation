"""create periodos_roadmaps

Revision ID: 015
Revises: 014
Create Date: 2025-01-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'periodos_roadmaps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ano', sa.Integer(), nullable=False),
        sa.Column('inicio', sa.Date(), nullable=False),
        sa.Column('termino', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_periodos_roadmaps_ano', 'periodos_roadmaps', ['ano'], unique=True)

def downgrade():
    op.drop_index('ix_periodos_roadmaps_ano')
    op.drop_table('periodos_roadmaps')
