from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
import datetime
import math
from typing import List, Dict, Any
from models import *
from services.cp_service import CPService
from utils.config import lifespan, settings
from db.database import get_db
from db import crud
from db import schemas

def sanitize_for_json(obj):
    """Sanitize object to be JSON serializable"""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isinf(obj) or math.isnan(obj):
            return 999999999
        return obj
    else:
        return obj

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

cp_service = CPService()

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

# CRUD Tribos
@app.get("/api/tribos", response_model=List[schemas.Tribo])
async def get_tribos(db: Session = Depends(get_db)):
    return crud.get_tribos(db)

@app.post("/api/tribos", response_model=schemas.Tribo)
async def create_tribo(tribo: schemas.TriboCreate, db: Session = Depends(get_db)):
    return crud.create_tribo(db, tribo)

@app.put("/api/tribos/{tribo_id}", response_model=schemas.Tribo)
async def update_tribo(tribo_id: int, tribo: schemas.TriboCreate, db: Session = Depends(get_db)):
    updated_tribo = crud.update_tribo(db, tribo_id, tribo)
    if not updated_tribo:
        raise HTTPException(status_code=404, detail="Tribo não encontrada")
    return updated_tribo

@app.delete("/api/tribos/{tribo_id}")
async def delete_tribo(tribo_id: int, db: Session = Depends(get_db)):
    result = crud.delete_tribo(db, tribo_id)
    if result == "in_use":
        raise HTTPException(status_code=400, detail="Não é possível excluir esta tribo pois ela está sendo utilizada por squads")
    elif not result:
        raise HTTPException(status_code=404, detail="Tribo não encontrada")
    return {"message": "Tribo deletada com sucesso"}

# CRUD Squads
@app.get("/api/squads", response_model=List[schemas.Squad])
async def get_squads(tribo_id: int = None, db: Session = Depends(get_db)):
    if tribo_id:
        return crud.get_squads_by_tribo(db, tribo_id)
    return crud.get_squads(db)

@app.post("/api/squads", response_model=schemas.Squad)
async def create_squad(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    return crud.create_squad(db, squad)

@app.put("/api/squads/{squad_id}", response_model=schemas.Squad)
async def update_squad(squad_id: int, squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    updated_squad = crud.update_squad(db, squad_id, squad)
    if not updated_squad:
        raise HTTPException(status_code=404, detail="Squad não encontrada")
    return updated_squad

@app.delete("/api/squads/{squad_id}")
async def delete_squad(squad_id: int, db: Session = Depends(get_db)):
    result = crud.delete_squad(db, squad_id)
    if result == "in_use":
        raise HTTPException(status_code=400, detail="Não é possível excluir esta squad pois ela está sendo utilizada por colaboradores")
    elif not result:
        raise HTTPException(status_code=404, detail="Squad não encontrada")
    return {"message": "Squad deletada com sucesso"}

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



@app.post("/api/executar-cp-stream")
async def executar_cp_stream(params: AlgoritmoParams, db: Session = Depends(get_db)):
    async def event_generator():
        try:
            async for event in cp_service.execute_algorithm_stream(
                {
                    "ref_date": params.ref_date,
                    "time_limit_seconds": getattr(params, 'time_limit_seconds', 300),
                    "makespan_weight": getattr(params, 'makespan_weight', 150),
                    "projeto_ids": params.projeto_ids,
                    "colaborador_ids": params.colaborador_ids,
                    "simulated_members": [m.dict() for m in params.simulated_members] if params.simulated_members else []
                },
                db
            ):
                # Sanitize event before JSON serialization
                sanitized_event = sanitize_for_json(event)
                yield f"data: {json.dumps(sanitized_event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/executar-cp")
async def executar_cp(params: AlgoritmoParams, db: Session = Depends(get_db)):
    try:
        result = cp_service.execute_algorithm({
            "ref_date": params.ref_date,
            "time_limit_seconds": getattr(params, 'time_limit_seconds', 300),
            "makespan_weight": getattr(params, 'makespan_weight', 150),
            "projeto_ids": params.projeto_ids,
            "colaborador_ids": params.colaborador_ids,
            "simulated_members": [m.dict() for m in params.simulated_members] if params.simulated_members else []
        }, db)
        
        return ResultadoAlgoritmo(
            tarefas=result["tarefas"],
            melhor_fitness=result["melhor_fitness"],
            historico_fitness=result["historico_fitness"],
            penalidades=result["penalidades"],
            ocorrencias_penalidades=result["ocorrencias_penalidades"]
        )
        
    except Exception as e:
        import traceback
        print(f"Error in executar_cp: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/api/resultados-salvos", response_model=schemas.ResultadoSalvo)
async def salvar_resultado(resultado: schemas.ResultadoSalvoCreate, db: Session = Depends(get_db)):
    return crud.create_resultado_salvo(db, resultado)

@app.get("/api/resultados-salvos", response_model=List[schemas.ResultadoSalvo])
async def listar_resultados_salvos(squad_id: int = None, ano: int = None, db: Session = Depends(get_db)):
    return crud.get_resultados_salvos(db, squad_id, ano)

@app.get("/api/resultados-salvos/{resultado_id}", response_model=schemas.ResultadoSalvo)
async def obter_resultado_salvo(resultado_id: int, db: Session = Depends(get_db)):
    resultado = crud.get_resultado_salvo(db, resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    return resultado

@app.delete("/api/resultados-salvos/{resultado_id}")
async def deletar_resultado_salvo(resultado_id: int, db: Session = Depends(get_db)):
    if not crud.delete_resultado_salvo(db, resultado_id):
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    return {"message": "Resultado deletado com sucesso"}

# CRUD Periodos Roadmaps
@app.get("/api/periodos-roadmaps", response_model=List[schemas.PeriodoRoadmap])
async def get_periodos_roadmaps(db: Session = Depends(get_db)):
    return crud.get_periodos_roadmaps(db)

@app.post("/api/periodos-roadmaps", response_model=schemas.PeriodoRoadmap)
async def create_periodo_roadmap(periodo: schemas.PeriodoRoadmapCreate, db: Session = Depends(get_db)):
    return crud.create_periodo_roadmap(db, periodo)

@app.put("/api/periodos-roadmaps/{periodo_id}", response_model=schemas.PeriodoRoadmap)
async def update_periodo_roadmap(periodo_id: int, periodo: schemas.PeriodoRoadmapCreate, db: Session = Depends(get_db)):
    updated_periodo = crud.update_periodo_roadmap(db, periodo_id, periodo)
    if not updated_periodo:
        raise HTTPException(status_code=404, detail="Período não encontrado")
    return updated_periodo

@app.delete("/api/periodos-roadmaps/{periodo_id}")
async def delete_periodo_roadmap(periodo_id: int, db: Session = Depends(get_db)):
    if not crud.delete_periodo_roadmap(db, periodo_id):
        raise HTTPException(status_code=404, detail="Período não encontrado")
    return {"message": "Período deletado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
