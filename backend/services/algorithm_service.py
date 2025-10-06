import datetime
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from genetic_algorithm import GeneticAlgorithm, Utils
from algorithm.scheduler import TaskScheduler
from db import crud

class AlgorithmService:
    """Service layer for genetic algorithm operations"""
    
    def __init__(self):
        self.ga = GeneticAlgorithm()
        self.scheduler = TaskScheduler()
    
    def load_data_from_db(self, db: Session) -> Tuple[List[Dict], List[Dict]]:
        """Load and format data from database"""
        colaboradores_db = crud.get_colaboradores(db)
        projetos_db = crud.get_projetos(db)
        
        colaboradores = []
        for colab in colaboradores_db:
            colaboradores.append({
                "id": colab.id,
                "nome": colab.nome,
                "cargo": colab.cargo.nome,
                "habilidades": [h.nome for h in colab.habilidades],
                "ausencias": [a.data.strftime("%Y-%m-%d") for a in colab.ausencias]
            })
        
        projetos = []
        for proj in projetos_db:
            etapas = []
            for etapa in proj.etapas:
                etapas.append({
                    "id": etapa.id,
                    "nome": etapa.nome,
                    "duracao_dias": etapa.duracao_dias,
                    "cargo_necessario": etapa.cargo_necessario.nome,
                    "habilidades_necessarias": [h.nome for h in etapa.habilidades_necessarias]
                })
            
            projetos.append({
                "nome": proj.nome,
                "color": proj.color,
                "etapas": etapas
            })
        
        return colaboradores, projetos
    
    def convert_absences(self, colaboradores: List[Dict], ref_date: datetime.date) -> List[Dict]:
        """Convert absence dates to integer days"""
        for colab in colaboradores:
            ausencias_convertidas = []
            for data_str in colab["ausencias"]:
                dia_int = Utils.date_to_int(data_str, ref_date)
                ausencias_convertidas.append(dia_int)
            colab["ausencias"] = ausencias_convertidas
        return colaboradores
    
    def build_global_tasks(self, projetos: List[Dict]) -> List[Dict]:
        """Build global task list from projects"""
        tarefas_globais = []
        for proj in projetos:
            etapas_ordenadas = sorted(proj["etapas"], key=lambda e: e["id"])
            for etapa in etapas_ordenadas:
                tarefas_globais.append({
                    "projeto": proj["nome"],
                    "task_id": etapa["id"],
                    "nome": etapa["nome"],
                    "duracao_dias": etapa["duracao_dias"],
                    "habilidades_necessarias": set(etapa["habilidades_necessarias"]),
                    "cargo_necessario": etapa["cargo_necessario"],
                })
        return tarefas_globais
    
    def execute_algorithm(self, params: Dict, db: Session) -> Dict:
        """Execute genetic algorithm with given parameters"""
        colaboradores, projetos = self.load_data_from_db(db)
        ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
        
        colaboradores = self.convert_absences(colaboradores, ref_date)
        tarefas_globais = self.build_global_tasks(projetos)
        
        # Run genetic algorithm
        best_solution, best_fitness, fitness_history, penalties, violations = self.ga.run(
            params["tam_pop"], params["n_gen"], params["pc"], params["pm"], 
            tarefas_globais, colaboradores
        )
        
        # Build schedule
        schedule = self.scheduler.build_schedule(
            best_solution, tarefas_globais, colaboradores, ref_date
        )
        
        return {
            "tarefas": schedule,
            "melhor_fitness": best_fitness,
            "historico_fitness": fitness_history,
            "penalidades": penalties,
            "ocorrencias_penalidades": violations
        }