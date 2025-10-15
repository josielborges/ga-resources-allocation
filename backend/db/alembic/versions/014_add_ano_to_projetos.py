"""add ano to projetos

Revision ID: 014
Revises: 013
Create Date: 2025-01-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '014'
down_revision = '013'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('projetos', sa.Column('ano', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('projetos', 'ano')
