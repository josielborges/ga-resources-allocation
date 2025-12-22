import datetime
from typing import List, Dict, Tuple

class TaskScheduler:
    """Handles task scheduling logic"""
    
    @staticmethod
    def calculate_task_timing(task: Dict, collaborator: Dict, project_end: int, 
                            collaborator_end: int, ref_date: datetime.date, 
                            task_completions: Dict[int, int] = None) -> Tuple[int, int]:
        """Calculate start and end times for a task considering predecessors"""
        # Consider predecessor completion times
        predecessor_end = 0
        if task_completions and "predecessoras" in task:
            for pred_id in task["predecessoras"]:
                if pred_id in task_completions:
                    predecessor_end = max(predecessor_end, task_completions[pred_id])
        
        # Consider work period start date only if set
        work_start = collaborator.get("inicio")
        if work_start is not None:
            start_day = max(collaborator_end, predecessor_end, work_start)
        else:
            start_day = max(collaborator_end, predecessor_end)
        
        # Helper function to check if day is blocked (absences and weekends only, not vacations)
        def is_day_blocked(day):
            if day in collaborator["ausencias"]:
                return True
            if TaskScheduler._is_weekend(day, ref_date):
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
            
        return start_day, end_day
    
    @staticmethod
    def _is_weekend(day: int, ref_date: datetime.date) -> bool:
        """Check if a day is weekend"""
        actual_date = ref_date + datetime.timedelta(days=day)
        return actual_date.weekday() >= 5
    
    def build_schedule_from_cp_solution(self, solution: List[int], tasks: List[Dict], 
                                       collaborators: List[Dict], ref_date: datetime.date,
                                       solver: 'cp_model.CpSolver', variables: Dict) -> List[Dict]:
        """Build schedule from CP solution using the exact timing calculated by the solver"""
        schedule = []
        
        # Get collaborator mapping
        collab_map = {c["id"]: c for c in collaborators}
        
        for i, task in enumerate(tasks):
            collaborator_id = solution[i]
            collaborator = collab_map[collaborator_id]
            task_id = task["task_id"]
            
            # Get the exact start and end times calculated by the CP solver
            if task_id in variables['task_starts'] and task_id in variables['task_ends']:
                start_day = solver.Value(variables['task_starts'][task_id])
                end_day = solver.Value(variables['task_ends'][task_id])
            else:
                # Fallback to standard calculation if variables not found
                print(f"WARNING: CP timing variables not found for task {task_id}, using fallback")
                allocations = {col["id"]: [] for col in collaborators}
                task_completions = {}
                
                # Calculate using standard method
                collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
                start_day, end_day = TaskScheduler.calculate_task_timing(
                    task, collaborator, 0, collaborator_end, ref_date, task_completions
                )
            
            # Format dates
            start_date = (ref_date + datetime.timedelta(days=start_day)).strftime("%d/%m/%Y")
            end_date = (ref_date + datetime.timedelta(days=end_day - 1)).strftime("%d/%m/%Y")
            
            schedule.append({
                "projeto": task["projeto"],
                "nome_tarefa": task["nome"],
                "inicio_dias": start_day,
                "data_inicio": start_date,
                "fim_dias": end_day - 1,  # CP uses end_day as exclusive, we need inclusive
                "data_fim": end_date,
                "colaborador": collaborator["nome"],
                "duracao_dias": task["duracao_dias"]
            })
            
        return schedule

    @staticmethod
    def build_schedule(solution: List[int], tasks: List[Dict], 
                      collaborators: List[Dict], ref_date: datetime.date) -> List[Dict]:
        """Build complete schedule from solution (standard method for GA/ACO)"""
        allocations = {col["id"]: [] for col in collaborators}
        task_completions = {}  # Track individual task completion times
        schedule = []
        
        for i, task in enumerate(tasks):
            collaborator_id = solution[i]
            collaborator = next(c for c in collaborators if c["id"] == collaborator_id)
            
            # Get timing constraints
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            
            # Calculate timing with predecessor constraints
            start_day, end_day = TaskScheduler.calculate_task_timing(
                task, collaborator, 0, collaborator_end, ref_date, task_completions
            )
            task_completions[task["task_id"]] = end_day
            allocations[collaborator_id].append((start_day, end_day))
            
            # Format dates
            start_date = (ref_date + datetime.timedelta(days=start_day)).strftime("%d/%m/%Y")
            end_date = (ref_date + datetime.timedelta(days=end_day - 1)).strftime("%d/%m/%Y")
            
            schedule.append({
                "projeto": task["projeto"],
                "nome_tarefa": task["nome"],
                "inicio_dias": start_day,
                "data_inicio": start_date,
                "fim_dias": end_day - 1,
                "data_fim": end_date,
                "colaborador": collaborator["nome"],
                "duracao_dias": task["duracao_dias"]
            })
            
        return schedule