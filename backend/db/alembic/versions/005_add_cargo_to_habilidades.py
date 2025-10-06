"""add cargo to habilidades

Revision ID: 005_add_cargo_to_habilidades
Revises: 004_add_etapa_predecessora_table
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Add cargo_id to habilidades
    op.add_column('habilidades', sa.Column('cargo_id', sa.Integer(), nullable=True))
    
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT COUNT(*) FROM cargos")).fetchone()
    if result[0] == 0:
        connection.execute(sa.text("INSERT INTO cargos (nome) VALUES ('Desenvolvedor')"))
        connection.commit()
    
    first_cargo = connection.execute(sa.text("SELECT id FROM cargos LIMIT 1")).fetchone()
    if first_cargo:
        connection.execute(sa.text("UPDATE habilidades SET cargo_id = :cargo_id WHERE cargo_id IS NULL"), {'cargo_id': first_cargo[0]})
        connection.commit()
    
    op.alter_column('habilidades', 'cargo_id', nullable=False)
    op.create_foreign_key('fk_habilidades_cargo', 'habilidades', 'cargos', ['cargo_id'], ['id'], ondelete='RESTRICT')


def downgrade():
    # Remove foreign key and column
    op.drop_constraint('fk_habilidades_cargo', 'habilidades', type_='foreignkey')
    op.drop_column('habilidades', 'cargo_id')