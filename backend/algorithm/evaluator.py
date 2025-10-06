from typing import List, Dict, Tuple
from .constraints import ConstraintValidator, ConstraintViolation
from .scheduler import TaskScheduler

class SolutionEvaluator:
    """Evaluates genetic algorithm solutions"""
    
    def __init__(self, makespan_weight: int = 200):
        self.makespan_weight = makespan_weight
        self.validator = ConstraintValidator()
    
    def evaluate(self, solution: List[int], tasks: List[Dict], 
                collaborators: List[Dict]) -> Tuple[float, Dict, Dict]:
        """Evaluate a solution and return fitness, penalties, and violations"""
        
        allocations = {col["id"]: [] for col in collaborators}
        project_ends = {task["projeto"]: 0 for task in tasks}
        
        penalties = {
            "habilidades_incorretas": 0,
            "cargo_incorreto": 0,
            "ausencias": 0,
            "sobreposicoes_colaborador": 0,
            "makespan": 0
        }
        
        violations_details = {
            "habilidades_incorretas": [],
            "cargo_incorreto": [],
            "ausencias": [],
            "sobreposicoes_colaborador": []
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
            
            # Calculate timing
            project_end = project_ends[task["projeto"]]
            collaborator_end = max([end for _, end in allocations[collaborator_id]], default=0)
            
            start_day = max(project_end, collaborator_end)
            while start_day in collaborator["ausencias"]:
                start_day += 1
            
            end_day = start_day
            remaining_duration = task["duracao_dias"]
            while remaining_duration > 0:
                if end_day not in collaborator["ausencias"]:
                    remaining_duration -= 1
                end_day += 1
            
            # Check availability violations
            availability_violations = self.validator.validate_availability(
                collaborator, start_day, end_day
            )
            for violation in availability_violations:
                penalties["ausencias"] += violation.penalty
                violations_details["ausencias"].append(violation.details)
            
            # Update tracking
            project_ends[task["projeto"]] = end_day
            allocations[collaborator_id].append((start_day, end_day))
            makespan = max(makespan, end_day)
        
        # Check for overlaps
        overlap_violations = self.validator.validate_overlaps(allocations)
        for violation in overlap_violations:
            penalties["sobreposicoes_colaborador"] += violation.penalty
            violations_details["sobreposicoes_colaborador"].append(violation.details)
        
        # Add makespan penalty
        penalties["makespan"] = makespan * self.makespan_weight
        
        # Calculate total fitness
        fitness = sum(penalties.values())
        
        return fitness, penalties, violations_details