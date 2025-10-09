import random
import math
from typing import List, Dict, Tuple
from algorithm.evaluator import SolutionEvaluator
from algorithm.scheduler import TaskScheduler

class AntColonyOptimization:
    def __init__(self, makespan_weight: int = 150, alpha: float = 0.5, beta: float = 3.0, 
                 rho: float = 0.05, q0: float = 0.5):
        self.evaluator = SolutionEvaluator(makespan_weight)
        self.scheduler = TaskScheduler()
        self.alpha = alpha  # Pheromone importance (reduced)
        self.beta = beta    # Heuristic importance (increased)
        self.rho = rho      # Evaporation rate (very low for slow convergence)
        self.q0 = q0        # Exploitation vs exploration (balanced 50/50)
        
    def initialize_pheromones(self, num_tasks: int, collaborator_ids: List[int]) -> Dict:
        """Initialize pheromone matrix"""
        pheromones = {}
        initial_pheromone = 1.0 / (num_tasks * len(collaborator_ids))
        
        for task_idx in range(num_tasks):
            pheromones[task_idx] = {}
            for collab_id in collaborator_ids:
                pheromones[task_idx][collab_id] = initial_pheromone
        
        return pheromones
    
    def calculate_heuristic(self, task: Dict, collaborator: Dict) -> float:
        """Calculate heuristic value for task-collaborator assignment"""
        heuristic = 1.0
        
        # Skill match bonus
        required_skills = task["habilidades_necessarias"]
        collaborator_skills = set(collaborator["habilidades"])
        
        if required_skills.issubset(collaborator_skills):
            heuristic *= 10.0  # Strong bonus for skill match
        else:
            heuristic *= 0.1   # Heavy penalty for skill mismatch
        
        # Position match bonus
        if task["cargo_necessario"] == collaborator["cargo"]:
            heuristic *= 5.0
        else:
            heuristic *= 0.2
        
        # Availability bonus (fewer absences = better)
        absence_penalty = len(collaborator["ausencias"]) * 0.1
        heuristic *= max(0.1, 1.0 - absence_penalty)
        
        return heuristic
    
    def select_collaborator(self, task_idx: int, task: Dict, collaborators: List[Dict], 
                          pheromones: Dict, used_collaborators: Dict) -> int:
        """Select collaborator using ACO probability rules"""
        collaborator_ids = [c["id"] for c in collaborators]
        probabilities = {}
        total_prob = 0.0
        
        for collab_id in collaborator_ids:
            collaborator = next(c for c in collaborators if c["id"] == collab_id)
            
            # Calculate availability penalty based on current usage
            usage_penalty = 1.0
            if collab_id in used_collaborators:
                usage_penalty = 1.0 / (1.0 + len(used_collaborators[collab_id]) * 0.1)
            
            pheromone = pheromones[task_idx][collab_id]
            heuristic = self.calculate_heuristic(task, collaborator) * usage_penalty
            
            prob = (pheromone ** self.alpha) * (heuristic ** self.beta)
            probabilities[collab_id] = prob
            total_prob += prob
        
        # Normalize probabilities
        if total_prob > 0:
            for collab_id in probabilities:
                probabilities[collab_id] /= total_prob
        else:
            # Fallback to uniform distribution
            uniform_prob = 1.0 / len(collaborator_ids)
            probabilities = {collab_id: uniform_prob for collab_id in collaborator_ids}
        
        # Selection strategy
        if random.random() < self.q0:
            # Exploitation: choose best option
            return max(probabilities.keys(), key=lambda k: probabilities[k])
        else:
            # Exploration: roulette wheel selection
            rand_val = random.random()
            cumulative = 0.0
            for collab_id, prob in probabilities.items():
                cumulative += prob
                if rand_val <= cumulative:
                    return collab_id
            return random.choice(collaborator_ids)
    
    def construct_solution(self, tasks: List[Dict], collaborators: List[Dict], 
                         pheromones: Dict) -> List[int]:
        """Construct a solution using ACO principles"""
        solution = []
        used_collaborators = {}  # Track collaborator usage
        
        for task_idx, task in enumerate(tasks):
            collab_id = self.select_collaborator(task_idx, task, collaborators, 
                                               pheromones, used_collaborators)
            solution.append(collab_id)
            
            # Update usage tracking
            if collab_id not in used_collaborators:
                used_collaborators[collab_id] = []
            used_collaborators[collab_id].append(task_idx)
        
        return solution
    
    def update_pheromones(self, pheromones: Dict, solutions: List[List[int]], 
                         fitnesses: List[float], tasks: List[Dict]):
        """Update pheromone levels based on solution quality"""
        # Evaporation
        for task_idx in pheromones:
            for collab_id in pheromones[task_idx]:
                pheromones[task_idx][collab_id] *= (1.0 - self.rho)
        
        # Reinforcement - only best solution deposits (elitist strategy)
        best_idx = fitnesses.index(min(fitnesses))
        best_solution = solutions[best_idx]
        best_fitness = fitnesses[best_idx]
        
        # Small deposit to prevent premature convergence
        if best_fitness > 0:
            deposit = 0.1 / best_fitness  # Very small deposit
        else:
            deposit = 0.1
        
        # Deposit pheromones only for best solution
        for task_idx, collab_id in enumerate(best_solution):
            pheromones[task_idx][collab_id] += deposit
    
    def local_search(self, solution: List[int], tasks: List[Dict], 
                    collaborators: List[Dict], project_deadlines: Dict[str, int] = None) -> List[int]:
        """Apply local search to improve solution"""
        improved_solution = solution[:]
        current_fitness = self.evaluator.evaluate(improved_solution, tasks, collaborators, project_deadlines)[0]
        
        collaborator_ids = [c["id"] for c in collaborators]
        
        # Try swapping assignments for tasks with violations
        for i in range(len(solution)):
            original_collab = improved_solution[i]
            
            # Try other collaborators
            for new_collab in collaborator_ids:
                if new_collab != original_collab:
                    improved_solution[i] = new_collab
                    new_fitness = self.evaluator.evaluate(improved_solution, tasks, collaborators, project_deadlines)[0]
                    
                    if new_fitness < current_fitness:
                        current_fitness = new_fitness
                        break
                    else:
                        improved_solution[i] = original_collab
        
        return improved_solution
    
    def run(self, num_ants: int, max_iterations: int, tasks: List[Dict], 
           collaborators: List[Dict], project_deadlines: Dict[str, int] = None) -> Tuple[List[int], float, List[float], Dict, Dict]:
        """Run ACO algorithm"""
        
        num_tasks = len(tasks)
        collaborator_ids = [c["id"] for c in collaborators]
        
        # Initialize pheromones
        pheromones = self.initialize_pheromones(num_tasks, collaborator_ids)
        
        # Track best solution
        best_solution = None
        best_fitness = float("inf")
        best_penalties = {}
        best_violations = {}
        fitness_history = []
        
        for iteration in range(max_iterations):
            # Generate solutions with ants
            solutions = []
            fitnesses = []
            penalties_list = []
            violations_list = []
            
            for ant in range(num_ants):
                solution = self.construct_solution(tasks, collaborators, pheromones)
                
                # Apply local search with decreasing probability
                local_search_prob = 0.5 * (1.0 - iteration / max_iterations)
                if random.random() < local_search_prob:
                    solution = self.local_search(solution, tasks, collaborators, project_deadlines)
                
                fitness, penalties, violations = self.evaluator.evaluate(solution, tasks, collaborators, project_deadlines)
                
                solutions.append(solution)
                fitnesses.append(fitness)
                penalties_list.append(penalties)
                violations_list.append(violations)
                
                # Update best solution
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = solution[:]
                    best_penalties = penalties
                    best_violations = violations
            
            # Update pheromones
            self.update_pheromones(pheromones, solutions, fitnesses, tasks)
            
            fitness_history.append(best_fitness)
            
            # Early stopping only after significant iterations with minimal improvement
            if iteration >= max_iterations * 0.5 and len(fitness_history) >= 30:
                recent_improvement = fitness_history[-30] - fitness_history[-1]
                if recent_improvement < 0.001 * abs(fitness_history[-30]):  # Less than 0.1% improvement
                    break
        
        return best_solution, best_fitness, fitness_history, best_penalties, best_violations