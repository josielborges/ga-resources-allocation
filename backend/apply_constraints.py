#!/usr/bin/env python3

import os
import sys
import subprocess

# Add current directory to path
sys.path.append('.')

try:
    from utils.config import settings
    DATABASE_URL = settings.DATABASE_URL
except:
    # Fallback to environment variable or default
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/resource_allocation')

def apply_constraints():
    sql_commands = """
    -- Drop existing constraints
    ALTER TABLE colaboradores DROP CONSTRAINT IF EXISTS colaboradores_cargo_id_fkey;
    ALTER TABLE etapas DROP CONSTRAINT IF EXISTS etapas_cargo_necessario_id_fkey;
    ALTER TABLE colaborador_habilidade DROP CONSTRAINT IF EXISTS colaborador_habilidade_habilidade_id_fkey;
    ALTER TABLE etapa_habilidade DROP CONSTRAINT IF EXISTS etapa_habilidade_habilidade_id_fkey;
    
    -- Add new constraints with RESTRICT
    ALTER TABLE colaboradores ADD CONSTRAINT colaboradores_cargo_id_fkey FOREIGN KEY (cargo_id) REFERENCES cargos(id) ON DELETE RESTRICT;
    ALTER TABLE etapas ADD CONSTRAINT etapas_cargo_necessario_id_fkey FOREIGN KEY (cargo_necessario_id) REFERENCES cargos(id) ON DELETE RESTRICT;
    ALTER TABLE colaborador_habilidade ADD CONSTRAINT colaborador_habilidade_habilidade_id_fkey FOREIGN KEY (habilidade_id) REFERENCES habilidades(id) ON DELETE RESTRICT;
    ALTER TABLE etapa_habilidade ADD CONSTRAINT etapa_habilidade_habilidade_id_fkey FOREIGN KEY (habilidade_id) REFERENCES habilidades(id) ON DELETE RESTRICT;
    """
    
    try:
        print("Aplicando restrições de integridade referencial...")
        
        # Execute using psql command
        env = os.environ.copy()
        env['PGPASSWORD'] = 'postgres'
        
        result = subprocess.run([
            'psql', '-h', 'localhost', '-U', 'postgres', '-d', 'resource_allocation', '-c', sql_commands
        ], env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Restrições aplicadas com sucesso!")
            return True
        else:
            print(f"Erro ao aplicar restrições: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False

if __name__ == "__main__":
    apply_constraints()