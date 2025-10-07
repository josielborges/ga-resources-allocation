# Resource Allocation System - Development Guide

## System Overview
Hybrid optimization system using **Genetic Algorithm (GA)** and **Ant Colony Optimization (ACO)** for Resource-Constrained Project Scheduling Problem (RCPSP). Allocates workers to project tasks based on skills, positions, availability, and dependencies.

## Tech Stack
- **Backend**: FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Frontend**: Vue.js + Element Plus + Chart.js + FullCalendar
- **Database**: PostgreSQL (localhost:5439)
- **Algorithms**: GA and ACO for optimization

## Architecture

### Core Algorithm Components
- `genetic_algorithm.py`: Evolutionary optimization (tournament selection, crossover, mutation)
- `ant_colony_optimization.py`: Pheromone-based optimization with local search
- `algorithm/evaluator.py`: Fitness calculation with multi-constraint penalties
- `algorithm/scheduler.py`: Task timing with predecessor constraints
- `algorithm/constraints.py`: Validation and penalty calculation

### Services Layer
- `services/algorithm_service.py`: GA execution wrapper
- `services/aco_service.py`: ACO execution wrapper
- Both load DB data, convert formats, build task lists, execute algorithms

### Database Schema
**Tables**: cargos, habilidades, colaboradores, ausencias, projetos, etapas
**Associations**: colaborador_habilidade, etapa_habilidade, etapa_predecessora

**Key Relationships**:
- Skills belong to positions (cargo_id FK)
- Workers have position + multiple skills
- Tasks require position + multiple skills + predecessors (DAG)
- Absences block worker availability

## Development Rules

### When Modifying Algorithms
1. **Fitness penalties** are in `algorithm/constraints.py` - adjust weights there
2. **Task ordering** logic is in service layer `build_global_tasks()` methods
3. **Never break predecessor constraints** - tasks must respect dependencies
4. **Maintain DAG structure** - no circular dependencies in etapa_predecessora

### When Modifying Database
1. **Always create Alembic migration** for schema changes
2. **Use CASCADE RESTRICT** on FKs to prevent orphaned data
3. **Update both models.py and schemas.py** for consistency
4. **Test CRUD operations** after schema changes

### When Adding Features
1. **Service layer** handles data transformation (DB ↔ Algorithm format)
2. **Evaluator** calculates fitness - add new penalties there
3. **Scheduler** handles timing - modify for new scheduling rules
4. **Keep algorithms pure** - no DB access in GA/ACO classes

### Constraint Penalties (Current Values)
- Missing skills: 10,000
- Wrong position: 10,000
- Collaborator overlap: 2,000
- Absence conflict: 500
- Resource idle time: 100/day
- Project gaps: 50/day
- Makespan weight: 150-200

### Algorithm Parameters
**GA**: pop_size, generations, crossover_prob, mutation_prob (0.15)
**ACO**: num_ants, iterations, alpha (1.0), beta (2.0), rho (0.5), q0 (0.9)

### Data Flow
Database → CRUD → Service → Algorithm → Schedule → API → Frontend

### Testing Algorithms
1. Use `/api/executar-algoritmo` for GA
2. Use `/api/executar-aco` for ACO
3. Use `/api/comparar-algoritmos` for comparison
4. Check fitness_history for convergence
5. Validate no constraint violations in results

### Common Pitfalls
- Don't modify task order without considering predecessors
- Don't delete cargos/habilidades in use (RESTRICT prevents this)
- Don't forget to convert absence dates to integer days
- Don't create circular dependencies in etapa_predecessora
- Always refresh DB objects after commit

### File Locations
- Migrations: `backend/db/alembic/versions/`
- Models: `backend/db/models.py`
- Schemas: `backend/db/schemas.py`
- CRUD: `backend/db/crud.py`
- Config: `backend/.env`
