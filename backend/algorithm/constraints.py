from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class ConstraintViolation:
    type: str
    penalty: int
    details: Dict

class ConstraintValidator:
    """Validates and calculates penalties for constraint violations"""
    
    PENALTIES = {
        "missing_skills": 10000,
        "wrong_position": 10000,
        "absence_conflict": 500,
        "collaborator_overlap": 2000,
        "project_overlap": 1000,
        "makespan": 200
    }
    
    @classmethod
    def validate_skills(cls, task: Dict, collaborator: Dict) -> List[ConstraintViolation]:
        violations = []
        required_skills = task["habilidades_necessarias"]
        collaborator_skills = set(collaborator["habilidades"])
        
        if not required_skills.issubset(collaborator_skills):
            violations.append(ConstraintViolation(
                type="missing_skills",
                penalty=cls.PENALTIES["missing_skills"],
                details={
                    "projeto": task["projeto"],
                    "tarefa": task["nome"],
                    "colaborador": collaborator["nome"],
                    "habilidades_necessarias": ", ".join(required_skills),
                    "habilidades_colaborador": ", ".join(collaborator_skills)
                }
            ))
        return violations
    
    @classmethod
    def validate_position(cls, task: Dict, collaborator: Dict) -> List[ConstraintViolation]:
        violations = []
        if task["cargo_necessario"] != collaborator["cargo"]:
            violations.append(ConstraintViolation(
                type="wrong_position",
                penalty=cls.PENALTIES["wrong_position"],
                details={
                    "projeto": task["projeto"],
                    "tarefa": task["nome"],
                    "colaborador": collaborator["nome"],
                    "cargo_necessario": task["cargo_necessario"],
                    "cargo_colaborador": collaborator["cargo"]
                }
            ))
        return violations
    
    @classmethod
    def validate_availability(cls, collaborator: Dict, start_day: int, end_day: int) -> List[ConstraintViolation]:
        violations = []
        for day in range(start_day, end_day):
            if day in collaborator["ausencias"]:
                violations.append(ConstraintViolation(
                    type="absence_conflict",
                    penalty=cls.PENALTIES["absence_conflict"],
                    details={
                        "colaborador": collaborator["nome"],
                        "dia": day
                    }
                ))
                break
        return violations
    
    @classmethod
    def validate_overlaps(cls, allocations: Dict[int, List[tuple]]) -> List[ConstraintViolation]:
        violations = []
        for collaborator_id, intervals in allocations.items():
            sorted_intervals = sorted(intervals, key=lambda x: x[0])
            for i in range(len(sorted_intervals)):
                for j in range(i + 1, len(sorted_intervals)):
                    start1, end1 = sorted_intervals[i]
                    start2, end2 = sorted_intervals[j]
                    if start1 < end2 and start2 < end1:
                        violations.append(ConstraintViolation(
                            type="collaborator_overlap",
                            penalty=cls.PENALTIES["collaborator_overlap"],
                            details={
                                "colaborador_id": collaborator_id,
                                "intervalo1": (start1, end1),
                                "intervalo2": (start2, end2)
                            }
                        ))
        return violations