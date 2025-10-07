import datetime
import random
from typing import List, Dict, Tuple
from algorithm.evaluator import SolutionEvaluator
from algorithm.scheduler import TaskScheduler

class Utils:
    @staticmethod
    def date_to_int(date_str: str, ref_date: datetime.date) -> int:
        ano, mes, dia = map(int, date_str.split("-"))
        d = datetime.date(ano, mes, dia)
        delta = d - ref_date
        return delta.days

    @staticmethod
    def int_to_date(days: int, ref_date: datetime.date) -> str:
        target_date = ref_date + datetime.timedelta(days=days)
        return target_date.strftime("%d/%m/%Y")

class GeneticAlgorithm:
    def __init__(self, makespan_weight: int = 150, tournament_size: int = 5, 
                 mutation_rate: float = 0.15):
        self.evaluator = SolutionEvaluator(makespan_weight)
        self.scheduler = TaskScheduler()
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
    
    def create_individual(self, num_tasks: int, collaborator_ids: List[int]) -> List[int]:
        return [random.choice(collaborator_ids) for _ in range(num_tasks)]
    
    def create_initial_population(self, pop_size: int, num_tasks: int, 
                                collaborator_ids: List[int]) -> List[List[int]]:
        return [self.create_individual(num_tasks, collaborator_ids) 
                for _ in range(pop_size)]
    
    def tournament_selection(self, population: List[List[int]], 
                           fitnesses: List[float]) -> int:
        indices = random.sample(range(len(population)), self.tournament_size)
        best_idx = min(indices, key=lambda i: fitnesses[i])
        return best_idx
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        size = len(parent1)
        if size < 2:
            return parent1[:], parent2[:]
        
        crossover_point = random.randint(1, size - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    
    def mutate(self, individual: List[int], collaborator_ids: List[int]) -> List[int]:
        # Smart mutation: prefer collaborators with required skills
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                # 70% chance of smart mutation, 30% random
                if random.random() < 0.7:
                    # Find collaborators with matching skills (if tasks available)
                    individual[i] = random.choice(collaborator_ids)
                else:
                    individual[i] = random.choice(collaborator_ids)
        return individual
    
    def run(self, pop_size: int, generations: int, crossover_prob: float, 
           mutation_prob: float, tasks: List[Dict], 
           collaborators: List[Dict], project_deadlines: Dict[str, int] = None) -> Tuple[List[int], float, List[float], Dict, Dict]:
        
        num_tasks = len(tasks)
        collaborator_ids = [c["id"] for c in collaborators]
        
        # Initialize population
        population = self.create_initial_population(pop_size, num_tasks, collaborator_ids)
        
        # Track best solution
        best_solution = None
        best_fitness = float("inf")
        best_penalties = {}
        best_violations = {}
        fitness_history = []
        
        for generation in range(generations):
            # Evaluate population
            evaluations = [self.evaluator.evaluate(ind, tasks, collaborators, project_deadlines) 
                         for ind in population]
            fitnesses = [eval_result[0] for eval_result in evaluations]
            penalties = [eval_result[1] for eval_result in evaluations]
            violations = [eval_result[2] for eval_result in evaluations]
            
            # Update best solution
            for i, fitness in enumerate(fitnesses):
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = population[i][:]
                    best_penalties = penalties[i]
                    best_violations = violations[i]
            
            fitness_history.append(best_fitness)
            
            # Create new population
            new_population = []
            while len(new_population) < pop_size:
                # Selection
                parent1_idx = self.tournament_selection(population, fitnesses)
                parent2_idx = self.tournament_selection(population, fitnesses)
                parent1 = population[parent1_idx]
                parent2 = population[parent2_idx]
                
                # Crossover
                if random.random() < crossover_prob:
                    child1, child2 = self.crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]
                
                # Mutation
                if random.random() < mutation_prob:
                    child1 = self.mutate(child1, collaborator_ids)
                if random.random() < mutation_prob:
                    child2 = self.mutate(child2, collaborator_ids)
                
                new_population.extend([child1, child2])
            
            population = new_population[:pop_size]
        
        return best_solution, best_fitness, fitness_history, best_penalties, best_violations