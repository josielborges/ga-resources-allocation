import datetime
import asyncio
from typing import List, Dict, Tuple, AsyncGenerator
from sqlalchemy.orm import Session
from ant_colony_optimization import AntColonyOptimization
from algorithm.scheduler import TaskScheduler
from db import crud

class ACOService:
    """Service layer for Ant Colony Optimization operations"""
    
    def __init__(self):
        self.aco = AntColonyOptimization()
        self.scheduler = TaskScheduler()
    
    def load_data_from_db(self, db: Session, colaborador_ids: List[int] = None, projeto_ids: List[int] = None) -> Tuple[List[Dict], List[Dict]]:
        """Load and format data from database with optional filtering"""
        colaboradores_db = crud.get_colaboradores(db)
        projetos_db = crud.get_projetos(db)
        
        # Filter if IDs provided
        if colaborador_ids:
            colaboradores_db = [c for c in colaboradores_db if c.id in colaborador_ids]
        if projeto_ids:
            projetos_db = [p for p in projetos_db if p.id in projeto_ids]
        
        colaboradores = []
        for colab in colaboradores_db:
            colaboradores.append({
                "id": colab.id,
                "nome": colab.nome,
                "cargo": colab.cargo.nome,
                "habilidades": [h.nome for h in colab.habilidades],
                "ausencias": [a.data.strftime("%Y-%m-%d") for a in colab.ausencias],
                "inicio": colab.inicio,
                "termino": colab.termino,
                "ferias": [(f.inicio, f.termino) for f in colab.ferias]
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
                "termino": proj.termino,
                "etapas": etapas
            })
        
        return colaboradores, projetos
    
    def convert_absences(self, colaboradores: List[Dict], ref_date: datetime.date) -> List[Dict]:
        """Convert absence dates, work period, and vacation dates to integer days"""
        for colab in colaboradores:
            ausencias_convertidas = []
            for data_str in colab["ausencias"]:
                ano, mes, dia = map(int, data_str.split("-"))
                d = datetime.date(ano, mes, dia)
                delta = d - ref_date
                ausencias_convertidas.append(delta.days)
            colab["ausencias"] = ausencias_convertidas
            
            # Convert work period
            if colab.get("inicio"):
                colab["inicio"] = (colab["inicio"] - ref_date).days
            if colab.get("termino"):
                colab["termino"] = (colab["termino"] - ref_date).days
            
            # Convert vacation periods
            ferias_convertidas = []
            for inicio, termino in colab.get("ferias", []):
                inicio_dias = (inicio - ref_date).days
                termino_dias = (termino - ref_date).days
                ferias_convertidas.append((inicio_dias, termino_dias))
            colab["ferias"] = ferias_convertidas
        
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
    
    async def execute_algorithm_stream(self, params: Dict, db: Session) -> AsyncGenerator[Dict, None]:
        colaboradores, projetos = self.load_data_from_db(
            db,
            colaborador_ids=params.get("colaborador_ids"),
            projeto_ids=params.get("projeto_ids")
        )
        
        ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
        colaboradores = self.convert_absences(colaboradores, ref_date)
        
        simulated_members = params.get("simulated_members", [])
        for sim_member in simulated_members:
            cargo = crud.get_cargo(db, sim_member["cargo_id"])
            inicio = None
            termino = None
            if sim_member.get("inicio"):
                inicio_date = datetime.datetime.strptime(sim_member["inicio"], "%Y-%m-%d").date() if isinstance(sim_member["inicio"], str) else sim_member["inicio"]
                inicio = (inicio_date - ref_date).days
            if sim_member.get("termino"):
                termino_date = datetime.datetime.strptime(sim_member["termino"], "%Y-%m-%d").date() if isinstance(sim_member["termino"], str) else sim_member["termino"]
                termino = (termino_date - ref_date).days
            
            colaboradores.append({
                "id": f"sim_{sim_member['nome']}",
                "nome": sim_member["nome"],
                "cargo": cargo.nome if cargo else "Unknown",
                "habilidades": sim_member.get("habilidade_names", []),
                "ausencias": [],
                "inicio": inicio,
                "termino": termino,
                "ferias": []
            })
        tarefas_globais = self.build_global_tasks(projetos)
        
        project_deadlines = {}
        for proj in projetos:
            if proj.get("termino"):
                delta = proj["termino"] - ref_date
                project_deadlines[proj["nome"]] = delta.days
        
        alpha = params.get("alpha", 0.5)
        beta = params.get("beta", 3.0)
        rho = params.get("rho", 0.05)
        q0 = params.get("q0", 0.5)
        self.aco = AntColonyOptimization(alpha=alpha, beta=beta, rho=rho, q0=q0)
        
        num_ants = params.get("tam_pop", 50)
        max_iterations = params.get("n_gen", 100)
        
        async for progress in self.aco.run_with_progress(
            num_ants, max_iterations, tarefas_globais, colaboradores, project_deadlines
        ):
            yield progress
    
    def execute_algorithm(self, params: Dict, db: Session) -> Dict:
        """Execute ACO algorithm with given parameters"""
        colaboradores, projetos = self.load_data_from_db(
            db,
            colaborador_ids=params.get("colaborador_ids"),
            projeto_ids=params.get("projeto_ids")
        )
        
        ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
        colaboradores = self.convert_absences(colaboradores, ref_date)
        
        # Add simulated members AFTER converting absences
        simulated_members = params.get("simulated_members", [])
        for sim_member in simulated_members:
            cargo = crud.get_cargo(db, sim_member["cargo_id"])
            inicio = None
            termino = None
            if sim_member.get("inicio"):
                inicio_date = datetime.datetime.strptime(sim_member["inicio"], "%Y-%m-%d").date() if isinstance(sim_member["inicio"], str) else sim_member["inicio"]
                inicio = (inicio_date - ref_date).days
            if sim_member.get("termino"):
                termino_date = datetime.datetime.strptime(sim_member["termino"], "%Y-%m-%d").date() if isinstance(sim_member["termino"], str) else sim_member["termino"]
                termino = (termino_date - ref_date).days
            
            colaboradores.append({
                "id": f"sim_{sim_member['nome']}",
                "nome": sim_member["nome"],
                "cargo": cargo.nome if cargo else "Unknown",
                "habilidades": sim_member.get("habilidade_names", []),
                "ausencias": [],
                "inicio": inicio,
                "termino": termino,
                "ferias": []
            })
        tarefas_globais = self.build_global_tasks(projetos)
        
        # Build project deadlines dict
        project_deadlines = {}
        for proj in projetos:
            if proj.get("termino"):
                delta = proj["termino"] - ref_date
                project_deadlines[proj["nome"]] = delta.days
        
        # Create ACO with custom parameters
        alpha = params.get("alpha", 0.5)
        beta = params.get("beta", 3.0)
        rho = params.get("rho", 0.05)
        q0 = params.get("q0", 0.5)
        
        self.aco = AntColonyOptimization(alpha=alpha, beta=beta, rho=rho, q0=q0)
        
        # Map parameters
        num_ants = params.get("tam_pop", 50)
        max_iterations = params.get("n_gen", 100)
        
        # Run ACO algorithm
        best_solution, best_fitness, fitness_history, penalties, violations = self.aco.run(
            num_ants, max_iterations, tarefas_globais, colaboradores, project_deadlines
        )
        
        # Build schedule
        schedule = self.scheduler.build_schedule(
            best_solution, tarefas_globais, colaboradores, ref_date
        )
        
        # Validate actual schedule with real day numbers
        from algorithm.constraints import ConstraintValidator
        validator = ConstraintValidator()
        
        final_penalties = {
            "habilidades_incorretas": 0,
            "cargo_incorreto": 0,
            "ausencias": 0,
            "sobreposicoes_colaborador": 0,
            "resource_idle_time": 0,
            "gaps_projeto": 0,
            "makespan": 0,
            "deadline_violation": 0,
            "work_period_violation": 0,
            "vacation_conflict": 0
        }
        final_violations = {
            "habilidades_incorretas": [],
            "cargo_incorreto": [],
            "ausencias": [],
            "sobreposicoes_colaborador": [],
            "resource_idle_time": [],
            "gaps_projeto": [],
            "deadline_violation": [],
            "work_period_violation": [],
            "vacation_conflict": []
        }
        
        for task_schedule in schedule:
            task = next((t for t in tarefas_globais if t["projeto"] == task_schedule["projeto"] and t["nome"] == task_schedule["nome_tarefa"]), None)
            if not task:
                continue
            
            collaborator = next(c for c in colaboradores if c["nome"] == task_schedule["colaborador"])
            start_day = task_schedule["inicio_dias"]
            end_day = task_schedule["fim_dias"] + 1
            
            skill_violations = validator.validate_skills(task, collaborator)
            for v in skill_violations:
                final_penalties["habilidades_incorretas"] += v.penalty
                final_violations["habilidades_incorretas"].append(v.details)
            
            position_violations = validator.validate_position(task, collaborator)
            for v in position_violations:
                final_penalties["cargo_incorreto"] += v.penalty
                final_violations["cargo_incorreto"].append(v.details)
            
            availability_violations = validator.validate_availability(collaborator, start_day, end_day, task)
            for v in availability_violations:
                if v.type == "vacation_conflict":
                    final_penalties["vacation_conflict"] += v.penalty
                    final_violations["vacation_conflict"].append(v.details)
                elif v.type == "work_period_violation":
                    final_penalties["work_period_violation"] += v.penalty
                    final_violations["work_period_violation"].append(v.details)
                elif v.type == "absence_conflict":
                    final_penalties["ausencias"] += v.penalty
                    final_violations["ausencias"].append(v.details)
        
        return {
            "tarefas": schedule,
            "melhor_fitness": best_fitness,
            "historico_fitness": fitness_history,
            "penalidades": final_penalties,
            "ocorrencias_penalidades": final_violations
        }
