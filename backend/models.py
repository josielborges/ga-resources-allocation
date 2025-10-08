from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

class Colaborador(BaseModel):
    id: int
    nome: str
    habilidades: List[str]
    cargo: str
    ausencias: List[str]

class Etapa(BaseModel):
    id: int
    nome: str
    duracao_dias: int
    habilidades_necessarias: List[str]
    cargo_necessario: str

class Projeto(BaseModel):
    nome: str
    color: str
    etapas: List[Etapa]

class SimulatedMember(BaseModel):
    nome: str
    cargo_id: int
    habilidade_names: List[str]

class AlgoritmoParams(BaseModel):
    tam_pop: int = 20
    n_gen: int = 100
    pc: float = 0.7
    pm: float = 0.3
    ref_date: str = "2025-01-01"
    projeto_ids: Optional[List[int]] = None
    colaborador_ids: Optional[List[int]] = None
    simulated_members: Optional[List[SimulatedMember]] = None

class ResultadoTarefa(BaseModel):
    projeto: str
    nome_tarefa: str
    inicio_dias: int
    data_inicio: str
    fim_dias: int
    data_fim: str
    colaborador: str
    duracao_dias: int

class ResultadoAlgoritmo(BaseModel):
    tarefas: List[ResultadoTarefa]
    melhor_fitness: float
    historico_fitness: List[float]
    penalidades: Dict[str, float]
    ocorrencias_penalidades: Dict[str, List[Dict]]