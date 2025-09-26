from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

# Association table for many-to-many relationship between colaboradores and habilidades
colaborador_habilidade = Table(
    'colaborador_habilidade',
    Base.metadata,
    Column('colaborador_id', Integer, ForeignKey('colaboradores.id'), primary_key=True),
    Column('habilidade_id', Integer, ForeignKey('habilidades.id'), primary_key=True)
)

# Association table for many-to-many relationship between etapas and habilidades
etapa_habilidade = Table(
    'etapa_habilidade',
    Base.metadata,
    Column('etapa_id', Integer, ForeignKey('etapas.id'), primary_key=True),
    Column('habilidade_id', Integer, ForeignKey('habilidades.id'), primary_key=True)
)

class Habilidade(Base):
    __tablename__ = "habilidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)

class Cargo(Base):
    __tablename__ = "cargos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)

class Colaborador(Base):
    __tablename__ = "colaboradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cargo_id = Column(Integer, ForeignKey("cargos.id"))
    
    cargo = relationship("Cargo")
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
    
    etapas = relationship("Etapa", back_populates="projeto")

class Etapa(Base):
    __tablename__ = "etapas"
    
    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    nome = Column(String)
    duracao_dias = Column(Integer)
    cargo_necessario_id = Column(Integer, ForeignKey("cargos.id"))
    
    projeto = relationship("Projeto", back_populates="etapas")
    cargo_necessario = relationship("Cargo")
    habilidades_necessarias = relationship("Habilidade", secondary=etapa_habilidade, back_populates="etapas")

# Add back_populates to Habilidade
Habilidade.colaboradores = relationship("Colaborador", secondary=colaborador_habilidade, back_populates="habilidades")
Habilidade.etapas = relationship("Etapa", secondary=etapa_habilidade, back_populates="habilidades_necessarias")