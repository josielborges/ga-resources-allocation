"""add ano to resultados_salvos

Revision ID: 016
Revises: 015
Create Date: 2025-01-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('resultados_salvos', sa.Column('ano', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('resultados_salvos', 'ano')
