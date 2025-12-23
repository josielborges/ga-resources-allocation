import datetime
from typing import List, Dict, Tuple
from utils.calendar_utils import is_business_day, is_holiday, is_weekend

class TaskScheduler:
    """Handles task scheduling logic"""
    
    @staticmethod
    def calculate_task_timing(task: Dict, collaborator: Dict, project_start_dates: Dict[str, int], 
                            collaborator_end: int, ref_date: datetime.date, 
                            task_completions: Dict[int, int] = None) -> Tuple[int, int]:
        """Calculate start and end times for a task considering predecessors and project constraints"""
        # Consider predecessor completion times
        predecessor_end = 0
        if task_completions and "predecessoras" in task:
            for pred_id in task["predecessoras"]:
                if pred_id in task_completions:
                    predecessor_end = max(predecessor_end, task_completions[pred_id])
        
        # Consider project start date constraint
        project_start = 0
        if project_start_dates and task.get("projeto") in project_start_dates:
            project_start = project_start_dates[task["projeto"]]
        
        # Consider work period start date only if set
        work_start = collaborator.get("inicio")
        if work_start is not None:
            start_day = max(collaborator_end, predecessor_end, work_start, project_start)
        else:
            start_day = max(collaborator_end, predecessor_end, project_start)
        
        # Helper function to check if day is blocked (absences, weekends, holidays, and vacations)
        def is_day_blocked(day):
            # Check absences
            if day in collaborator["ausencias"]:
                return True
            
            # Check weekends and holidays
            actual_date = ref_date + datetime.timedelta(days=day)
            if not is_business_day(actual_date):
                return True
            
            # Check if day falls within any vacation period
            ferias_list = collaborator.get("ferias", [])
            for ferias_item in ferias_list:
                if isinstance(ferias_item, (tuple, list)) and len(ferias_item) == 2:
                    ferias_inicio, ferias_fim = ferias_item
                    if ferias_inicio <= day < ferias_fim:
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
        return is_weekend(actual_date)
    
    @staticmethod
    def _is_weekend_date(date: datetime.date) -> bool:
        """Check if a date is weekend"""
        return is_weekend(date)
    
    @staticmethod
    def _is_holiday_date(date: datetime.date) -> bool:
        """Check if a date is a Brazilian holiday"""
        return is_holiday(date)
    
    @staticmethod
    def work_day_to_calendar_date(work_day: int, ref_date: datetime.date) -> datetime.date:
        """
        Convert work day number to calendar date, skipping weekends and holidays
        work_day 0 = first business day from ref_date (or ref_date itself if it's a business day)
        """
        current_date = ref_date
        
        # If ref_date is not a business day, skip to first business day
        if not is_business_day(current_date):
            while not is_business_day(current_date):
                current_date += datetime.timedelta(days=1)
        
        # If work_day is 0, return the first business day (which is current_date now)
        if work_day == 0:
            return current_date
        
        # Count business days from the first business day
        days_counted = 0
        while days_counted < work_day:
            current_date += datetime.timedelta(days=1)
            if is_business_day(current_date):
                days_counted += 1
        
        return current_date
    
    def build_schedule_from_cp_solution(self, solution: List[int], tasks: List[Dict], 
                                       collaborators: List[Dict], ref_date: datetime.date,
                                       solver: 'cp_model.CpSolver', variables: Dict,
                                       project_start_dates: Dict[str, int] = None) -> List[Dict]:
        """
        Build schedule from CP solution.
        
        IMPORTANT: CP works with abstract "work days" but we need to convert to calendar dates
        considering holidays, weekends, vacations, and absences. We use the CP solution for
        task ordering and assignments, but recalculate actual dates using business day logic.
        """
        
        # Always use the standard scheduler which properly handles holidays and weekends
        # The CP solution provides optimal task assignments and ordering, but dates
        # must be recalculated to respect business days
        return TaskScheduler.build_schedule(solution, tasks, collaborators, ref_date, project_start_dates)

    @staticmethod
    def build_schedule(solution: List[int], tasks: List[Dict], 
                      collaborators: List[Dict], ref_date: datetime.date,
                      project_start_dates: Dict[str, int] = None) -> List[Dict]:
        """Build complete schedule from solution (standard method for GA/ACO)"""
        allocations = {col["id"]: [] for col in collaborators}
        task_completions = {}  # Track individual task completion times
        schedule = []
        
        for i, task in enumerate(tasks):
            collaborator_id = solution[i]
            collaborator = next(c for c in collaborators if c["id"] == collaborator_id)
            
            # Get timing constraints
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            
            # Calculate timing with predecessor and project constraints
            start_day, end_day = TaskScheduler.calculate_task_timing(
                task, collaborator, project_start_dates, collaborator_end, ref_date, task_completions
            )
            task_completions[task["task_id"]] = end_day
            allocations[collaborator_id].append((start_day, end_day))
            
            # Format dates
            start_date = (ref_date + datetime.timedelta(days=start_day)).strftime("%d/%m/%Y")
            end_date = (ref_date + datetime.timedelta(days=end_day - 1)).strftime("%d/%m/%Y")
            
            # Prepare vacation and absence information for this collaborator
            ferias_info = []
            ausencias_info = []
            
            # Process vacation periods - handle tuple format from database
            ferias_list = collaborator.get("ferias", [])
            for ferias_item in ferias_list:
                if isinstance(ferias_item, (tuple, list)) and len(ferias_item) == 2:
                    # Handle tuple/list format: (inicio_dias, fim_dias)
                    ferias_inicio, ferias_fim = ferias_item
                    ferias_start_date = (ref_date + datetime.timedelta(days=ferias_inicio)).strftime("%d/%m/%Y")
                    ferias_end_date = (ref_date + datetime.timedelta(days=ferias_fim - 1)).strftime("%d/%m/%Y")
                    ferias_info.append({
                        "inicio_dias": ferias_inicio,
                        "fim_dias": ferias_fim - 1,
                        "data_inicio": ferias_start_date,
                        "data_fim": ferias_end_date,
                        "duracao_dias": ferias_fim - ferias_inicio
                    })
            
            # Process absence days
            ausencias_set = collaborator.get("ausencias", set())
            for ausencia_day in sorted(ausencias_set):
                ausencia_date = (ref_date + datetime.timedelta(days=ausencia_day)).strftime("%d/%m/%Y")
                ausencias_info.append({
                    "dia": ausencia_day,
                    "data": ausencia_date
                })
            
            schedule.append({
                "projeto": task["projeto"],
                "nome_tarefa": task["nome"],
                "inicio_dias": start_day,
                "data_inicio": start_date,
                "fim_dias": end_day - 1,
                "data_fim": end_date,
                "colaborador": collaborator["nome"],
                "colaborador_id": collaborator["id"],
                "duracao_dias": task["duracao_dias"],
                "ferias": ferias_info,
                "ausencias": ausencias_info
            })
            
        return schedule