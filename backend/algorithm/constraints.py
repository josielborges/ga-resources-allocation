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
        "makespan": 200,
        "resource_idle_time": 100,
        "bottleneck_delay": 300,
        "deadline_violation": 1000,
        "work_period_violation": 5000,
        "vacation_conflict": 2000
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
    def validate_availability(cls, collaborator: Dict, start_day: int, end_day: int, task: Dict = None) -> List[ConstraintViolation]:
        violations = []
        
        # Check work period
        inicio = collaborator.get("inicio")
        termino = collaborator.get("termino")
        if inicio is not None and inicio > 0 and start_day < inicio:
            violations.append(ConstraintViolation(
                type="work_period_violation",
                penalty=cls.PENALTIES["work_period_violation"],
                details={
                    "colaborador": collaborator["nome"],
                    "dia_inicio_tarefa": start_day,
                    "dia_inicio_trabalho": inicio
                }
            ))
        if termino is not None and termino > 0 and end_day > termino:
            violations.append(ConstraintViolation(
                type="work_period_violation",
                penalty=cls.PENALTIES["work_period_violation"],
                details={
                    "colaborador": collaborator["nome"],
                    "dia_fim_tarefa": end_day,
                    "dia_fim_trabalho": termino
                }
            ))
        
        # Check absences
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
        
        # Check vacations
        ferias_list = collaborator.get("ferias", [])
        
        for ferias in ferias_list:
            ferias_inicio, ferias_fim = ferias
            # Check if task overlaps with vacation period
            if start_day < ferias_fim and end_day > ferias_inicio:
                overlap_days = min(end_day, ferias_fim) - max(start_day, ferias_inicio)
                penalty_value = cls.PENALTIES["vacation_conflict"] * overlap_days
                details = {
                    "colaborador": collaborator["nome"],
                    "ferias_inicio": ferias_inicio,
                    "ferias_fim": ferias_fim,
                    "dias_sobrepostos": overlap_days,
                    "tarefa_inicio": start_day,
                    "tarefa_fim": end_day
                }
                if task:
                    details["projeto"] = task.get("projeto", "")
                    details["tarefa"] = task.get("nome", "")
                violations.append(ConstraintViolation(
                    type="vacation_conflict",
                    penalty=penalty_value,
                    details=details
                ))
        
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
    
    @classmethod
    def validate_resource_efficiency(cls, allocations: Dict[int, List[tuple]], 
                                   collaborators: List[Dict]) -> List[ConstraintViolation]:
        """Penalize idle time for scarce resources"""
        violations = []
        
        for collaborator in collaborators:
            collab_id = collaborator["id"]
            if collab_id not in allocations or not allocations[collab_id]:
                continue
                
            # Check if this is a scarce resource
            is_scarce = any(skill in ["Análise", "Analise"] for skill in collaborator["habilidades"])
            
            if is_scarce:
                intervals = sorted(allocations[collab_id], key=lambda x: x[0])
                total_idle = 0
                
                for i in range(len(intervals) - 1):
                    gap = intervals[i+1][0] - intervals[i][1]
                    if gap > 0:
                        total_idle += gap
                
                if total_idle > 5:
                    violations.append(ConstraintViolation(
                        type="resource_idle_time",
                        penalty=cls.PENALTIES["resource_idle_time"] * total_idle,
                        details={
                            "colaborador": collaborator["nome"],
                            "idle_days": total_idle
                        }
                    ))
        
        return violations

    @classmethod
    def validate_deadline(cls, project_name: str, project_end: int, deadline: int) -> List[ConstraintViolation]:
        """Validate project deadline constraint"""
        violations = []
        if deadline is not None and project_end > deadline:
            days_late = project_end - deadline
            violations.append(ConstraintViolation(
                type="deadline_violation",
                penalty=cls.PENALTIES["deadline_violation"] * days_late,
                details={
                    "projeto": project_name,
                    "dias_atraso": days_late,
                    "termino_planejado": deadline,
                    "termino_real": project_end
                }
            ))
        return violations
