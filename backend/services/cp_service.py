import datetime
import asyncio
from typing import List, Dict, AsyncGenerator
from sqlalchemy.orm import Session
from constraint_programming import ConstraintProgramming
from algorithm.constraints import ConstraintValidator
from utils.result_saver import ResultSaver
from db import crud

class CPService:
    def __init__(self):
        self.cp = ConstraintProgramming(
            makespan_weight=200,
            time_limit_seconds=600,
            load_balancing_weight=50,
            parallelization_bonus=100
        )
        self.result_saver = ResultSaver()
    
    def load_data_from_db(self, db: Session):
        """Load collaborators and projects from database"""
        colaboradores_db = crud.get_colaboradores(db)
        projetos_db = crud.get_projetos(db)
        
        # Convert to algorithm format
        colaboradores = []
        for col in colaboradores_db:
            colaborador_data = {
                "id": col.id,
                "nome": col.nome,
                "cargo": col.cargo.nome if col.cargo else "",
                "habilidades": set([h.nome for h in col.habilidades]),
                "ausencias": set(),
                "ferias": [],
                "transversal": bool(col.transversal),
                "squad_id": col.squad_id,
                "inicio": None,
                "termino": None
            }
            
            # Add work period dates
            if col.inicio:
                colaborador_data["inicio"] = (col.inicio - datetime.date(2024, 1, 1)).days
            if col.termino:
                colaborador_data["termino"] = (col.termino - datetime.date(2024, 1, 1)).days
            
            # Add absences
            for ausencia in col.ausencias:
                days_since_ref = (ausencia.data - datetime.date(2024, 1, 1)).days
                colaborador_data["ausencias"].add(days_since_ref)
            
            # Add vacation periods
            for ferias in col.ferias:
                inicio_days = (ferias.inicio - datetime.date(2024, 1, 1)).days
                termino_days = (ferias.termino - datetime.date(2024, 1, 1)).days
                colaborador_data["ferias"].append((inicio_days, termino_days))
            
            colaboradores.append(colaborador_data)
        
        # Convert projects
        projetos = []
        for proj in projetos_db:
            projeto_data = {
                "id": proj.id,
                "nome": proj.nome,
                "color": proj.color or "#3B82F6",
                "squad_id": proj.squad_id,
                "ano": proj.ano,
                "etapas": []
            }
            
            # Add project dates if available
            if proj.inicio:
                projeto_data["inicio"] = (proj.inicio - datetime.date(2024, 1, 1)).days
            if proj.termino:
                projeto_data["termino"] = (proj.termino - datetime.date(2024, 1, 1)).days
            
            # Add stages
            for etapa in sorted(proj.etapas, key=lambda e: e.ordem):
                etapa_data = {
                    "id": etapa.id,
                    "nome": etapa.nome,
                    "duracao_dias": etapa.duracao_dias,
                    "cargo_necessario": etapa.cargo_necessario.nome if etapa.cargo_necessario else "",
                    "habilidades_necessarias": set([h.nome for h in etapa.habilidades_necessarias]),
                    "ordem": etapa.ordem,
                    "predecessoras": [p.id for p in etapa.predecessoras]
                }
                projeto_data["etapas"].append(etapa_data)
            
            projetos.append(projeto_data)
        
        return colaboradores, projetos
    
    def convert_absences(self, colaboradores: List[Dict], ref_date: datetime.date) -> List[Dict]:
        """Convert absence dates to days since reference date"""
        for colaborador in colaboradores:
            new_ausencias = set()
            for ausencia_date in colaborador["ausencias"]:
                if isinstance(ausencia_date, datetime.date):
                    days_since_ref = (ausencia_date - ref_date).days
                    new_ausencias.add(days_since_ref)
                else:
                    new_ausencias.add(ausencia_date)
            colaborador["ausencias"] = new_ausencias
            
            # Convert vacation periods
            new_ferias = []
            for ferias in colaborador.get("ferias", []):
                if len(ferias) == 2:
                    inicio, termino = ferias
                    if isinstance(inicio, datetime.date):
                        inicio = (inicio - ref_date).days
                    if isinstance(termino, datetime.date):
                        termino = (termino - ref_date).days
                    new_ferias.append((inicio, termino))
                else:
                    new_ferias.append(ferias)
            colaborador["ferias"] = new_ferias
            
            # Convert work period dates
            if colaborador.get("inicio") and isinstance(colaborador["inicio"], datetime.date):
                colaborador["inicio"] = (colaborador["inicio"] - ref_date).days
            if colaborador.get("termino") and isinstance(colaborador["termino"], datetime.date):
                colaborador["termino"] = (colaborador["termino"] - ref_date).days
        
        return colaboradores
    
    def build_global_tasks(self, projetos: List[Dict]) -> List[Dict]:
        """Build global task list with proper ordering and dependencies"""
        tarefas_globais = []
        task_id_counter = 1
        
        for projeto in projetos:
            # Create mapping from etapa id to global task id
            etapa_to_task_id = {}
            
            # First pass: create tasks and assign IDs
            for etapa in projeto["etapas"]:
                etapa_to_task_id[etapa["id"]] = task_id_counter
                
                tarefa = {
                    "task_id": task_id_counter,
                    "projeto": projeto["nome"],
                    "projeto_id": projeto["id"],
                    "nome": etapa["nome"],
                    "duracao_dias": etapa["duracao_dias"],
                    "cargo_necessario": etapa["cargo_necessario"],
                    "habilidades_necessarias": etapa["habilidades_necessarias"],
                    "ordem": etapa["ordem"],
                    "predecessoras": []  # Will be filled in second pass
                }
                
                tarefas_globais.append(tarefa)
                task_id_counter += 1
            
            # Second pass: resolve predecessor references
            for i, etapa in enumerate(projeto["etapas"]):
                task_idx = None
                for j, tarefa in enumerate(tarefas_globais):
                    if (tarefa["projeto_id"] == projeto["id"] and 
                        tarefa["nome"] == etapa["nome"]):
                        task_idx = j
                        break
                
                if task_idx is not None:
                    predecessoras_ids = []
                    for pred_etapa_id in etapa["predecessoras"]:
                        if pred_etapa_id in etapa_to_task_id:
                            predecessoras_ids.append(etapa_to_task_id[pred_etapa_id])
                    
                    tarefas_globais[task_idx]["predecessoras"] = predecessoras_ids
        
        return tarefas_globais
    
    def filter_data(self, colaboradores: List[Dict], projetos: List[Dict], 
                   colaborador_ids: List[int] = None, projeto_ids: List[int] = None,
                   squad_id: int = None, ano: int = None) -> tuple:
        """Filter collaborators and projects based on selection"""
        
        # Filter collaborators
        filtered_colaboradores = colaboradores
        if colaborador_ids:
            filtered_colaboradores = [c for c in colaboradores if c["id"] in colaborador_ids]
        elif squad_id:
            filtered_colaboradores = [c for c in colaboradores if c.get("squad_id") == squad_id]
        
        # Filter projects
        filtered_projetos = projetos
        if projeto_ids:
            filtered_projetos = [p for p in projetos if p["id"] in projeto_ids]
        elif squad_id and ano:
            filtered_projetos = [p for p in projetos 
                               if p.get("squad_id") == squad_id and p.get("ano") == ano]
        
        return filtered_colaboradores, filtered_projetos
    
    def add_simulated_members(self, colaboradores: List[Dict], simulated_members: List[Dict]) -> List[Dict]:
        """Add simulated team members to collaborators list"""
        if not simulated_members:
            return colaboradores
        
        # Find the highest existing ID
        max_id = max([c["id"] for c in colaboradores]) if colaboradores else 0
        
        # Add simulated members with new IDs
        for i, member in enumerate(simulated_members):
            new_member = {
                "id": max_id + i + 1,
                "nome": member["nome"],
                "cargo": member["cargo"],
                "habilidades": set(member["habilidades"]),
                "ausencias": set(),
                "ferias": [],
                "transversal": member.get("transversal", False),
                "squad_id": member.get("squad_id"),
                "inicio": member.get("inicio"),
                "termino": member.get("termino")
            }
            colaboradores.append(new_member)
        
        return colaboradores
    
    async def execute_algorithm_stream(self, params: Dict, db: Session) -> AsyncGenerator[Dict, None]:
        """Execute CP algorithm with streaming progress"""
        try:
            # Load data
            colaboradores, projetos = self.load_data_from_db(db)
            
            # Parse reference date
            ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
            
            # Convert dates
            colaboradores = self.convert_absences(colaboradores, ref_date)
            
            # Filter data
            colaborador_ids = params.get("colaborador_ids")
            projeto_ids = params.get("projeto_ids")
            squad_id = params.get("squad_id")
            ano = params.get("ano")
            
            colaboradores, projetos = self.filter_data(
                colaboradores, projetos, colaborador_ids, projeto_ids, squad_id, ano
            )
            
            # Add simulated members
            simulated_members = params.get("simulated_members", [])
            colaboradores = self.add_simulated_members(colaboradores, simulated_members)
            
            # Build global tasks
            tarefas_globais = self.build_global_tasks(projetos)
            
            if not tarefas_globais:
                yield {"error": "Nenhuma tarefa encontrada para os projetos selecionados"}
                return
            
            if not colaboradores:
                yield {"error": "Nenhum colaborador encontrado para a seleção"}
                return
            
            # Prepare project constraints
            project_deadlines = {}
            project_start_dates = {}
            
            for projeto in projetos:
                if "termino" in projeto and projeto["termino"] is not None:
                    termino_days = projeto["termino"]
                    if isinstance(termino_days, datetime.date):
                        termino_days = (termino_days - ref_date).days
                    project_deadlines[projeto["nome"]] = termino_days
                
                if "inicio" in projeto and projeto["inicio"] is not None:
                    inicio_days = projeto["inicio"]
                    if isinstance(inicio_days, datetime.date):
                        inicio_days = (inicio_days - ref_date).days
                    project_start_dates[projeto["nome"]] = inicio_days
            
            # Configure CP algorithm with enhanced parameters (streaming)
            time_limit = params.get("time_limit_seconds", 600)  # Increased default
            makespan_weight = params.get("makespan_weight", 200)  # Increased focus on makespan
            load_balancing_weight = params.get("load_balancing_weight", 50)  # New parameter
            
            self.cp = ConstraintProgramming(
                makespan_weight=makespan_weight,
                time_limit_seconds=time_limit,
                load_balancing_weight=load_balancing_weight,
                parallelization_bonus=100
            )
            
            # Run algorithm with progress
            async for event in self.cp.run_with_progress(
                tarefas_globais, colaboradores, project_deadlines, project_start_dates
            ):
                if event.get("type") == "complete":
                    if event.get("best_solution"):
                        print("[CP] Algorithm complete, building schedule")
                        
                        # Get solver and variables from CP instance
                        solver, variables = self.cp.get_last_solver_info()
                        
                        if solver is not None and variables:
                            print("Using CP-specific schedule building with exact timing")
                            schedule = self.cp.scheduler.build_schedule_from_cp_solution(
                                event["best_solution"], tarefas_globais, colaboradores, ref_date, solver, variables
                            )
                        else:
                            print("Using standard schedule building (fallback)")
                            schedule = self.cp.scheduler.build_schedule(
                                event["best_solution"], tarefas_globais, colaboradores, ref_date
                            )
                        
                        # Return final result with schedule
                        final_event = event.copy()
                        final_event["schedule"] = schedule
                        
                        yield final_event
                    else:
                        yield event
                else:
                    yield event
                
        except Exception as e:
            import traceback
            print(f"Erro no CP service: {e}")
            traceback.print_exc()
            yield {"error": f"Erro na execução do CP: {str(e)}"}
    
    def execute_algorithm(self, params: Dict, db: Session) -> Dict:
        """Execute CP algorithm (synchronous version)"""
        try:
            # Load data
            colaboradores, projetos = self.load_data_from_db(db)
            
            # Parse reference date
            ref_date = datetime.datetime.strptime(params["ref_date"], "%Y-%m-%d").date()
            
            # Convert dates
            colaboradores = self.convert_absences(colaboradores, ref_date)
            
            # Filter data
            colaborador_ids = params.get("colaborador_ids")
            projeto_ids = params.get("projeto_ids")
            squad_id = params.get("squad_id")
            ano = params.get("ano")
            
            colaboradores, projetos = self.filter_data(
                colaboradores, projetos, colaborador_ids, projeto_ids, squad_id, ano
            )
            
            # Add simulated members
            simulated_members = params.get("simulated_members", [])
            colaboradores = self.add_simulated_members(colaboradores, simulated_members)
            
            # Build global tasks
            tarefas_globais = self.build_global_tasks(projetos)
            
            if not tarefas_globais:
                raise ValueError("Nenhuma tarefa encontrada para os projetos selecionados")
            
            if not colaboradores:
                raise ValueError("Nenhum colaborador encontrado para a seleção")
            
            # Prepare project constraints
            project_deadlines = {}
            project_start_dates = {}
            
            for projeto in projetos:
                if "termino" in projeto and projeto["termino"] is not None:
                    termino_days = projeto["termino"]
                    if isinstance(termino_days, datetime.date):
                        termino_days = (termino_days - ref_date).days
                    project_deadlines[projeto["nome"]] = termino_days
                
                if "inicio" in projeto and projeto["inicio"] is not None:
                    inicio_days = projeto["inicio"]
                    if isinstance(inicio_days, datetime.date):
                        inicio_days = (inicio_days - ref_date).days
                    project_start_dates[projeto["nome"]] = inicio_days
            
            # Configure CP algorithm with enhanced parameters (synchronous)
            time_limit = params.get("time_limit_seconds", 600)  # Increased default
            makespan_weight = params.get("makespan_weight", 200)  # Increased focus on makespan
            load_balancing_weight = params.get("load_balancing_weight", 50)  # New parameter
            
            self.cp = ConstraintProgramming(
                makespan_weight=makespan_weight,
                time_limit_seconds=time_limit,
                load_balancing_weight=load_balancing_weight,
                parallelization_bonus=100
            )
            
            # Run algorithm
            result = self.cp.run(
                tarefas_globais, colaboradores, project_deadlines, project_start_dates
            )
            
            if len(result) == 7:  # New format with solver and variables
                best_solution, best_fitness, fitness_history, penalties, violations, solver, variables = result
            else:  # Old format (fallback)
                best_solution, best_fitness, fitness_history, penalties, violations = result
                solver, variables = None, {}
            
            if not best_solution:
                raise ValueError("Nenhuma solução viável encontrada pelo CP")
            
            # Build schedule using CP-specific method if solver is available
            if solver is not None and variables:
                print("Using CP-specific schedule building with exact timing")
                schedule = self.cp.scheduler.build_schedule_from_cp_solution(
                    best_solution, tarefas_globais, colaboradores, ref_date, solver, variables
                )
            else:
                print("Using standard schedule building (fallback)")
                schedule = self.cp.scheduler.build_schedule(
                    best_solution, tarefas_globais, colaboradores, ref_date
                )
            
            # Validate and recalculate penalties for consistency
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
                "project_start_violation": 0,
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
                "project_start_violation": [],
                "work_period_violation": [],
                "vacation_conflict": []
            }
            
            # Validate each task assignment
            for i, task in enumerate(tarefas_globais):
                collaborator_id = best_solution[i]
                collaborator = next(c for c in colaboradores if c["id"] == collaborator_id)
                
                # Validate skills and position
                skill_violations = validator.validate_skills(task, collaborator)
                for v in skill_violations:
                    final_penalties["habilidades_incorretas"] += v.penalty
                    final_violations["habilidades_incorretas"].append(v.details)
                
                position_violations = validator.validate_position(task, collaborator)
                for v in position_violations:
                    final_penalties["cargo_incorreto"] += v.penalty
                    final_violations["cargo_incorreto"].append(v.details)
                
                # Validate availability (including work period and vacations)
                task_schedule = next(t for t in schedule if t["nome_tarefa"] == task["nome"])
                start_day = task_schedule["inicio_dias"]
                end_day = task_schedule["fim_dias"] + 1
                
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
            
            # Check project constraints
            project_completion = {}
            project_starts = {}
            
            for task_schedule in schedule:
                project_name = task_schedule["projeto"]
                end_day = task_schedule["fim_dias"]
                start_day = task_schedule["inicio_dias"]
                
                project_completion[project_name] = max(
                    project_completion.get(project_name, 0), end_day
                )
                
                if project_name not in project_starts:
                    project_starts[project_name] = start_day
                else:
                    project_starts[project_name] = min(project_starts[project_name], start_day)
            
            # Validate project start dates
            for project_name, required_start in project_start_dates.items():
                if project_name in project_starts:
                    actual_start = project_starts[project_name]
                    if actual_start < required_start:
                        start_violations = validator.validate_project_start(project_name, actual_start, required_start)
                        for v in start_violations:
                            final_penalties["project_start_violation"] += v.penalty
                            final_violations["project_start_violation"].append(v.details)
            
            # Validate project deadlines
            for project_name, deadline in project_deadlines.items():
                if project_name in project_completion:
                    actual_end = project_completion[project_name]
                    if actual_end > deadline:
                        deadline_violations = validator.validate_deadline(project_name, actual_end, deadline)
                        for v in deadline_violations:
                            final_penalties["deadline_violation"] += v.penalty
                            final_violations["deadline_violation"].append(v.details)
            
            # Save result to file for analysis
            try:
                formatted_result = self.result_saver.format_algorithm_result(
                    algorithm_name="CP",
                    solution=best_solution,
                    fitness=best_fitness,
                    fitness_history=fitness_history,
                    penalties=final_penalties,
                    violations=final_violations,
                    tasks=tarefas_globais,
                    collaborators=colaboradores,
                    schedule=schedule,
                    solve_info={"status": "OPTIMAL", "solver": "CP-SAT"}
                )
                
                self.result_saver.save_result(
                    algorithm_name="CP",
                    result_data=formatted_result,
                    params=params,
                    metadata={
                        "total_tasks": len(tarefas_globais),
                        "total_collaborators": len(colaboradores),
                        "execution_time": "N/A"
                    }
                )
            except Exception as e:
                print(f"Warning: Failed to save CP result to file: {e}")
            
            return {
                "tarefas": schedule,
                "melhor_fitness": best_fitness,
                "historico_fitness": fitness_history,
                "penalidades": final_penalties,
                "ocorrencias_penalidades": final_violations
            }
            
        except Exception as e:
            raise Exception(f"Erro na execução do CP: {str(e)}")