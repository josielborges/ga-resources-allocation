from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

def get_colaboradores(db: Session) -> List[models.Colaborador]:
    return db.query(models.Colaborador).all()

def get_colaborador(db: Session, colaborador_id: int):
    return db.query(models.Colaborador).filter(models.Colaborador.id == colaborador_id).first()

def get_projetos(db: Session) -> List[models.Projeto]:
    return db.query(models.Projeto).all()

def get_projeto(db: Session, projeto_id: int):
    return db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()

def create_projeto(db: Session, projeto: schemas.ProjetoCreate):
    db_projeto = models.Projeto(nome=projeto.nome, color=projeto.color)
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    
    # Criar etapas
    for etapa_data in projeto.etapas:
        db_etapa = models.Etapa(
            projeto_id=db_projeto.id,
            nome=etapa_data.nome,
            duracao_dias=etapa_data.duracao_dias,
            cargo_necessario_id=etapa_data.cargo_necessario_id
        )
        db.add(db_etapa)
        db.commit()
        db.refresh(db_etapa)
        
        # Adicionar habilidades necessárias
        for hab_nome in etapa_data.habilidades_necessarias:
            habilidade = db.query(models.Habilidade).filter(models.Habilidade.nome == hab_nome).first()
            if habilidade:
                db_etapa.habilidades_necessarias.append(habilidade)
        
        db.commit()
    
    return db_projeto

def update_projeto(db: Session, projeto_id: int, projeto: schemas.ProjetoCreate):
    db_projeto = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()
    if not db_projeto:
        return None
    
    db_projeto.nome = projeto.nome
    db_projeto.color = projeto.color
    db.commit()
    
    # Limpar relações many-to-many das etapas existentes
    etapas_existentes = db.query(models.Etapa).filter(models.Etapa.projeto_id == projeto_id).all()
    for etapa in etapas_existentes:
        etapa.habilidades_necessarias.clear()
    db.commit()
    
    # Remover etapas existentes
    db.query(models.Etapa).filter(models.Etapa.projeto_id == projeto_id).delete()
    db.commit()
    
    # Criar novas etapas
    for etapa_data in projeto.etapas:
        db_etapa = models.Etapa(
            projeto_id=projeto_id,
            nome=etapa_data.nome,
            duracao_dias=etapa_data.duracao_dias,
            cargo_necessario_id=etapa_data.cargo_necessario_id
        )
        db.add(db_etapa)
        db.commit()
        db.refresh(db_etapa)
        
        # Adicionar habilidades necessárias
        for hab_nome in etapa_data.habilidades_necessarias:
            habilidade = db.query(models.Habilidade).filter(models.Habilidade.nome == hab_nome).first()
            if habilidade:
                db_etapa.habilidades_necessarias.append(habilidade)
        db.commit()
    
    db.refresh(db_projeto)
    return db_projeto

def delete_projeto(db: Session, projeto_id: int):
    db_projeto = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()
    if db_projeto:
        db.delete(db_projeto)
        db.commit()
        return True
    return False

def get_habilidades(db: Session) -> List[models.Habilidade]:
    return db.query(models.Habilidade).all()

def get_cargos(db: Session) -> List[models.Cargo]:
    return db.query(models.Cargo).all()

def get_etapas(db: Session) -> List[models.Etapa]:
    return db.query(models.Etapa).all()