from sqlalchemy.orm import Session
from . import models
from typing import List

def get_colaboradores(db: Session) -> List[models.Colaborador]:
    return db.query(models.Colaborador).all()

def get_colaborador(db: Session, colaborador_id: int):
    return db.query(models.Colaborador).filter(models.Colaborador.id == colaborador_id).first()

def get_projetos(db: Session) -> List[models.Projeto]:
    return db.query(models.Projeto).all()

def get_projeto(db: Session, projeto_id: int):
    return db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()

def get_habilidades(db: Session) -> List[models.Habilidade]:
    return db.query(models.Habilidade).all()

def get_cargos(db: Session) -> List[models.Cargo]:
    return db.query(models.Cargo).all()

def get_etapas(db: Session) -> List[models.Etapa]:
    return db.query(models.Etapa).all()