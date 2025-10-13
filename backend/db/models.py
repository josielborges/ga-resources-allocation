from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from datetime import datetime
from .database import Base

# Association table for many-to-many relationship between colaboradores and habilidades
colaborador_habilidade = Table(
    'colaborador_habilidade',
    Base.metadata,
    Column('colaborador_id', Integer, ForeignKey('colaboradores.id'), primary_key=True),
    Column('habilidade_id', Integer, ForeignKey('habilidades.id', ondelete='RESTRICT'), primary_key=True)
)

# Association table for many-to-many relationship between etapas and habilidades
etapa_habilidade = Table(
    'etapa_habilidade',
    Base.metadata,
    Column('etapa_id', Integer, ForeignKey('etapas.id'), primary_key=True),
    Column('habilidade_id', Integer, ForeignKey('habilidades.id', ondelete='RESTRICT'), primary_key=True)
)

# Association table for etapa predecessors
etapa_predecessora = Table(
    'etapa_predecessora',
    Base.metadata,
    Column('etapa_id', Integer, ForeignKey('etapas.id'), primary_key=True),
    Column('predecessora_id', Integer, ForeignKey('etapas.id'), primary_key=True)
)

class Habilidade(Base):
    __tablename__ = "habilidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cargo_id = Column(Integer, ForeignKey("cargos.id", ondelete="RESTRICT"), nullable=False)
    
    cargo = relationship("Cargo")

class Cargo(Base):
    __tablename__ = "cargos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)

class Tribo(Base):
    __tablename__ = "tribos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)

class Squad(Base):
    __tablename__ = "squads"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    tribo_id = Column(Integer, ForeignKey("tribos.id", ondelete="RESTRICT"), nullable=False)
    
    tribo = relationship("Tribo")

class Colaborador(Base):
    __tablename__ = "colaboradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cargo_id = Column(Integer, ForeignKey("cargos.id", ondelete="RESTRICT"))
    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="RESTRICT"), nullable=True)
    transversal = Column(Integer, default=0)
    
    cargo = relationship("Cargo")
    squad = relationship("Squad")
    habilidades = relationship("Habilidade", secondary=colaborador_habilidade, back_populates="colaboradores")
    ausencias = relationship("Ausencia", back_populates="colaborador")

class Ausencia(Base):
    __tablename__ = "ausencias"
    
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"))
    data = Column(Date)
    
    colaborador = relationship("Colaborador", back_populates="ausencias")

class Projeto(Base):
    __tablename__ = "projetos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    color = Column(String)
    termino = Column(Date, nullable=True)
    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="RESTRICT"), nullable=True)
    
    squad = relationship("Squad")
    etapas = relationship("Etapa", back_populates="projeto")

class Etapa(Base):
    __tablename__ = "etapas"
    
    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    nome = Column(String)
    duracao_dias = Column(Integer)
    cargo_necessario_id = Column(Integer, ForeignKey("cargos.id", ondelete="RESTRICT"))
    ordem = Column(Integer, default=0)
    
    projeto = relationship("Projeto", back_populates="etapas")
    cargo_necessario = relationship("Cargo")
    habilidades_necessarias = relationship("Habilidade", secondary=etapa_habilidade, back_populates="etapas")
    predecessoras = relationship(
        "Etapa",
        secondary=etapa_predecessora,
        primaryjoin=id == etapa_predecessora.c.etapa_id,
        secondaryjoin=id == etapa_predecessora.c.predecessora_id,
        back_populates="dependentes"
    )
    dependentes = relationship(
        "Etapa",
        secondary=etapa_predecessora,
        primaryjoin=id == etapa_predecessora.c.predecessora_id,
        secondaryjoin=id == etapa_predecessora.c.etapa_id,
        back_populates="predecessoras"
    )

# Add back_populates to Habilidade
Habilidade.colaboradores = relationship("Colaborador", secondary=colaborador_habilidade, back_populates="habilidades")
Habilidade.etapas = relationship("Etapa", secondary=etapa_habilidade, back_populates="habilidades_necessarias")

class ResultadoSalvo(Base):
    __tablename__ = "resultados_salvos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    algoritmo = Column(String, nullable=False)
    data_execucao = Column(DateTime, default=datetime.utcnow)
    melhor_fitness = Column(Float)
    roadmap_end_date = Column(Date, nullable=True)
    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="SET NULL"), nullable=True)
    tarefas = Column(JSON)
    historico_fitness = Column(JSON)
    penalidades = Column(JSON)
    ocorrencias_penalidades = Column(JSON)
    parametros = Column(JSON)
    
    squad = relationship("Squad")