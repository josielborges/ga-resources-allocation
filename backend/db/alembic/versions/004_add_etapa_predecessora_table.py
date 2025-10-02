"""add etapa predecessora table

Revision ID: 004
Revises: 003
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade():
    # Create etapa_predecessora association table
    op.create_table(
        'etapa_predecessora',
        sa.Column('etapa_id', sa.Integer(), nullable=False),
        sa.Column('predecessora_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['etapa_id'], ['etapas.id'], ),
        sa.ForeignKeyConstraint(['predecessora_id'], ['etapas.id'], ),
        sa.PrimaryKeyConstraint('etapa_id', 'predecessora_id')
    )
    
    # Migrate existing data from predecessora_id to association table
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT id, predecessora_id FROM etapas WHERE predecessora_id IS NOT NULL"))
    for row in result:
        connection.execute(
            sa.text("INSERT INTO etapa_predecessora (etapa_id, predecessora_id) VALUES (:etapa_id, :predecessora_id)"),
            {"etapa_id": row[0], "predecessora_id": row[1]}
        )
    
    # Drop old predecessora_id column
    op.drop_column('etapas', 'predecessora_id')

def downgrade():
    # Add back predecessora_id column
    op.add_column('etapas', sa.Column('predecessora_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'etapas', 'etapas', ['predecessora_id'], ['id'])
    
    # Migrate data back (only first predecessor)
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT etapa_id, MIN(predecessora_id) as predecessora_id FROM etapa_predecessora GROUP BY etapa_id"))
    for row in result:
        connection.execute(
            sa.text("UPDATE etapas SET predecessora_id = :predecessora_id WHERE id = :etapa_id"),
            {"etapa_id": row[0], "predecessora_id": row[1]}
        )
    
    # Drop association table
    op.drop_table('etapa_predecessora')