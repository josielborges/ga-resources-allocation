from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class HabilidadeBase(BaseModel):
    nome: str
    cargo_id: int

class HabilidadeCreate(HabilidadeBase):
    pass

class CargoBase(BaseModel):
    nome: str

class CargoCreate(CargoBase):
    pass

class Cargo(CargoBase):
    id: int
    
    class Config:
        from_attributes = True

class TriboBase(BaseModel):
    nome: str

class TriboCreate(TriboBase):
    pass

class Tribo(TriboBase):
    id: int
    
    class Config:
        from_attributes = True

class SquadBase(BaseModel):
    nome: str
    tribo_id: int

class SquadCreate(SquadBase):
    pass

class Squad(SquadBase):
    id: int
    tribo: Tribo
    
    class Config:
        from_attributes = True

class Habilidade(HabilidadeBase):
    id: int
    cargo: Cargo
    
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

class FeriasBase(BaseModel):
    inicio: date
    termino: date

class FeriasCreate(FeriasBase):
    colaborador_id: int

class Ferias(FeriasBase):
    id: int
    colaborador_id: int
    
    class Config:
        from_attributes = True

class ColaboradorBase(BaseModel):
    nome: str
    inicio: Optional[date] = None
    termino: Optional[date] = None

class ColaboradorCreate(ColaboradorBase):
    cargo_id: int
    squad_id: Optional[int] = None
    transversal: bool = False
    ativo: bool = True
    habilidades_ids: List[int] = []
    ausencias: List[dict] = []
    ferias: List[dict] = []

class Colaborador(ColaboradorBase):
    id: int
    cargo: Cargo
    squad: Optional[Squad] = None
    transversal: bool = False
    ativo: bool = True
    habilidades: List[Habilidade] = []
    ausencias: List[Ausencia] = []
    ferias: List[Ferias] = []
    
    class Config:
        from_attributes = True

class EtapaBase(BaseModel):
    nome: str
    duracao_dias: int

class EtapaCreate(EtapaBase):
    cargo_necessario_id: int
    habilidades_necessarias: List[str] = []
    ordem: int = 0
    predecessoras_ids: List[int] = []
    originalIndex: Optional[int] = None

class Etapa(EtapaBase):
    id: int
    projeto_id: int
    cargo_necessario: Cargo
    habilidades_necessarias: List[Habilidade] = []
    ordem: int = 0
    predecessoras: List['Etapa'] = []
    
    class Config:
        from_attributes = True

class ProjetoBase(BaseModel):
    nome: str
    color: str
    inicio: Optional[date] = None
    termino: Optional[date] = None
    squad_id: Optional[int] = None
    ano: Optional[int] = None

class ProjetoCreate(ProjetoBase):
    etapas: List[EtapaCreate] = []

class ProjetoUpdate(ProjetoBase):
    etapas: List[EtapaCreate] = []

class Projeto(ProjetoBase):
    id: int
    squad: Optional[Squad] = None
    etapas: List[Etapa] = []
    
    class Config:
        from_attributes = True

class ResultadoSalvoBase(BaseModel):
    nome: str
    algoritmo: str
    melhor_fitness: float
    roadmap_end_date: Optional[date] = None
    squad_id: Optional[int] = None
    ano: Optional[int] = None
    tarefas: List[Dict[str, Any]]
    historico_fitness: List[float]
    penalidades: Dict[str, Any]
    ocorrencias_penalidades: Dict[str, Any]
    parametros: Dict[str, Any]

class ResultadoSalvoCreate(ResultadoSalvoBase):
    pass

class ResultadoSalvo(ResultadoSalvoBase):
    id: int
    data_execucao: datetime
    squad: Optional[Squad] = None
    
    class Config:
        from_attributes = True

class PeriodoRoadmapBase(BaseModel):
    ano: int
    inicio: date
    termino: date

class PeriodoRoadmapCreate(PeriodoRoadmapBase):
    pass

class PeriodoRoadmap(PeriodoRoadmapBase):
    id: int
    
    class Config:
        from_attributes = True