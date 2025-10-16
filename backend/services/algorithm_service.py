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
                dia_int = Utils.date_to_int(data_str, ref_date)
                ausencias_convertidas.append(dia_int)
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
                print(f"DEBUG: {colab['nome']} vacation: {inicio} to {termino} = days {inicio_dias} to {termino_dias} (ref={ref_date})")
            colab["ferias"] = ferias_convertidas
        
        return colaboradores
    
    def build_global_tasks(self, projetos: List[Dict]) -> List[Dict]:
        """Build optimized task list prioritizing bottleneck resources"""
        # Identify bottleneck skills and positions
        skill_demand = {}
        position_demand = {}
        
        for proj in projetos:
            for etapa in proj["etapas"]:
                # Count skill demand
                for skill in etapa["habilidades_necessarias"]:
                    skill_demand[skill] = skill_demand.get(skill, 0) + etapa["duracao_dias"]
                
                # Count position demand
                pos = etapa["cargo_necessario"]
                position_demand[pos] = position_demand.get(pos, 0) + etapa["duracao_dias"]
        
        # Sort projects by bottleneck priority (shortest bottleneck tasks first)
        def project_priority(proj):
            bottleneck_duration = 0
            for etapa in proj["etapas"]:
                if len(etapa["predecessoras"]) == 0:  # Initial tasks
                    # Check if this is a bottleneck skill/position
                    is_bottleneck = (
                        any(skill_demand.get(skill, 0) > 50 for skill in etapa["habilidades_necessarias"]) or
                        position_demand.get(etapa["cargo_necessario"], 0) > 50
                    )
                    if is_bottleneck:
                        bottleneck_duration += etapa["duracao_dias"]
            return bottleneck_duration
        
        # Sort projects by bottleneck duration (ascending)
        sorted_projects = sorted(projetos, key=project_priority)
        
        # Build tasks with intelligent interleaving
        all_project_tasks = []
        for proj in sorted_projects:
            task_map = {etapa["id"]: etapa for etapa in proj["etapas"]}
            in_degree = {etapa["id"]: len(etapa["predecessoras"]) for etapa in proj["etapas"]}
            queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
            sorted_tasks = []
            
            while queue:
                current_id = queue.pop(0)
                sorted_tasks.append(current_id)
                
                for etapa in proj["etapas"]:
                    if current_id in etapa["predecessoras"]:
                        in_degree[etapa["id"]] -= 1
                        if in_degree[etapa["id"]] == 0:
                            queue.append(etapa["id"])
            
            project_tasks = []
            for task_id in sorted_tasks:
                etapa = task_map[task_id]
                project_tasks.append({
                    "projeto": proj["nome"],
                    "task_id": etapa["id"],
                    "nome": etapa["nome"],
                    "duracao_dias": etapa["duracao_dias"],
                    "habilidades_necessarias": set(etapa["habilidades_necessarias"]),
                    "cargo_necessario": etapa["cargo_necessario"],
                    "predecessoras": etapa["predecessoras"]
                })
            all_project_tasks.append(project_tasks)
        
        # Intelligent task interleaving
        tarefas_globais = []
        max_tasks = max(len(tasks) for tasks in all_project_tasks) if all_project_tasks else 0
        
        for level in range(max_tasks):
            # Group tasks by resource requirements at this level
            level_tasks = []
            for project_tasks in all_project_tasks:
                if level < len(project_tasks):
                    level_tasks.append(project_tasks[level])
            
            # Sort by resource scarcity (bottleneck tasks first)
            level_tasks.sort(key=lambda t: (
                sum(skill_demand.get(skill, 0) for skill in t["habilidades_necessarias"]) +
                position_demand.get(t["cargo_necessario"], 0)
            ), reverse=True)
            
            tarefas_globais.extend(level_tasks)
        
        return tarefas_globais
    
    def execute_algorithm(self, params: Dict, db: Session) -> Dict:
        """Execute genetic algorithm with given parameters"""
        colaboradores, projetos = self.load_data_from_db(
            db, 
            colaborador_ids=params.get("colaborador_ids"),
            projeto_ids=params.get("projeto_ids")
        )
        
        # Add simulated members
        simulated_members = params.get("simulated_members", [])
        for sim_member in simulated_members:
            cargo = crud.get_cargo(db, sim_member["cargo_id"])
            colaboradores.append({
                "id": f"sim_{sim_member['nome']}",
                "nome": sim_member["nome"],
                "cargo": cargo.nome if cargo else "Unknown",
                "habilidades": sim_member.get("habilidade_names", []),
                "ausencias": []
            })
        
        ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
        
        colaboradores = self.convert_absences(colaboradores, ref_date)
        tarefas_globais = self.build_global_tasks(projetos)
        
        # Build project deadlines dict
        project_deadlines = {}
        for proj in projetos:
            if proj.get("termino"):
                delta = proj["termino"] - ref_date
                project_deadlines[proj["nome"]] = delta.days
        
        # Run genetic algorithm
        best_solution, best_fitness, fitness_history, penalties, violations = self.ga.run(
            params["tam_pop"], params["n_gen"], params["pc"], params["pm"], 
            tarefas_globais, colaboradores, project_deadlines
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