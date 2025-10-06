import datetime
from typing import List, Dict, Tuple

class TaskScheduler:
    """Handles task scheduling logic"""
    
    @staticmethod
    def calculate_task_timing(task: Dict, collaborator: Dict, project_end: int, 
                            collaborator_end: int, ref_date: datetime.date) -> Tuple[int, int]:
        """Calculate start and end times for a task"""
        start_day = max(project_end, collaborator_end)
        
        # Skip absences and weekends
        while (start_day in collaborator["ausencias"] or 
               TaskScheduler._is_weekend(start_day, ref_date)):
            start_day += 1
        
        end_day = start_day
        remaining_duration = task["duracao_dias"]
        
        while remaining_duration > 0:
            if (end_day not in collaborator["ausencias"] and 
                not TaskScheduler._is_weekend(end_day, ref_date)):
                remaining_duration -= 1
            end_day += 1
            
        return start_day, end_day
    
    @staticmethod
    def _is_weekend(day: int, ref_date: datetime.date) -> bool:
        """Check if a day is weekend"""
        actual_date = ref_date + datetime.timedelta(days=day)
        return actual_date.weekday() >= 5
    
    @staticmethod
    def build_schedule(solution: List[int], tasks: List[Dict], 
                      collaborators: List[Dict], ref_date: datetime.date) -> List[Dict]:
        """Build complete schedule from solution"""
        allocations = {col["id"]: [] for col in collaborators}
        project_ends = {task["projeto"]: 0 for task in tasks}
        schedule = []
        
        for i, task in enumerate(tasks):
            collaborator_id = solution[i]
            collaborator = next(c for c in collaborators if c["id"] == collaborator_id)
            
            # Get timing constraints
            project_end = project_ends[task["projeto"]]
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            
            # Calculate timing
            start_day, end_day = TaskScheduler.calculate_task_timing(
                task, collaborator, project_end, collaborator_end, ref_date
            )
            
            # Update tracking
            project_ends[task["projeto"]] = end_day
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