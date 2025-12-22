import json
import datetime
import os
from typing import Dict, List, Any

class ResultSaver:
    """Utility class to save algorithm results to files for analysis"""
    
    def __init__(self, results_dir: str = "algorithm_results"):
        self.results_dir = results_dir
        # Create results directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)
    
    def save_result(self, algorithm_name: str, result_data: Dict[str, Any], 
                   params: Dict[str, Any] = None, metadata: Dict[str, Any] = None) -> str:
        """
        Save algorithm result to a JSON file
        
        Args:
            algorithm_name: Name of the algorithm (GA, ACO, CP)
            result_data: The algorithm result data
            params: Algorithm parameters used
            metadata: Additional metadata
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{algorithm_name.lower()}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # Prepare the complete result structure
        complete_result = {
            "algorithm": algorithm_name.upper(),
            "timestamp": datetime.datetime.now().isoformat(),
            "parameters": params or {},
            "metadata": metadata or {},
            "results": result_data
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ {algorithm_name.upper()} result saved to: {filepath}")
        return filepath
    
    def format_algorithm_result(self, algorithm_name: str, solution: List[int], 
                              fitness: float, fitness_history: List[float],
                              penalties: Dict[str, float], violations: Dict[str, List[Dict]],
                              tasks: List[Dict], collaborators: List[Dict],
                              schedule: List[Dict] = None, solve_info: Dict = None) -> Dict[str, Any]:
        """
        Format algorithm result into a standardized structure
        
        Args:
            algorithm_name: Name of the algorithm
            solution: Task assignments (collaborator IDs)
            fitness: Final fitness value
            fitness_history: Evolution of fitness over generations/iterations
            penalties: Penalty breakdown by type
            violations: Detailed violation information
            tasks: Task definitions
            collaborators: Collaborator definitions
            schedule: Generated schedule (optional)
            solve_info: Additional solver information (for CP)
            
        Returns:
            Formatted result dictionary
        """
        
        # Build task assignments with details
        task_assignments = []
        for i, task in enumerate(tasks):
            if i < len(solution):
                collab_id = solution[i]
                collaborator = next((c for c in collaborators if c["id"] == collab_id), None)
                
                # Check for violations
                task_violations = {
                    "skill_mismatch": False,
                    "position_mismatch": False,
                    "missing_skills": [],
                    "wrong_position": None
                }
                
                if collaborator:
                    required_skills = task["habilidades_necessarias"]
                    collab_skills = set(collaborator["habilidades"])
                    
                    if not required_skills.issubset(collab_skills):
                        task_violations["skill_mismatch"] = True
                        task_violations["missing_skills"] = list(required_skills - collab_skills)
                    
                    if task["cargo_necessario"] != collaborator["cargo"]:
                        task_violations["position_mismatch"] = True
                        task_violations["wrong_position"] = {
                            "required": task["cargo_necessario"],
                            "assigned": collaborator["cargo"]
                        }
                
                assignment = {
                    "task_id": task["task_id"],
                    "task_name": task["nome"],
                    "project": task["projeto"],
                    "duration_days": task["duracao_dias"],
                    "required_position": task["cargo_necessario"],
                    "required_skills": list(task["habilidades_necessarias"]),
                    "assigned_collaborator_id": collab_id,
                    "assigned_collaborator_name": collaborator["nome"] if collaborator else "Unknown",
                    "collaborator_position": collaborator["cargo"] if collaborator else "Unknown",
                    "collaborator_skills": list(collaborator["habilidades"]) if collaborator else [],
                    "violations": task_violations
                }
                task_assignments.append(assignment)
        
        # Calculate summary statistics
        total_violations = sum(len(v) for v in violations.values())
        skill_violations = len(violations.get("habilidades_incorretas", []))
        position_violations = len(violations.get("cargo_incorreto", []))
        
        # Collaborator utilization
        collaborator_usage = {}
        for assignment in task_assignments:
            collab_id = assignment["assigned_collaborator_id"]
            if collab_id not in collaborator_usage:
                collaborator_usage[collab_id] = {
                    "name": assignment["assigned_collaborator_name"],
                    "position": assignment["collaborator_position"],
                    "task_count": 0,
                    "total_days": 0,
                    "tasks": []
                }
            collaborator_usage[collab_id]["task_count"] += 1
            collaborator_usage[collab_id]["total_days"] += assignment["duration_days"]
            collaborator_usage[collab_id]["tasks"].append({
                "task_name": assignment["task_name"],
                "project": assignment["project"],
                "duration": assignment["duration_days"]
            })
        
        # Build the result structure
        result = {
            "summary": {
                "algorithm": algorithm_name.upper(),
                "total_tasks": len(tasks),
                "total_collaborators": len(collaborators),
                "tasks_assigned": len(task_assignments),
                "assignment_rate": len(task_assignments) / len(tasks) if tasks else 0,
                "final_fitness": fitness,
                "total_violations": total_violations,
                "skill_violations": skill_violations,
                "position_violations": position_violations,
                "convergence_generations": len(fitness_history)
            },
            "fitness_evolution": {
                "history": fitness_history,
                "initial_fitness": fitness_history[0] if fitness_history else None,
                "final_fitness": fitness_history[-1] if fitness_history else None,
                "improvement": fitness_history[0] - fitness_history[-1] if len(fitness_history) > 1 else 0
            },
            "penalties_breakdown": penalties,
            "violations_detailed": violations,
            "task_assignments": task_assignments,
            "collaborator_utilization": collaborator_usage,
            "schedule": schedule or [],
            "solver_info": solve_info or {}
        }
        
        return result
    
    def compare_results(self, file1: str, file2: str) -> Dict[str, Any]:
        """
        Compare two algorithm results
        
        Args:
            file1: Path to first result file
            file2: Path to second result file
            
        Returns:
            Comparison analysis
        """
        with open(file1, 'r', encoding='utf-8') as f:
            result1 = json.load(f)
        
        with open(file2, 'r', encoding='utf-8') as f:
            result2 = json.load(f)
        
        r1_summary = result1["results"]["summary"]
        r2_summary = result2["results"]["summary"]
        
        comparison = {
            "algorithms": {
                "algorithm_1": result1["algorithm"],
                "algorithm_2": result2["algorithm"]
            },
            "fitness_comparison": {
                "algorithm_1_fitness": r1_summary["final_fitness"],
                "algorithm_2_fitness": r2_summary["final_fitness"],
                "better_algorithm": result1["algorithm"] if r1_summary["final_fitness"] < r2_summary["final_fitness"] else result2["algorithm"],
                "fitness_difference": abs(r1_summary["final_fitness"] - r2_summary["final_fitness"]),
                "improvement_percentage": abs(r1_summary["final_fitness"] - r2_summary["final_fitness"]) / max(r1_summary["final_fitness"], r2_summary["final_fitness"]) * 100
            },
            "violations_comparison": {
                "algorithm_1_violations": r1_summary["total_violations"],
                "algorithm_2_violations": r2_summary["total_violations"],
                "better_algorithm": result1["algorithm"] if r1_summary["total_violations"] < r2_summary["total_violations"] else result2["algorithm"]
            },
            "assignment_comparison": {
                "algorithm_1_rate": r1_summary["assignment_rate"],
                "algorithm_2_rate": r2_summary["assignment_rate"],
                "both_complete": r1_summary["assignment_rate"] == 1.0 and r2_summary["assignment_rate"] == 1.0
            }
        }
        
        return comparison