import datetime
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ant_colony_optimization import AntColonyOptimization
from algorithm.scheduler import TaskScheduler
from db import crud

class ACOService:
    """Service layer for Ant Colony Optimization operations"""
    
    def __init__(self):
        self.aco = AntColonyOptimization()
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
                    "habilidades_necessarias": [h.nome for h in etapa.habilidades_necessarias],
                    "predecessoras": [p.id for p in etapa.predecessoras]
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
                ano, mes, dia = map(int, data_str.split("-"))
                d = datetime.date(ano, mes, dia)
                delta = d - ref_date
                ausencias_convertidas.append(delta.days)
            colab["ausencias"] = ausencias_convertidas
        return colaboradores
    
    def build_global_tasks(self, projetos: List[Dict]) -> List[Dict]:
        """Build task list with ACO-optimized ordering"""
        # Calculate resource scarcity for better task ordering
        skill_frequency = {}
        position_frequency = {}
        
        for proj in projetos:
            for etapa in proj["etapas"]:
                for skill in etapa["habilidades_necessarias"]:
                    skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
                
                pos = etapa["cargo_necessario"]
                position_frequency[pos] = position_frequency.get(pos, 0) + 1
        
        # Build tasks with dependency-aware ordering
        all_tasks = []
        
        for proj in projetos:
            task_map = {etapa["id"]: etapa for etapa in proj["etapas"]}
            in_degree = {etapa["id"]: len(etapa["predecessoras"]) for etapa in proj["etapas"]}
            queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
            
            while queue:
                # Sort by resource scarcity (rarest resources first)
                queue.sort(key=lambda tid: (
                    sum(skill_frequency.get(skill, 0) for skill in task_map[tid]["habilidades_necessarias"]) +
                    position_frequency.get(task_map[tid]["cargo_necessario"], 0)
                ))
                
                current_id = queue.pop(0)
                etapa = task_map[current_id]
                
                all_tasks.append({
                    "projeto": proj["nome"],
                    "task_id": etapa["id"],
                    "nome": etapa["nome"],
                    "duracao_dias": etapa["duracao_dias"],
                    "habilidades_necessarias": set(etapa["habilidades_necessarias"]),
                    "cargo_necessario": etapa["cargo_necessario"],
                    "predecessoras": etapa["predecessoras"]
                })
                
                # Update dependencies
                for etapa_check in proj["etapas"]:
                    if current_id in etapa_check["predecessoras"]:
                        in_degree[etapa_check["id"]] -= 1
                        if in_degree[etapa_check["id"]] == 0:
                            queue.append(etapa_check["id"])
        
        return all_tasks
    
    def execute_algorithm(self, params: Dict, db: Session) -> Dict:
        """Execute ACO algorithm with given parameters"""
        colaboradores, projetos = self.load_data_from_db(db)
        ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
        
        colaboradores = self.convert_absences(colaboradores, ref_date)
        tarefas_globais = self.build_global_tasks(projetos)
        
        # Create ACO with custom parameters
        alpha = params.get("alpha", 1.0)
        beta = params.get("beta", 2.0)
        rho = params.get("rho", 0.5)
        
        self.aco = AntColonyOptimization(alpha=alpha, beta=beta, rho=rho)
        
        # Map parameters
        num_ants = params.get("tam_pop", 50)
        max_iterations = params.get("n_gen", 100)
        
        # Run ACO algorithm
        best_solution, best_fitness, fitness_history, penalties, violations = self.aco.run(
            num_ants, max_iterations, tarefas_globais, colaboradores
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