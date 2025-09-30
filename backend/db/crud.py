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
    for i, etapa_data in enumerate(projeto.etapas):
        db_etapa = models.Etapa(
            projeto_id=db_projeto.id,
            nome=etapa_data.nome,
            duracao_dias=etapa_data.duracao_dias,
            cargo_necessario_id=etapa_data.cargo_necessario_id,
            ordem=getattr(etapa_data, 'ordem', i),
            predecessora_id=getattr(etapa_data, 'predecessora_id', None)
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
    for i, etapa_data in enumerate(projeto.etapas):
        db_etapa = models.Etapa(
            projeto_id=projeto_id,
            nome=etapa_data.nome,
            duracao_dias=etapa_data.duracao_dias,
            cargo_necessario_id=etapa_data.cargo_necessario_id,
            ordem=getattr(etapa_data, 'ordem', i),
            predecessora_id=getattr(etapa_data, 'predecessora_id', None)
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

# CRUD Habilidades
def create_habilidade(db: Session, habilidade: schemas.HabilidadeCreate):
    db_habilidade = models.Habilidade(nome=habilidade.nome)
    db.add(db_habilidade)
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade

def update_habilidade(db: Session, habilidade_id: int, habilidade: schemas.HabilidadeCreate):
    db_habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == habilidade_id).first()
    if not db_habilidade:
        return None
    db_habilidade.nome = habilidade.nome
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade

def delete_habilidade(db: Session, habilidade_id: int):
    from sqlalchemy.exc import IntegrityError
    db_habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == habilidade_id).first()
    if db_habilidade:
        try:
            db.delete(db_habilidade)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return "in_use"
    return False

# CRUD Cargos
def create_cargo(db: Session, cargo: schemas.CargoCreate):
    db_cargo = models.Cargo(nome=cargo.nome)
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

def update_cargo(db: Session, cargo_id: int, cargo: schemas.CargoCreate):
    db_cargo = db.query(models.Cargo).filter(models.Cargo.id == cargo_id).first()
    if not db_cargo:
        return None
    db_cargo.nome = cargo.nome
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

def delete_cargo(db: Session, cargo_id: int):
    from sqlalchemy.exc import IntegrityError
    db_cargo = db.query(models.Cargo).filter(models.Cargo.id == cargo_id).first()
    if db_cargo:
        try:
            db.delete(db_cargo)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return "in_use"
    return False

# CRUD Colaboradores
def create_colaborador(db: Session, colaborador: schemas.ColaboradorCreate):
    db_colaborador = models.Colaborador(nome=colaborador.nome, cargo_id=colaborador.cargo_id)
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    
    # Adicionar habilidades
    for hab_id in colaborador.habilidades_ids:
        habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == hab_id).first()
        if habilidade:
            db_colaborador.habilidades.append(habilidade)
    
    # Adicionar ausências
    for ausencia_data in colaborador.ausencias:
        db_ausencia = models.Ausencia(data=ausencia_data['data'], colaborador_id=db_colaborador.id)
        db.add(db_ausencia)
    
    db.commit()
    db.refresh(db_colaborador)
    return db_colaborador

def update_colaborador(db: Session, colaborador_id: int, colaborador: schemas.ColaboradorCreate):
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == colaborador_id).first()
    if not db_colaborador:
        return None
    
    db_colaborador.nome = colaborador.nome
    db_colaborador.cargo_id = colaborador.cargo_id
    
    # Limpar habilidades existentes
    db_colaborador.habilidades.clear()
    
    # Adicionar novas habilidades
    for hab_id in colaborador.habilidades_ids:
        habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == hab_id).first()
        if habilidade:
            db_colaborador.habilidades.append(habilidade)
    
    # Limpar ausências existentes
    db.query(models.Ausencia).filter(models.Ausencia.colaborador_id == colaborador_id).delete()
    
    # Adicionar novas ausências
    for ausencia_data in colaborador.ausencias:
        db_ausencia = models.Ausencia(data=ausencia_data['data'], colaborador_id=colaborador_id)
        db.add(db_ausencia)
    
    db.commit()
    db.refresh(db_colaborador)
    return db_colaborador

def delete_colaborador(db: Session, colaborador_id: int):
    db_colaborador = db.query(models.Colaborador).filter(models.Colaborador.id == colaborador_id).first()
    if db_colaborador:
        db.delete(db_colaborador)
        db.commit()
        return True
    return False