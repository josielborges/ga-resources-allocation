import time
from typing import Dict, List, Tuple
from genetic_algorithm import GeneticAlgorithm
from ant_colony_optimization import AntColonyOptimization

class AlgorithmComparison:
    """Compare GA and ACO performance"""
    
    def __init__(self):
        self.ga = GeneticAlgorithm()
        self.aco = AntColonyOptimization()
    
    def run_comparison(self, tasks: List[Dict], collaborators: List[Dict], 
                      ga_params: Dict = None, aco_params: Dict = None, runs: int = 5) -> Dict:
        """Run both algorithms multiple times and compare results"""
        
        ga_results = []
        aco_results = []
        
        # GA parameters
        ga_pop_size = ga_params.get('tam_pop', 50) if ga_params else 50
        ga_generations = ga_params.get('n_gen', 100) if ga_params else 100
        crossover_prob = ga_params.get('pc', 0.8) if ga_params else 0.8
        mutation_prob = ga_params.get('pm', 0.2) if ga_params else 0.2
        
        # ACO parameters
        aco_pop_size = aco_params.get('tam_pop', 50) if aco_params else 50
        aco_generations = aco_params.get('n_gen', 100) if aco_params else 100
        alpha = aco_params.get('alpha', 0.5) if aco_params else 0.5
        beta = aco_params.get('beta', 3.0) if aco_params else 3.0
        rho = aco_params.get('rho', 0.05) if aco_params else 0.05
        q0 = aco_params.get('q0', 0.5) if aco_params else 0.5
        
        # Create ACO with custom parameters
        self.aco = AntColonyOptimization(alpha=alpha, beta=beta, rho=rho, q0=q0)
        
        print(f"Running comparison with {runs} runs each...")
        
        # Run GA
        for i in range(runs):
            print(f"GA Run {i+1}/{runs}")
            start_time = time.time()
            
            solution, fitness, history, penalties, violations = self.ga.run(
                ga_pop_size, ga_generations, crossover_prob, mutation_prob,
                tasks, collaborators
            )
            
            execution_time = time.time() - start_time
            
            ga_results.append({
                'fitness': fitness,
                'execution_time': execution_time,
                'penalties': penalties,
                'convergence_generation': self._find_convergence(history)
            })
        
        # Run ACO
        for i in range(runs):
            print(f"ACO Run {i+1}/{runs}")
            start_time = time.time()
            
            solution, fitness, history, penalties, violations = self.aco.run(
                aco_pop_size, aco_generations, tasks, collaborators
            )
            
            execution_time = time.time() - start_time
            
            aco_results.append({
                'fitness': fitness,
                'execution_time': execution_time,
                'penalties': penalties,
                'convergence_generation': self._find_convergence(history)
            })
        
        # Calculate statistics
        ga_stats = self._calculate_stats(ga_results)
        aco_stats = self._calculate_stats(aco_results)
        
        return {
            'ga_results': ga_results,
            'aco_results': aco_results,
            'ga_stats': ga_stats,
            'aco_stats': aco_stats,
            'comparison': self._compare_algorithms(ga_stats, aco_stats)
        }
    
    def _find_convergence(self, history: List[float]) -> int:
        """Find generation where algorithm converged"""
        if len(history) < 10:
            return len(history)
        
        for i in range(10, len(history)):
            if len(set(history[i-10:i])) == 1:
                return i - 10
        
        return len(history)
    
    def _calculate_stats(self, results: List[Dict]) -> Dict:
        """Calculate statistics from multiple runs"""
        fitnesses = [r['fitness'] for r in results]
        times = [r['execution_time'] for r in results]
        convergences = [r['convergence_generation'] for r in results]
        
        return {
            'best_fitness': min(fitnesses),
            'worst_fitness': max(fitnesses),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'avg_time': sum(times) / len(times),
            'avg_convergence': sum(convergences) / len(convergences),
            'fitness_std': self._std_dev(fitnesses)
        }
    
    def _std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _compare_algorithms(self, ga_stats: Dict, aco_stats: Dict) -> Dict:
        """Compare algorithm performance"""
        return {
            'fitness_improvement': (ga_stats['avg_fitness'] - aco_stats['avg_fitness']) / ga_stats['avg_fitness'] * 100,
            'time_difference': aco_stats['avg_time'] - ga_stats['avg_time'],
            'convergence_difference': aco_stats['avg_convergence'] - ga_stats['avg_convergence'],
            'winner': 'ACO' if aco_stats['avg_fitness'] < ga_stats['avg_fitness'] else 'GA'
        }