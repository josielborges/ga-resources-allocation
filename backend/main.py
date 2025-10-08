from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import json
import datetime
from typing import List
from models import *
from services.algorithm_service import AlgorithmService
from services.aco_service import ACOService
from algorithm_comparison import AlgorithmComparison
from utils.config import lifespan, settings
from db.database import get_db
from db import crud
from db import schemas

app = FastAPI(title="Resource Allocation API",
              openapi_url=settings.OPENAPI_URL,
              docs_url=settings.SWAGGER_URL,
              redoc_url=settings.REDOC_URL,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

algorithm_service = AlgorithmService()
aco_service = ACOService()
comparison_service = AlgorithmComparison()

def load_data():
    with open("data/colaborators.json", "r") as f:
        colaboradores = json.load(f)
    with open("data/projects.json", "r") as f:
        projetos = json.load(f)
    return colaboradores, projetos

@app.get("/api/colaboradores", response_model=List[schemas.Colaborador])
async def get_colaboradores_db(db: Session = Depends(get_db)):
    return crud.get_colaboradores(db)

@app.get("/api/projetos", response_model=List[schemas.Projeto])
async def get_projetos_db(db: Session = Depends(get_db)):
    return crud.get_projetos(db)

@app.get("/api/projetos/{projeto_id}", response_model=schemas.Projeto)
async def get_projeto(projeto_id: int, db: Session = Depends(get_db)):
    projeto = crud.get_projeto(db, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto

@app.post("/api/projetos", response_model=schemas.Projeto)
async def create_projeto(projeto: schemas.ProjetoCreate, db: Session = Depends(get_db)):
    return crud.create_projeto(db, projeto)

@app.put("/api/projetos/{projeto_id}", response_model=schemas.Projeto)
async def update_projeto(projeto_id: int, projeto: schemas.ProjetoCreate, db: Session = Depends(get_db)):
    updated_projeto = crud.update_projeto(db, projeto_id, projeto)
    if not updated_projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return updated_projeto

@app.delete("/api/projetos/{projeto_id}")
async def delete_projeto(projeto_id: int, db: Session = Depends(get_db)):
    if not crud.delete_projeto(db, projeto_id):
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return {"message": "Projeto deletado com sucesso"}

@app.get("/api/colaboradores/json")
async def get_colaboradores():
    colaboradores, _ = load_data()
    return colaboradores

@app.get("/api/projetos/json")
async def get_projetos():
    _, projetos = load_data()
    return projetos

@app.get("/api/habilidades", response_model=List[schemas.Habilidade])
async def get_habilidades(cargo_id: int = None, db: Session = Depends(get_db)):
    if cargo_id:
        return crud.get_habilidades_by_cargo(db, cargo_id)
    return crud.get_habilidades(db)

@app.get("/api/cargos", response_model=List[schemas.Cargo])
async def get_cargos(db: Session = Depends(get_db)):
    return crud.get_cargos(db)

@app.get("/api/etapas", response_model=List[schemas.Etapa])
async def get_etapas(db: Session = Depends(get_db)):
    return crud.get_etapas(db)

# CRUD Habilidades
@app.post("/api/habilidades", response_model=schemas.Habilidade)
async def create_habilidade(habilidade: schemas.HabilidadeCreate, db: Session = Depends(get_db)):
    return crud.create_habilidade(db, habilidade)

@app.put("/api/habilidades/{habilidade_id}", response_model=schemas.Habilidade)
async def update_habilidade(habilidade_id: int, habilidade: schemas.HabilidadeCreate, db: Session = Depends(get_db)):
    updated_habilidade = crud.update_habilidade(db, habilidade_id, habilidade)
    if not updated_habilidade:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    return updated_habilidade

@app.delete("/api/habilidades/{habilidade_id}")
async def delete_habilidade(habilidade_id: int, db: Session = Depends(get_db)):
    result = crud.delete_habilidade(db, habilidade_id)
    if result == "in_use":
        raise HTTPException(status_code=400, detail="Não é possível excluir esta habilidade pois ela está sendo utilizada por colaboradores ou projetos")
    elif not result:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    return {"message": "Habilidade deletada com sucesso"}

# CRUD Cargos
@app.post("/api/cargos", response_model=schemas.Cargo)
async def create_cargo(cargo: schemas.CargoCreate, db: Session = Depends(get_db)):
    return crud.create_cargo(db, cargo)

@app.put("/api/cargos/{cargo_id}", response_model=schemas.Cargo)
async def update_cargo(cargo_id: int, cargo: schemas.CargoCreate, db: Session = Depends(get_db)):
    updated_cargo = crud.update_cargo(db, cargo_id, cargo)
    if not updated_cargo:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return updated_cargo

@app.delete("/api/cargos/{cargo_id}")
async def delete_cargo(cargo_id: int, db: Session = Depends(get_db)):
    result = crud.delete_cargo(db, cargo_id)
    if result == "in_use":
        raise HTTPException(status_code=400, detail="Não é possível excluir este cargo pois ele está sendo utilizado por colaboradores ou projetos")
    elif not result:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")
    return {"message": "Cargo deletado com sucesso"}

# CRUD Colaboradores
@app.post("/api/colaboradores", response_model=schemas.Colaborador)
async def create_colaborador(colaborador: schemas.ColaboradorCreate, db: Session = Depends(get_db)):
    return crud.create_colaborador(db, colaborador)

@app.put("/api/colaboradores/{colaborador_id}", response_model=schemas.Colaborador)
async def update_colaborador(colaborador_id: int, colaborador: schemas.ColaboradorCreate, db: Session = Depends(get_db)):
    updated_colaborador = crud.update_colaborador(db, colaborador_id, colaborador)
    if not updated_colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return updated_colaborador

@app.delete("/api/colaboradores/{colaborador_id}")
async def delete_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    if not crud.delete_colaborador(db, colaborador_id):
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return {"message": "Colaborador deletado com sucesso"}

@app.post("/api/executar-algoritmo")
async def executar_algoritmo(params: AlgoritmoParams, db: Session = Depends(get_db)):
    try:
        result = algorithm_service.execute_algorithm({
            "ref_date": params.ref_date,
            "tam_pop": params.tam_pop,
            "n_gen": params.n_gen,
            "pc": params.pc,
            "pm": params.pm,
            "projeto_ids": params.projeto_ids,
            "colaborador_ids": params.colaborador_ids
        }, db)
        
        return ResultadoAlgoritmo(
            tarefas=result["tarefas"],
            melhor_fitness=result["melhor_fitness"],
            historico_fitness=result["historico_fitness"],
            penalidades=result["penalidades"],
            ocorrencias_penalidades=result["ocorrencias_penalidades"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/executar-aco")
async def executar_aco(params: AlgoritmoParams, db: Session = Depends(get_db)):
    try:
        result = aco_service.execute_algorithm({
            "ref_date": params.ref_date,
            "tam_pop": params.tam_pop,
            "n_gen": params.n_gen,
            "pc": params.pc,
            "pm": params.pm,
            "projeto_ids": params.projeto_ids,
            "colaborador_ids": params.colaborador_ids
        }, db)
        
        return ResultadoAlgoritmo(
            tarefas=result["tarefas"],
            melhor_fitness=result["melhor_fitness"],
            historico_fitness=result["historico_fitness"],
            penalidades=result["penalidades"],
            ocorrencias_penalidades=result["ocorrencias_penalidades"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/comparar-algoritmos")
async def comparar_algoritmos(request: dict, db: Session = Depends(get_db)):
    try:
        colaboradores, projetos = aco_service.load_data_from_db(db)
        ref_date = datetime.datetime.strptime(request["ref_date"], "%Y-%m-%d").date()
        
        colaboradores = aco_service.convert_absences(colaboradores, ref_date)
        tarefas_globais = aco_service.build_global_tasks(projetos)
        
        ga_params = request.get("ga_params", {})
        aco_params = request.get("aco_params", {})
        
        comparison_result = comparison_service.run_comparison(
            tarefas_globais, colaboradores, ga_params, aco_params, runs=3
        )
        
        return comparison_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)