from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class HabilidadeBase(BaseModel):
    nome: str

class HabilidadeCreate(HabilidadeBase):
    pass

class Habilidade(HabilidadeBase):
    id: int
    
    class Config:
        from_attributes = True

class CargoBase(BaseModel):
    nome: str

class CargoCreate(CargoBase):
    pass

class Cargo(CargoBase):
    id: int
    
    class Config:
        from_attributes = True

class AusenciaBase(BaseModel):
    data: date

class AusenciaCreate(AusenciaBase):
    colaborador_id: int

class Ausencia(AusenciaBase):
    id: int
    colaborador_id: int
    
    class Config:
        from_attributes = True

class ColaboradorBase(BaseModel):
    nome: str

class ColaboradorCreate(ColaboradorBase):
    cargo_id: int
    habilidades: List[str] = []
    ausencias: List[date] = []

class Colaborador(ColaboradorBase):
    id: int
    cargo: Cargo
    habilidades: List[Habilidade] = []
    ausencias: List[Ausencia] = []
    
    class Config:
        from_attributes = True

class EtapaBase(BaseModel):
    nome: str
    duracao_dias: int

class EtapaCreate(EtapaBase):
    projeto_id: int
    cargo_necessario_id: int
    habilidades_necessarias: List[str] = []

class Etapa(EtapaBase):
    id: int
    projeto_id: int
    cargo_necessario: Cargo
    habilidades_necessarias: List[Habilidade] = []
    
    class Config:
        from_attributes = True

class ProjetoBase(BaseModel):
    nome: str
    color: str

class ProjetoCreate(ProjetoBase):
    etapas: List[EtapaCreate] = []

class Projeto(ProjetoBase):
    id: int
    etapas: List[Etapa] = []
    
    class Config:
        from_attributes = True