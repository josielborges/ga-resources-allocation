import json
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, engine
from db.models import Base, Colaborador, Projeto, Etapa, Habilidade, Cargo, Ausencia

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Ausencia).delete()
        db.query(Etapa).delete()
        db.query(Colaborador).delete()
        db.query(Projeto).delete()
        db.query(Habilidade).delete()
        db.query(Cargo).delete()
        db.commit()
        
        # Load JSON data
        with open('data/colaborators.json', 'r', encoding='utf-8') as f:
            colaboradores_data = json.load(f)
        
        with open('data/projects.json', 'r', encoding='utf-8') as f:
            projetos_data = json.load(f)
        
        # Create habilidades
        habilidades_set = set()
        for colaborador in colaboradores_data:
            habilidades_set.update(colaborador['habilidades'])
        
        for projeto in projetos_data:
            for etapa in projeto['etapas']:
                habilidades_set.update(etapa['habilidades_necessarias'])
        
        habilidades_map = {}
        for habilidade_nome in habilidades_set:
            habilidade = Habilidade(nome=habilidade_nome)
            db.add(habilidade)
            db.flush()
            habilidades_map[habilidade_nome] = habilidade
        
        # Create cargos
        cargos_set = set()
        for colaborador in colaboradores_data:
            cargos_set.add(colaborador['cargo'])
        
        for projeto in projetos_data:
            for etapa in projeto['etapas']:
                cargos_set.add(etapa['cargo_necessario'])
        
        cargos_map = {}
        for cargo_nome in cargos_set:
            cargo = Cargo(nome=cargo_nome)
            db.add(cargo)
            db.flush()
            cargos_map[cargo_nome] = cargo
        
        # Create colaboradores
        for colaborador_data in colaboradores_data:
            colaborador = Colaborador(
                id=colaborador_data['id'],
                nome=colaborador_data['nome'],
                cargo=cargos_map[colaborador_data['cargo']]
            )
            
            # Add habilidades
            for habilidade_nome in colaborador_data['habilidades']:
                colaborador.habilidades.append(habilidades_map[habilidade_nome])
            
            db.add(colaborador)
            db.flush()
            
            # Add ausencias
            for ausencia_str in colaborador_data['ausencias']:
                ausencia_date = datetime.strptime(ausencia_str, '%Y-%m-%d').date()
                ausencia = Ausencia(colaborador=colaborador, data=ausencia_date)
                db.add(ausencia)
        
        # Create projetos and etapas
        for projeto_data in projetos_data:
            projeto = Projeto(
                nome=projeto_data['nome'],
                color=projeto_data['color']
            )
            db.add(projeto)
            db.flush()
            
            for etapa_data in projeto_data['etapas']:
                etapa = Etapa(
                    nome=etapa_data['nome'],
                    duracao_dias=etapa_data['duracao_dias'],
                    projeto=projeto,
                    cargo_necessario=cargos_map[etapa_data['cargo_necessario']]
                )
                
                # Add habilidades necessarias
                for habilidade_nome in etapa_data['habilidades_necessarias']:
                    etapa.habilidades_necessarias.append(habilidades_map[habilidade_nome])
                
                db.add(etapa)
        
        db.commit()
        print("Data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_data()