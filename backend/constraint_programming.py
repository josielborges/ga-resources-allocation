import datetime
import asyncio
from typing import List, Dict, Tuple, AsyncGenerator, Optional

try:
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False
    cp_model = None

from algorithm.evaluator import SolutionEvaluator
from algorithm.scheduler import TaskScheduler

def sanitize_for_json(value):
    """Convert infinite or NaN values to safe numbers for JSON serialization"""
    if value == float('inf') or value != value:  # NaN check
        return 999999999
    return value

class ConstraintProgramming:
    def __init__(self, makespan_weight: int = 200, time_limit_seconds: int = 600, 
                 load_balancing_weight: int = 50, parallelization_bonus: int = 100):
        if not ORTOOLS_AVAILABLE:
            raise ImportError("Google OR-Tools não está instalado. Execute: pip install ortools")
        
        self.evaluator = SolutionEvaluator(makespan_weight)
        self.scheduler = TaskScheduler()
        self.time_limit_seconds = time_limit_seconds
        self.makespan_weight = makespan_weight
        self.load_balancing_weight = load_balancing_weight
        self.parallelization_bonus = parallelization_bonus
        
        # Internal state for solver and variables (not serialized)
        self._last_solver = None
        self._last_variables = None
    
    def get_last_solver_info(self):
        """Get the last solver and variables for internal use"""
        return self._last_solver, self._last_variables
    
    def create_cp_model(self, tasks: List[Dict], collaborators: List[Dict], 
                       project_deadlines: Dict[str, int] = None,
                       project_start_dates: Dict[str, int] = None) -> Tuple[cp_model.CpModel, Dict]:
        """Create optimized CP-SAT model focusing on makespan reduction and load balancing"""
        model = cp_model.CpModel()
        
        # Variables dictionary to store all decision variables
        variables = {
            'task_assignments': {},  # task_id -> collaborator_id
            'task_starts': {},       # task_id -> start_day
            'task_ends': {},         # task_id -> end_day
            'makespan': None,        # total project duration
            'project_makespans': {}, # makespan per project
            'collaborator_loads': {},# workload per collaborator
            'soft_violations': {},   # soft constraint violations
            'parallelization_vars': {} # variables to encourage parallelization
        }
        
        # Create collaborator mapping and analyze capabilities
        collab_ids = [c["id"] for c in collaborators]
        collab_map = {c["id"]: c for c in collaborators}
        
        # Analyze task requirements and collaborator capabilities
        skill_demand = {}
        position_demand = {}
        for task in tasks:
            for skill in task["habilidades_necessarias"]:
                skill_demand[skill] = skill_demand.get(skill, 0) + task["duracao_dias"]
            pos = task["cargo_necessario"]
            position_demand[pos] = position_demand.get(pos, 0) + task["duracao_dias"]
        
        # Calculate smarter horizon based on critical path and resource constraints
        total_duration = sum(task["duracao_dias"] for task in tasks)
        num_collaborators = len(collaborators)
        theoretical_min = total_duration // num_collaborators if num_collaborators > 0 else total_duration
        
        # More conservative horizon calculation
        max_task_duration = max(task["duracao_dias"] for task in tasks) if tasks else 0
        
        # Consider project deadlines and start dates in horizon calculation
        max_deadline = 0
        max_start_date = 0
        if project_deadlines:
            max_deadline = max(project_deadlines.values())
        if project_start_dates:
            max_start_date = max(project_start_dates.values())
        
        # Set horizon as the maximum of several estimates with safety margins
        horizon_estimates = [
            theoretical_min * 3,      # More conservative estimate based on resources
            total_duration * 2,       # Sequential execution with buffer
            max_deadline + 200,       # Deadline plus large buffer
            max_start_date + total_duration + 100,  # Start date plus work duration
            1000                      # Minimum reasonable horizon
        ]
        
        max_horizon = max(h for h in horizon_estimates if h > 0)
        
        # Ensure horizon can accommodate the longest task from any start date
        max_horizon = max(max_horizon, max_start_date + max_task_duration * 3)
        
        print(f"CP Model: Using horizon = {max_horizon} days (total_duration={total_duration}, max_task={max_task_duration})")
        
        # Group tasks by project for better organization
        projects = {}
        for task in tasks:
            proj_name = task["projeto"]
            if proj_name not in projects:
                projects[proj_name] = []
            projects[proj_name].append(task)
        
        # Validate input data before creating variables
        print(f"CP Model validation: {len(tasks)} tasks, {len(collaborators)} collaborators, horizon={max_horizon}")
        
        # Check for empty inputs
        if not tasks:
            raise ValueError("No tasks provided to CP model")
        if not collaborators:
            raise ValueError("No collaborators provided to CP model")
        
        # Validate task data
        for task in tasks:
            if task["duracao_dias"] <= 0:
                raise ValueError(f"Task {task['task_id']} has invalid duration: {task['duracao_dias']}")
            if task["duracao_dias"] > max_horizon:
                print(f"WARNING: Task {task['task_id']} duration ({task['duracao_dias']}) exceeds horizon ({max_horizon})")
        
        # Validate collaborator IDs are unique
        collab_ids_set = set(collab_ids)
        if len(collab_ids_set) != len(collab_ids):
            raise ValueError("Duplicate collaborator IDs found")
        
        # 1. Task assignment variables with intelligent domain restriction
        for task in tasks:
            task_id = task["task_id"]
            
            # Create preference-based domain (prefer suitable collaborators)
            suitable_collabs = []
            less_suitable_collabs = []
            
            for collab_id in collab_ids:
                collab = collab_map[collab_id]
                
                # Check skill match
                has_skills = task["habilidades_necessarias"].issubset(set(collab["habilidades"]))
                has_position = task["cargo_necessario"] == collab["cargo"]
                
                if has_skills and has_position:
                    suitable_collabs.append(collab_id)
                elif has_skills or has_position:
                    less_suitable_collabs.append(collab_id)
                else:
                    less_suitable_collabs.append(collab_id)
            
            # Prefer suitable collaborators but allow all (for feasibility)
            domain_collabs = suitable_collabs + less_suitable_collabs
            if not domain_collabs:
                domain_collabs = collab_ids
            
            variables['task_assignments'][task_id] = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(domain_collabs),
                f'assign_task_{task_id}'
            )
        
        # 2. Enhanced task timing variables with project-aware scheduling
        for task in tasks:
            task_id = task["task_id"]
            duration = task["duracao_dias"]
            
            # Smart start time bounds
            min_start = 0
            
            # Apply project start date constraint (hard)
            if project_start_dates and task["projeto"] in project_start_dates:
                project_min_start = project_start_dates[task["projeto"]]
                min_start = max(min_start, project_min_start)
                print(f"Task {task_id} ({task['projeto']}): Applied project start constraint, min_start = {min_start} (project requires >= {project_min_start})")
            
            # Apply collaborator start date constraints (hard) - NEW FIX
            # Find the minimum start date among all potential collaborators
            earliest_collab_start = None
            for collab_id in collab_ids:
                collab = collab_map[collab_id]
                if collab.get("inicio") is not None and collab["inicio"] > 0:
                    if earliest_collab_start is None:
                        earliest_collab_start = collab["inicio"]
                    else:
                        earliest_collab_start = min(earliest_collab_start, collab["inicio"])
            
            # If all collaborators have start dates, enforce the earliest one as minimum
            # This ensures the task cannot start before any collaborator is available
            if earliest_collab_start is not None:
                min_start = max(min_start, earliest_collab_start)
                print(f"Task {task_id}: Applying collaborator start constraint, min_start = {min_start}")
            
            # Calculate max_start ensuring valid domain - FIXED LOGIC
            # Ensure we have enough horizon for this task
            required_horizon = min_start + duration
            if max_horizon < required_horizon:
                max_horizon = required_horizon + 100  # Add buffer
            
            # Calculate max_start with proper bounds
            max_start = max_horizon - duration
            
            # Ensure valid domain: max_start >= min_start
            if max_start < min_start:
                # Expand horizon to accommodate constraints
                max_horizon = min_start + duration + 100
                max_start = max_horizon - duration
            
            # Final safety check - ensure we have a valid domain
            if max_start < min_start:
                max_start = min_start
                max_horizon = max_start + duration + 100
            
            # Ensure we have a positive domain size
            if max_start < min_start:
                print(f"WARNING: Invalid domain for task {task_id}: min_start={min_start}, max_start={max_start}")
                max_start = min_start  # Force valid domain
            
            variables['task_starts'][task_id] = model.NewIntVar(
                min_start, max_start, f'start_task_{task_id}'
            )
            
            # Calculate end time bounds with proper validation
            min_end = min_start + duration
            max_end = max_start + duration
            
            # Ensure max_end is reasonable
            if max_end > max_horizon:
                max_end = max_horizon
            
            # Ensure valid end domain
            if max_end < min_end:
                max_end = min_end
            
            variables['task_ends'][task_id] = model.NewIntVar(
                min_end, max_end, f'end_task_{task_id}'
            )
            
            # Link start, duration, and end
            model.Add(variables['task_ends'][task_id] == 
                     variables['task_starts'][task_id] + duration)
        
        # 3. Global and per-project makespan variables
        variables['makespan'] = model.NewIntVar(0, max_horizon * 2, 'global_makespan')
        
        # Global makespan constraint
        for task in tasks:
            task_id = task["task_id"]
            model.Add(variables['makespan'] >= variables['task_ends'][task_id])
        
        # Per-project makespan tracking
        for proj_name, proj_tasks in projects.items():
            proj_makespan = model.NewIntVar(0, max_horizon * 2, f'makespan_{proj_name}')
            variables['project_makespans'][proj_name] = proj_makespan
            
            for task in proj_tasks:
                task_id = task["task_id"]
                model.Add(proj_makespan >= variables['task_ends'][task_id])
        
        # 4. Collaborator workload variables for load balancing
        for collab_id in collab_ids:
            variables['collaborator_loads'][collab_id] = model.NewIntVar(
                0, total_duration, f'load_{collab_id}'
            )
        
        # Calculate actual workloads
        for collab_id in collab_ids:
            workload_terms = []
            for task in tasks:
                task_id = task["task_id"]
                is_assigned = model.NewBoolVar(f'assigned_{task_id}_{collab_id}')
                model.Add(variables['task_assignments'][task_id] == collab_id).OnlyEnforceIf(is_assigned)
                model.Add(variables['task_assignments'][task_id] != collab_id).OnlyEnforceIf(is_assigned.Not())
                
                workload_contribution = model.NewIntVar(0, task["duracao_dias"], f'contrib_{task_id}_{collab_id}')
                model.Add(workload_contribution == task["duracao_dias"]).OnlyEnforceIf(is_assigned)
                model.Add(workload_contribution == 0).OnlyEnforceIf(is_assigned.Not())
                
                workload_terms.append(workload_contribution)
            
            if workload_terms:
                model.Add(variables['collaborator_loads'][collab_id] == sum(workload_terms))
        
        # 5. Predecessor constraints (hard) with intelligent scheduling
        task_levels = self._calculate_task_levels(tasks)
        for task in tasks:
            task_id = task["task_id"]
            if "predecessoras" in task and task["predecessoras"]:
                for pred_id in task["predecessoras"]:
                    if pred_id in variables['task_ends']:
                        # Add small buffer between dependent tasks for better scheduling
                        model.Add(variables['task_starts'][task_id] >= 
                                variables['task_ends'][pred_id])
        
        # 6. Enhanced collaborator non-overlap constraints with optimization hints
        for collab_id in collab_ids:
            intervals = []
            for task in tasks:
                task_id = task["task_id"]
                duration = task["duracao_dias"]
                
                # Create optional interval
                is_assigned = model.NewBoolVar(f'interval_assigned_{task_id}_{collab_id}')
                model.Add(variables['task_assignments'][task_id] == collab_id).OnlyEnforceIf(is_assigned)
                model.Add(variables['task_assignments'][task_id] != collab_id).OnlyEnforceIf(is_assigned.Not())
                
                # HARD CONSTRAINT: If assigned to this collaborator, respect their start date
                collab = collab_map[collab_id]
                if collab.get("inicio") is not None and collab["inicio"] > 0:
                    # Task cannot start before collaborator's start date if assigned to them
                    model.Add(variables['task_starts'][task_id] >= collab["inicio"]).OnlyEnforceIf(is_assigned)
                    print(f"Added hard constraint: Task {task_id} assigned to collab {collab_id} must start >= day {collab['inicio']}")
                
                # HARD CONSTRAINT: If assigned to this collaborator, respect their end date
                if collab.get("termino") is not None and collab["termino"] < max_horizon:
                    # Task must end before collaborator's end date if assigned to them
                    model.Add(variables['task_ends'][task_id] <= collab["termino"]).OnlyEnforceIf(is_assigned)
                    print(f"Added hard constraint: Task {task_id} assigned to collab {collab_id} must end <= day {collab['termino']}")
                
                interval = model.NewOptionalIntervalVar(
                    variables['task_starts'][task_id],
                    duration,
                    variables['task_ends'][task_id],
                    is_assigned,
                    f'interval_{task_id}_{collab_id}'
                )
                intervals.append(interval)
            
            # No overlap constraint
            model.AddNoOverlap(intervals)
        
        # 7. Parallelization encouragement variables
        # Encourage tasks to run in parallel when possible
        for level in range(max(task_levels.values()) + 1):
            level_tasks = [t for t in tasks if task_levels.get(t["task_id"], 0) == level]
            if len(level_tasks) > 1:
                # Create variables to track parallel execution
                parallel_bonus = model.NewIntVar(0, len(level_tasks) * self.parallelization_bonus, 
                                               f'parallel_bonus_level_{level}')
                variables['parallelization_vars'][level] = parallel_bonus
                
                # Bonus for tasks starting at similar times
                for i, task1 in enumerate(level_tasks):
                    for task2 in level_tasks[i+1:]:
                        task1_id = task1["task_id"]
                        task2_id = task2["task_id"]
                        
                        # Check if tasks can run in parallel (different collaborators)
                        different_collabs = model.NewBoolVar(f'diff_collab_{task1_id}_{task2_id}')
                        model.Add(variables['task_assignments'][task1_id] != 
                                variables['task_assignments'][task2_id]).OnlyEnforceIf(different_collabs)
                        model.Add(variables['task_assignments'][task1_id] == 
                                variables['task_assignments'][task2_id]).OnlyEnforceIf(different_collabs.Not())
        
        # 8. Soft constraints with enhanced penalties
        penalty_vars = []
        
        # 8. HARD CONSTRAINTS: Skills and Position Requirements
        # These are now mandatory constraints - tasks can only be assigned to collaborators
        # with the required skills and positions
        
        print("CP Model: Adding HARD constraints for skills and positions...")
        
        for task in tasks:
            task_id = task["task_id"]
            required_skills = task["habilidades_necessarias"]
            required_position = task["cargo_necessario"]
            
            # Find collaborators who meet BOTH skill and position requirements
            suitable_collabs = []
            for collab_id in collab_ids:
                collab = collab_map[collab_id]
                collab_skills = set(collab["habilidades"])
                collab_position = collab["cargo"]
                
                # Check if collaborator has required skills AND position
                has_skills = required_skills.issubset(collab_skills)
                has_position = collab_position == required_position
                
                if has_skills and has_position:
                    suitable_collabs.append(collab_id)
            
            if not suitable_collabs:
                # No suitable collaborator found - this will make the problem infeasible
                print(f"WARNING: Task {task_id} ({task['nome']}) requires skills {required_skills} and position {required_position}")
                print(f"         No collaborator meets these requirements!")
                print("         Available collaborators:")
                for collab_id in collab_ids:
                    collab = collab_map[collab_id]
                    print(f"         - {collab['nome']}: {collab['cargo']}, skills: {collab['habilidades']}")
                
                # Still add the constraint - it will make the problem infeasible as expected
                # This forces the user to either adjust requirements or add suitable collaborators
                model.Add(False)  # This makes the problem infeasible
            else:
                # HARD CONSTRAINT: Task can only be assigned to suitable collaborators
                print(f"Task {task_id} ({task['nome']}) can be assigned to: {[collab_map[c]['nome'] for c in suitable_collabs]}")
                
                # Create constraint that task assignment must be one of the suitable collaborators
                suitable_assignments = []
                for collab_id in suitable_collabs:
                    is_suitable = model.NewBoolVar(f'suitable_{task_id}_{collab_id}')
                    model.Add(variables['task_assignments'][task_id] == collab_id).OnlyEnforceIf(is_suitable)
                    model.Add(variables['task_assignments'][task_id] != collab_id).OnlyEnforceIf(is_suitable.Not())
                    suitable_assignments.append(is_suitable)
                
                # Exactly one of the suitable assignments must be true
                model.Add(sum(suitable_assignments) == 1)
        
        # Remove soft skill and position penalties since they are now hard constraints
        variables['soft_violations']['skill_penalty'] = model.NewIntVar(0, 0, 'skill_penalty')
        model.Add(variables['soft_violations']['skill_penalty'] == 0)
        
        variables['soft_violations']['position_penalty'] = model.NewIntVar(0, 0, 'position_penalty')
        model.Add(variables['soft_violations']['position_penalty'] == 0)
        
        # Load balancing penalty - encourage even distribution
        variables['soft_violations']['load_imbalance'] = model.NewIntVar(0, 100000, 'load_imbalance')
        if len(collab_ids) > 1:
            avg_load = total_duration // len(collab_ids)
            load_deviations = []
            
            for collab_id in collab_ids:
                load_var = variables['collaborator_loads'][collab_id]
                deviation_pos = model.NewIntVar(0, total_duration, f'dev_pos_{collab_id}')
                deviation_neg = model.NewIntVar(0, total_duration, f'dev_neg_{collab_id}')
                
                model.Add(deviation_pos >= load_var - avg_load)
                model.Add(deviation_neg >= avg_load - load_var)
                
                total_deviation = model.NewIntVar(0, total_duration, f'total_dev_{collab_id}')
                model.Add(total_deviation == deviation_pos + deviation_neg)
                load_deviations.append(total_deviation)
            
            model.Add(variables['soft_violations']['load_imbalance'] == sum(load_deviations))
        else:
            model.Add(variables['soft_violations']['load_imbalance'] == 0)
        
        # Absence and vacation constraints with updated horizon
        self._add_availability_constraints(model, variables, tasks, collaborators, collab_map, max_horizon * 2)
        
        return model, variables
    
    def _calculate_task_levels(self, tasks: List[Dict]) -> Dict[int, int]:
        """Calculate the dependency level of each task for better scheduling"""
        task_levels = {}
        task_map = {task["task_id"]: task for task in tasks}
        
        def get_level(task_id):
            if task_id in task_levels:
                return task_levels[task_id]
            
            task = task_map.get(task_id)
            if not task or not task.get("predecessoras"):
                task_levels[task_id] = 0
                return 0
            
            max_pred_level = 0
            for pred_id in task["predecessoras"]:
                if pred_id in task_map:
                    pred_level = get_level(pred_id)
                    max_pred_level = max(max_pred_level, pred_level)
            
            task_levels[task_id] = max_pred_level + 1
            return task_levels[task_id]
        
        for task in tasks:
            get_level(task["task_id"])
        
        return task_levels
    
    def _add_availability_constraints(self, model, variables, tasks, collaborators, collab_map, max_horizon):
        """Add constraints for collaborator availability with flexible handling"""
        
        # Collect vacation penalties for soft constraint handling
        vacation_penalties = []
        
        for task in tasks:
            task_id = task["task_id"]
            
            for collab_id in [c["id"] for c in collaborators]:
                collab = collab_map[collab_id]
                
                is_assigned = model.NewBoolVar(f'avail_check_{task_id}_{collab_id}')
                model.Add(variables['task_assignments'][task_id] == collab_id).OnlyEnforceIf(is_assigned)
                model.Add(variables['task_assignments'][task_id] != collab_id).OnlyEnforceIf(is_assigned.Not())
                
                # Work period constraints - now handled as hard constraints above
                # Only add soft penalties for edge cases or preferences
                if collab.get("inicio") is not None and collab["inicio"] > 0:
                    # This is now a hard constraint, so no soft penalty needed
                    pass
                
                if collab.get("termino") is not None and collab["termino"] < max_horizon:
                    # This is now a hard constraint, so no soft penalty needed
                    pass
                
                # Absence constraints (hard - cannot work during absences)
                ausencias = collab.get("ausencias", set())
                if ausencias:
                    for absence_day in ausencias:
                        if 0 <= absence_day < max_horizon:
                            # Task cannot overlap with absence day
                            # Either task ends before or equal to absence, or starts after absence
                            no_overlap_abs = model.NewBoolVar(f'no_abs_overlap_{task_id}_{collab_id}_{absence_day}')
                            
                            # Task ends before or at absence day OR task starts after absence day
                            ends_before = model.NewBoolVar(f'ends_before_abs_{task_id}_{collab_id}_{absence_day}')
                            model.Add(variables['task_ends'][task_id] <= absence_day).OnlyEnforceIf(ends_before)
                            model.Add(variables['task_ends'][task_id] > absence_day).OnlyEnforceIf(ends_before.Not())
                            
                            starts_after = model.NewBoolVar(f'starts_after_abs_{task_id}_{collab_id}_{absence_day}')
                            model.Add(variables['task_starts'][task_id] > absence_day).OnlyEnforceIf(starts_after)
                            model.Add(variables['task_starts'][task_id] <= absence_day).OnlyEnforceIf(starts_after.Not())
                            
                            # At least one must be true
                            model.AddBoolOr([ends_before, starts_after]).OnlyEnforceIf(is_assigned)
                
                # Vacation constraints (hard - cannot work during vacation periods)
                ferias_list = collab.get("ferias", [])
                for ferias_inicio, ferias_fim in ferias_list:
                    if 0 <= ferias_inicio < max_horizon and 0 <= ferias_fim < max_horizon:
                        # Task cannot overlap with vacation period
                        # Either task ends before vacation starts, or task starts after vacation ends
                        
                        # Task ends before or at vacation start OR task starts after or at vacation end
                        ends_before_vac = model.NewBoolVar(f'ends_before_vac_{task_id}_{collab_id}_{ferias_inicio}')
                        model.Add(variables['task_ends'][task_id] <= ferias_inicio).OnlyEnforceIf(ends_before_vac)
                        model.Add(variables['task_ends'][task_id] > ferias_inicio).OnlyEnforceIf(ends_before_vac.Not())
                        
                        starts_after_vac = model.NewBoolVar(f'starts_after_vac_{task_id}_{collab_id}_{ferias_inicio}')
                        model.Add(variables['task_starts'][task_id] >= ferias_fim).OnlyEnforceIf(starts_after_vac)
                        model.Add(variables['task_starts'][task_id] < ferias_fim).OnlyEnforceIf(starts_after_vac.Not())
                        
                        # At least one must be true when assigned to this collaborator
                        model.AddBoolOr([ends_before_vac, starts_after_vac]).OnlyEnforceIf(is_assigned)
        
        # Add vacation penalty variable
        variables['soft_violations']['vacation_penalty'] = model.NewIntVar(0, 200000, 'vacation_penalty')
        if vacation_penalties:
            model.Add(variables['soft_violations']['vacation_penalty'] == sum(vacation_penalties))
        else:
            model.Add(variables['soft_violations']['vacation_penalty'] == 0)
    
    def solve_cp_model(self, model: cp_model.CpModel, variables: Dict, 
                      tasks: List[Dict], project_start_dates: Dict[str, int] = None,
                      project_deadlines: Dict[str, int] = None) -> Tuple[Optional[List[int]], float, Dict, Optional['cp_model.CpSolver']]:
        """Solve the CP model with enhanced objective focusing on makespan and load balancing"""
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit_seconds
        solver.parameters.log_search_progress = True
        
        # Enhanced multi-objective optimization with project start date priority
        objective_terms = []
        
        # 1. Primary objective: Minimize makespan (highest priority)
        makespan_term = variables['makespan'] * self.makespan_weight
        objective_terms.append(makespan_term)
        
        # 2. Project start date constraints (HARD) - NEW IMPLEMENTATION
        # Transform project start dates from soft penalties to HARD constraints
        print("CP Model: Adding HARD constraints for project start dates...")
        
        for task in tasks:
            task_id = task["task_id"]
            project_name = task["projeto"]
            
            if project_start_dates and project_name in project_start_dates:
                min_start = project_start_dates[project_name]
                
                # HARD CONSTRAINT: Task cannot start before project's minimum start date
                print(f"Task {task_id} ({project_name}): Adding HARD project start constraint >= day {min_start}")
                model.Add(variables['task_starts'][task_id] >= min_start)
        
        # 3. Project deadline constraints (HARD) - NEW IMPLEMENTATION
        # Transform project deadlines from soft penalties to HARD constraints
        if project_deadlines:
            print("CP Model: Adding HARD constraints for project deadlines...")
            
            # Group tasks by project to find project end times
            projects = {}
            for task in tasks:
                proj_name = task["projeto"]
                if proj_name not in projects:
                    projects[proj_name] = []
                projects[proj_name].append(task)
            
            # Add hard deadline constraints for each project
            for proj_name, deadline_day in project_deadlines.items():
                if proj_name in projects:
                    project_tasks = projects[proj_name]
                    
                    print(f"Project '{proj_name}': Adding HARD deadline constraint <= day {deadline_day}")
                    
                    # HARD CONSTRAINT: All tasks in the project must end before or at the deadline
                    for task in project_tasks:
                        task_id = task["task_id"]
                        if task_id in variables['task_ends']:
                            model.Add(variables['task_ends'][task_id] <= deadline_day)
                            print(f"  Task {task_id} ({task['nome']}): must end <= day {deadline_day}")
        
        # Remove project start penalty since it's now a hard constraint
        project_start_penalty = model.NewIntVar(0, 0, 'project_start_penalty')
        model.Add(project_start_penalty == 0)
        objective_terms.append(project_start_penalty)
        
        # Remove project deadline penalty since it's now a hard constraint
        project_deadline_penalty = model.NewIntVar(0, 0, 'project_deadline_penalty')
        model.Add(project_deadline_penalty == 0)
        objective_terms.append(project_deadline_penalty)
        
        # 4. Load balancing: Minimize workload imbalance (high priority)
        load_balance_term = variables['soft_violations']['load_imbalance'] * self.load_balancing_weight
        objective_terms.append(load_balance_term)
        
        # 5. Vacation penalties (only soft constraint remaining for skills/positions)
        # Note: Skills and positions are now HARD constraints, so no penalties needed
        vacation_term = variables['soft_violations']['vacation_penalty']
        objective_terms.append(vacation_term)
        
        # 6. Parallelization bonus (encourage parallel execution)
        for level, parallel_var in variables.get('parallelization_vars', {}).items():
            # Subtract bonus (negative term to encourage parallelization)
            objective_terms.append(-parallel_var)
        
        # Set the objective
        model.Minimize(sum(objective_terms))
        
        # Add search hints for better performance
        self._add_search_hints(model, variables, tasks)
        
        # Solve with enhanced parameters
        solver.parameters.num_search_workers = 4  # Use multiple threads
        solver.parameters.cp_model_presolve = True
        solver.parameters.cp_model_probing_level = 2
        
        # Validate model before solving
        print("CP Solver: Validating model...")
        try:
            # Check if model is valid
            model_proto = model.Proto()
            print(f"CP Model stats: {len(model_proto.variables)} variables, {len(model_proto.constraints)} constraints")
            
            # Validate variable domains
            invalid_vars = []
            for i, var in enumerate(model_proto.variables):
                if not var.domain:
                    invalid_vars.append(f"var #{i}: {var.name}")
            
            if invalid_vars:
                print(f"ERROR: Found {len(invalid_vars)} variables with no domain:")
                for var_info in invalid_vars[:10]:  # Show first 10
                    print(f"  - {var_info}")
                raise ValueError(f"Model has {len(invalid_vars)} variables with invalid domains")
            
        except Exception as e:
            print(f"Model validation error: {e}")
            return None, sanitize_for_json(999999999), {
                'status': 'MODEL_INVALID',
                'error': str(e),
                'solve_time': 0,
                'num_branches': 0,
                'num_conflicts': 0
            }, None
        
        print("CP Solver: Starting solve...")
        status = solver.Solve(model)
        print(f"CP Solver: Finished with status {status}")
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            # Extract solution
            solution = []
            for task in tasks:
                task_id = task["task_id"]
                assigned_collab = solver.Value(variables['task_assignments'][task_id])
                solution.append(assigned_collab)
            
            makespan = solver.Value(variables['makespan'])
            skill_penalty = solver.Value(variables['soft_violations']['skill_penalty'])
            position_penalty = solver.Value(variables['soft_violations']['position_penalty'])
            load_imbalance = solver.Value(variables['soft_violations']['load_imbalance'])
            vacation_penalty = solver.Value(variables['soft_violations']['vacation_penalty'])
            
            # Calculate fitness similar to GA for comparison
            fitness = sanitize_for_json(makespan * self.makespan_weight + 
                      skill_penalty + position_penalty + 
                      load_imbalance * self.load_balancing_weight + 
                      vacation_penalty)
            
            # Collect detailed solve information
            solve_info = {
                'status': 'OPTIMAL' if status == cp_model.OPTIMAL else 'FEASIBLE',
                'makespan': makespan,
                'skill_penalty': skill_penalty,
                'position_penalty': position_penalty,
                'load_imbalance': load_imbalance,
                'vacation_penalty': vacation_penalty,
                'solve_time': solver.WallTime(),
                'objective_value': solver.ObjectiveValue(),
                'num_branches': solver.NumBranches(),
                'num_conflicts': solver.NumConflicts(),
                'collaborator_loads': {}
            }
            
            # Extract collaborator workloads
            for collab_id in variables['collaborator_loads']:
                load_value = solver.Value(variables['collaborator_loads'][collab_id])
                solve_info['collaborator_loads'][collab_id] = load_value
            
            return solution, fitness, solve_info, solver
        else:
            status_name = {
                cp_model.INFEASIBLE: 'INFEASIBLE',
                cp_model.MODEL_INVALID: 'MODEL_INVALID', 
                cp_model.UNKNOWN: 'UNKNOWN'
            }.get(status, f'STATUS_{status}')
            
            print(f"CP Solver failed with status: {status_name}")
            
            return None, sanitize_for_json(999999999), {
                'status': status_name,
                'solve_time': solver.WallTime(),
                'num_branches': solver.NumBranches(),
                'num_conflicts': solver.NumConflicts(),
                'error': f'Solver returned {status_name}'
            }, None
    
    def _add_search_hints(self, model: cp_model.CpModel, variables: Dict, tasks: List[Dict]):
        """Add search hints to guide the solver towards better solutions"""
        
        # Hint 1: Assign tasks to collaborators with matching skills first
        for task in tasks:
            task_id = task["task_id"]
            required_skills = task["habilidades_necessarias"]
            required_position = task["cargo_necessario"]
            
            # Find best matching collaborator
            best_collab = None
            best_score = -1
            
            for collab_id in variables['collaborator_loads'].keys():
                # This would need collaborator data - simplified for now
                pass
        
        # Hint 2: Start tasks as early as possible (greedy approach)
        for task in tasks:
            task_id = task["task_id"]
            if task_id in variables['task_starts']:
                # Hint to start early if no dependencies
                if not task.get("predecessoras"):
                    model.AddHint(variables['task_starts'][task_id], 0)
    
    async def run_with_progress(self, tasks: List[Dict], collaborators: List[Dict], 
                               project_deadlines: Dict[str, int] = None,
                               project_start_dates: Dict[str, int] = None) -> AsyncGenerator[Dict, None]:
        """Run CP algorithm with progress updates"""
        
        try:
            yield {
                "type": "progress",
                "generation": 1,
                "total_generations": 1,
                "best_fitness": 999999999,
                "progress_percent": 10,
                "message": "Criando modelo CP-SAT..."
            }
            await asyncio.sleep(0.1)
            
            # Create model
            model, variables = self.create_cp_model(tasks, collaborators, project_deadlines, project_start_dates)
            
            yield {
                "type": "progress", 
                "generation": 1,
                "total_generations": 1,
                "best_fitness": 999999999,
                "progress_percent": 30,
                "message": "Resolvendo com CP-SAT..."
            }
            await asyncio.sleep(0.1)
            
            # Solve model
            solution, fitness, solve_info, solver = self.solve_cp_model(model, variables, tasks, project_start_dates, project_deadlines)
            
            if solution is not None:
                # Evaluate with standard evaluator for consistency
                eval_fitness, penalties, violations = self.evaluator.evaluate(
                    solution, tasks, collaborators, project_deadlines, project_start_dates
                )
                
                # Ensure fitness is a valid number
                eval_fitness = sanitize_for_json(eval_fitness)
                
                yield {
                    "type": "progress",
                    "generation": 1,
                    "total_generations": 1, 
                    "best_fitness": eval_fitness,
                    "progress_percent": 90,
                    "message": f"Solução encontrada ({solve_info.get('status', 'UNKNOWN')})"
                }
                await asyncio.sleep(0.1)
                
                # Store solver and variables for internal use
                self._last_solver = solver
                self._last_variables = variables
                
                yield {
                    "type": "complete",
                    "best_solution": solution,
                    "best_fitness": eval_fitness,
                    "best_penalties": penalties,
                    "best_violations": violations,
                    "solve_info": solve_info
                }
            else:
                # Clear internal state on failure
                self._last_solver = None
                self._last_variables = None
                
                yield {
                    "type": "complete",
                    "best_solution": None,
                    "best_fitness": sanitize_for_json(999999999),
                    "best_penalties": {},
                    "best_violations": {},
                    "solve_info": solve_info,
                    "error": f"Nenhuma solução encontrada ({solve_info.get('status', 'UNKNOWN')})"
                }
                
        except Exception as e:
            # Clear internal state on error
            self._last_solver = None
            self._last_variables = None
            
            yield {
                "type": "complete",
                "best_solution": None,
                "best_fitness": sanitize_for_json(999999999),
                "best_penalties": {},
                "best_violations": {},
                "solve_info": {"status": "ERROR", "solve_time": 0},
                "error": f"Erro na execução do CP: {str(e)}"
            }
    
    def run(self, tasks: List[Dict], collaborators: List[Dict], 
           project_deadlines: Dict[str, int] = None,
           project_start_dates: Dict[str, int] = None) -> Tuple[List[int], float, List[float], Dict, Dict, Optional['cp_model.CpSolver'], Dict]:
        """Run CP algorithm (synchronous version)"""
        
        try:
            # Create and solve model
            model, variables = self.create_cp_model(tasks, collaborators, project_deadlines, project_start_dates)
            solution, fitness, solve_info, solver = self.solve_cp_model(model, variables, tasks, project_start_dates, project_deadlines)
            
            if solution is not None:
                # Evaluate with standard evaluator for consistency
                eval_fitness, penalties, violations = self.evaluator.evaluate(
                    solution, tasks, collaborators, project_deadlines, project_start_dates
                )
                
                # Ensure fitness is a valid number
                eval_fitness = sanitize_for_json(eval_fitness)
                
                # CP doesn't have generations, so return single fitness value
                fitness_history = [eval_fitness]
                
                return solution, eval_fitness, fitness_history, penalties, violations, solver, variables
            else:
                return [], sanitize_for_json(999999999), [sanitize_for_json(999999999)], {}, {}, None, {}
                
        except Exception as e:
            print(f"Erro no CP: {e}")
            import traceback
            traceback.print_exc()
            return [], sanitize_for_json(999999999), [sanitize_for_json(999999999)], {}, {}, None, {}