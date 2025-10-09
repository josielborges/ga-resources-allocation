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
    db_projeto = models.Projeto(nome=projeto.nome, color=projeto.color, termino=projeto.termino)
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    
    etapas_criadas = []
    for i, etapa_data in enumerate(projeto.etapas):
        db_etapa = models.Etapa(
            projeto_id=db_projeto.id,
            nome=etapa_data.nome,
            duracao_dias=etapa_data.duracao_dias,
            cargo_necessario_id=etapa_data.cargo_necessario_id,
            ordem=getattr(etapa_data, 'ordem', i)
        )
        db.add(db_etapa)
        db.commit()
        db.refresh(db_etapa)
        etapas_criadas.append(db_etapa)
        
        for hab_nome in etapa_data.habilidades_necessarias:
            habilidade = db.query(models.Habilidade).filter(models.Habilidade.nome == hab_nome).first()
            if habilidade:
                db_etapa.habilidades_necessarias.append(habilidade)
        db.commit()
    
    # Handle predecessors for new projects
    for i, etapa_data in enumerate(projeto.etapas):
        predecessoras_ids = getattr(etapa_data, 'predecessoras_ids', [])
        
        # If no predecessors specified but there are previous etapas, set last one as predecessor
        if not predecessoras_ids and i > 0:
            etapas_criadas[i].predecessoras.append(etapas_criadas[i-1])
        else:
            # Handle explicit predecessor references
            for pred_id in predecessoras_ids:
                if isinstance(pred_id, int) and pred_id < len(etapas_criadas):
                    etapas_criadas[i].predecessoras.append(etapas_criadas[pred_id])
    db.commit()
    
    return db_projeto

def update_projeto(db: Session, projeto_id: int, projeto: schemas.ProjetoCreate):
    db_projeto = db.query(models.Projeto).filter(models.Projeto.id == projeto_id).first()
    if not db_projeto:
        return None
    
    db_projeto.nome = projeto.nome
    db_projeto.color = projeto.color
    db_projeto.termino = projeto.termino
    
    etapas_existentes = db.query(models.Etapa).filter(models.Etapa.projeto_id == projeto_id).all()
    etapas_existentes_ordenadas = sorted(etapas_existentes, key=lambda e: e.ordem or 0)
    
    for etapa in etapas_existentes:
        etapa.predecessoras.clear()
    db.commit()
    
    todas_etapas = []
    etapas_utilizadas = set()
    
    for i, etapa_data in enumerate(projeto.etapas):
        original_index = getattr(etapa_data, 'originalIndex', i)
        
        if original_index < len(etapas_existentes_ordenadas):
            db_etapa = etapas_existentes_ordenadas[original_index]
            db_etapa.nome = etapa_data.nome
            db_etapa.duracao_dias = etapa_data.duracao_dias
            db_etapa.cargo_necessario_id = etapa_data.cargo_necessario_id
            db_etapa.ordem = i
            
            db_etapa.habilidades_necessarias.clear()
            for hab_nome in etapa_data.habilidades_necessarias:
                habilidade = db.query(models.Habilidade).filter(models.Habilidade.nome == hab_nome).first()
                if habilidade:
                    db_etapa.habilidades_necessarias.append(habilidade)
            
            etapas_utilizadas.add(original_index)
        else:
            db_etapa = models.Etapa(
                projeto_id=projeto_id,
                nome=etapa_data.nome,
                duracao_dias=etapa_data.duracao_dias,
                cargo_necessario_id=etapa_data.cargo_necessario_id,
                ordem=i
            )
            db.add(db_etapa)
            db.commit()
            db.refresh(db_etapa)
            
            for hab_nome in etapa_data.habilidades_necessarias:
                habilidade = db.query(models.Habilidade).filter(models.Habilidade.nome == hab_nome).first()
                if habilidade:
                    db_etapa.habilidades_necessarias.append(habilidade)
        
        todas_etapas.append(db_etapa)
    
    for i, etapa_existente in enumerate(etapas_existentes_ordenadas):
        if i not in etapas_utilizadas:
            db.delete(etapa_existente)
    db.commit()
    
    db.commit()
    
    for i, etapa_data in enumerate(projeto.etapas):
        db_etapa = todas_etapas[i]
        predecessoras_ids = getattr(etapa_data, 'predecessoras_ids', [])
        
        # If this is a new etapa (no predecessors specified) and there are previous etapas
        if not predecessoras_ids and i > 0:
            # Set the previous etapa as predecessor
            prev_etapa = todas_etapas[i-1]
            if prev_etapa.id != db_etapa.id:
                db_etapa.predecessoras.append(prev_etapa)
        else:
            # Handle explicit predecessor references
            for pred_id in predecessoras_ids:
                pred_etapa = db.query(models.Etapa).filter(models.Etapa.id == pred_id).first()
                if pred_etapa and pred_etapa.id != db_etapa.id:
                    db_etapa.predecessoras.append(pred_etapa)
    
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

def get_cargo(db: Session, cargo_id: int):
    return db.query(models.Cargo).filter(models.Cargo.id == cargo_id).first()

def get_habilidade(db: Session, habilidade_id: int):
    return db.query(models.Habilidade).filter(models.Habilidade.id == habilidade_id).first()
def create_habilidade(db: Session, habilidade: schemas.HabilidadeCreate):
    db_habilidade = models.Habilidade(nome=habilidade.nome, cargo_id=habilidade.cargo_id)
    db.add(db_habilidade)
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade

def update_habilidade(db: Session, habilidade_id: int, habilidade: schemas.HabilidadeCreate):
    db_habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == habilidade_id).first()
    if not db_habilidade:
        return None
    db_habilidade.nome = habilidade.nome
    db_habilidade.cargo_id = habilidade.cargo_id
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade

def get_habilidades_by_cargo(db: Session, cargo_id: int) -> List[models.Habilidade]:
    return db.query(models.Habilidade).filter(models.Habilidade.cargo_id == cargo_id).all()

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


def create_colaborador(db: Session, colaborador: schemas.ColaboradorCreate):
    db_colaborador = models.Colaborador(nome=colaborador.nome, cargo_id=colaborador.cargo_id)
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    
    for hab_id in colaborador.habilidades_ids:
        habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == hab_id).first()
        if habilidade:
            db_colaborador.habilidades.append(habilidade)
    
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
    
    db_colaborador.habilidades.clear()
    
    for hab_id in colaborador.habilidades_ids:
        habilidade = db.query(models.Habilidade).filter(models.Habilidade.id == hab_id).first()
        if habilidade:
            db_colaborador.habilidades.append(habilidade)
    
    db.query(models.Ausencia).filter(models.Ausencia.colaborador_id == colaborador_id).delete()
    
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

def create_resultado_salvo(db: Session, resultado: schemas.ResultadoSalvoCreate):
    db_resultado = models.ResultadoSalvo(**resultado.dict())
    db.add(db_resultado)
    db.commit()
    db.refresh(db_resultado)
    return db_resultado

def get_resultados_salvos(db: Session) -> List[models.ResultadoSalvo]:
    return db.query(models.ResultadoSalvo).order_by(models.ResultadoSalvo.data_execucao.desc()).all()

def get_resultado_salvo(db: Session, resultado_id: int):
    return db.query(models.ResultadoSalvo).filter(models.ResultadoSalvo.id == resultado_id).first()

def delete_resultado_salvo(db: Session, resultado_id: int):
    db_resultado = db.query(models.ResultadoSalvo).filter(models.ResultadoSalvo.id == resultado_id).first()
    if db_resultado:
        db.delete(db_resultado)
        db.commit()
        return True
    return False