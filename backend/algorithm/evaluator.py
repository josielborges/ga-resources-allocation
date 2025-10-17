from typing import List, Dict, Tuple
from .constraints import ConstraintValidator, ConstraintViolation
from .scheduler import TaskScheduler

class SolutionEvaluator:
    """Evaluates genetic algorithm solutions"""
    
    def __init__(self, makespan_weight: int = 200):
        self.makespan_weight = makespan_weight
        self.validator = ConstraintValidator()
    
    def evaluate(self, solution: List[int], tasks: List[Dict], 
                collaborators: List[Dict], project_deadlines: Dict[str, int] = None, 
                project_start_dates: Dict[str, int] = None) -> Tuple[float, Dict, Dict]:
        """Evaluate a solution and return fitness, penalties, and violations"""
        
        allocations = {col["id"]: [] for col in collaborators}
        project_ends = {task["projeto"]: 0 for task in tasks}
        task_completions = {}  # Track individual task completion times
        
        penalties = {
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
        
        violations_details = {
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
        
        makespan = 0
        
        # Evaluate each task assignment
        for i, task in enumerate(tasks):
            collaborator_id = solution[i]
            collaborator = next(c for c in collaborators if c["id"] == collaborator_id)
            
            # Validate constraints
            skill_violations = self.validator.validate_skills(task, collaborator)
            position_violations = self.validator.validate_position(task, collaborator)
            
            # Apply penalties and collect details
            for violation in skill_violations:
                penalties["habilidades_incorretas"] += violation.penalty
                violations_details["habilidades_incorretas"].append(violation.details)
            
            for violation in position_violations:
                penalties["cargo_incorreto"] += violation.penalty
                violations_details["cargo_incorreto"].append(violation.details)
            
            # Calculate timing with predecessor constraints
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            
            # Consider predecessor completion times
            predecessor_end = 0
            if "predecessoras" in task:
                for pred_id in task["predecessoras"]:
                    if pred_id in task_completions:
                        predecessor_end = max(predecessor_end, task_completions[pred_id])
            
            # Consider project start date
            project_start = 0
            if project_start_dates and task["projeto"] in project_start_dates:
                project_start = project_start_dates[task["projeto"]]
            
            # Consider work period start date only if set
            work_start = collaborator.get("inicio")
            if work_start is not None:
                start_day = max(collaborator_end, predecessor_end, work_start, project_start)
            else:
                start_day = max(collaborator_end, predecessor_end, project_start)
            
            # Helper function to check if day is blocked (only absences, not vacations)
            def is_day_blocked(day):
                if day in collaborator["ausencias"]:
                    return True
                return False
            
            # Skip blocked days at start
            while is_day_blocked(start_day):
                start_day += 1
            
            # Calculate end day skipping blocked days
            end_day = start_day
            remaining_duration = task["duracao_dias"]
            while remaining_duration > 0:
                if not is_day_blocked(end_day):
                    remaining_duration -= 1
                end_day += 1
            
            # Check availability violations
            availability_violations = self.validator.validate_availability(
                collaborator, start_day, end_day, task
            )
            for violation in availability_violations:
                if violation.type == "work_period_violation":
                    penalties["work_period_violation"] += violation.penalty
                    violations_details["work_period_violation"].append(violation.details)
                elif violation.type == "vacation_conflict":
                    penalties["vacation_conflict"] += violation.penalty
                    violations_details["vacation_conflict"].append(violation.details)
                else:  # absence_conflict
                    penalties["ausencias"] += violation.penalty
                    violations_details["ausencias"].append(violation.details)
            
            # Update tracking
            task_completions[task["task_id"]] = end_day
            allocations[collaborator_id].append((start_day, end_day))
            makespan = max(makespan, end_day)
        
        # Check for overlaps
        overlap_violations = self.validator.validate_overlaps(allocations)
        for violation in overlap_violations:
            penalties["sobreposicoes_colaborador"] += violation.penalty
            violations_details["sobreposicoes_colaborador"].append(violation.details)
        
        # Check resource efficiency
        efficiency_violations = self.validator.validate_resource_efficiency(allocations, collaborators)
        for violation in efficiency_violations:
            penalties["resource_idle_time"] += violation.penalty
            violations_details["resource_idle_time"].append(violation.details)
        
        # Penalize gaps between project tasks
        project_intervals = {}
        for i, task in enumerate(tasks):
            project = task["projeto"]
            if project not in project_intervals:
                project_intervals[project] = []
            
            collaborator_id = solution[i]
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            start_day = collaborator_end
            end_day = start_day + task["duracao_dias"]
            project_intervals[project].append((start_day, end_day))
        
        for project, intervals in project_intervals.items():
            if len(intervals) > 1:
                sorted_intervals = sorted(intervals, key=lambda x: x[0])
                for i in range(len(sorted_intervals) - 1):
                    current_end = sorted_intervals[i][1]
                    next_start = sorted_intervals[i + 1][0]
                    gap = next_start - current_end
                    if gap > 0:
                        penalties["gaps_projeto"] += gap * 50
                        violations_details["gaps_projeto"].append({
                            "projeto": project,
                            "gap_dias": gap,
                            "entre_tarefas": f"Tarefa {i+1} e {i+2}"
                        })
        
        # Add makespan penalty
        penalties["makespan"] = makespan * self.makespan_weight
        
        # Check project deadlines and start dates
        if project_deadlines or project_start_dates:
            project_completion = {}
            project_starts = {}
            
            # Build project start/end tracking from allocations
            for i, task in enumerate(tasks):
                collaborator_id = solution[i]
                task_id = task["task_id"]
                
                if task_id in task_completions:
                    project = task["projeto"]
                    end_day = task_completions[task_id]
                    
                    # Track project end
                    project_completion[project] = max(
                        project_completion.get(project, 0),
                        end_day
                    )
                    
                    # Track project start (earliest task start)
                    start_day = end_day - task["duracao_dias"]
                    if project not in project_starts:
                        project_starts[project] = start_day
                    else:
                        project_starts[project] = min(project_starts[project], start_day)
            
            # Check deadlines
            if project_deadlines:
                for project_name, deadline_day in project_deadlines.items():
                    if project_name in project_completion:
                        actual_end_day = project_completion[project_name]
                        deadline_violations = self.validator.validate_deadline(
                            project_name, actual_end_day, deadline_day
                        )
                        for violation in deadline_violations:
                            penalties["deadline_violation"] += violation.penalty
                            violations_details["deadline_violation"].append(violation.details)
            
            # Check start dates  
            if project_start_dates:
                for project_name, required_start_day in project_start_dates.items():
                    if project_name in project_starts:
                        actual_start_day = project_starts[project_name]
                        if actual_start_day < required_start_day:
                            start_violations = self.validator.validate_project_start(
                                project_name, actual_start_day, required_start_day
                            )
                            for violation in start_violations:
                                penalties["project_start_violation"] += violation.penalty
                                violations_details["project_start_violation"].append(violation.details)
        
        # Calculate total fitness
        fitness = sum(penalties.values())
        
        return fitness, penalties, violations_details