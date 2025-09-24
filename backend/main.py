from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import datetime
from typing import List
from models import *
from genetic_algorithm import GeneticAlgorithm, Utils

app = FastAPI(title="Resource Allocation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ga = GeneticAlgorithm()

def load_data():
    with open("data/colaborators.json", "r") as f:
        colaboradores = json.load(f)
    with open("data/projects.json", "r") as f:
        projetos = json.load(f)
    return colaboradores, projetos

def convert_ausencias(colaboradores: List[dict], ref_date: datetime.date):
    for colab in colaboradores:
        ausencias_convertidas = []
        for data_str in colab["ausencias"]:
            dia_int = Utils.date_to_int(data_str, ref_date)
            ausencias_convertidas.append(dia_int)
        colab["ausencias"] = ausencias_convertidas
    return colaboradores

def montar_tarefas_globais(projetos: List[dict]):
    tarefas_globais = []
    for proj in projetos:
        etapas_ordenadas = sorted(proj["etapas"], key=lambda e: e["id"])
        for etapa in etapas_ordenadas:
            tarefas_globais.append({
                "projeto": proj["nome"],
                "task_id": etapa["id"],
                "nome": etapa["nome"],
                "duracao_dias": etapa["duracao_dias"],
                "habilidades_necessarias": set(etapa["habilidades_necessarias"]),
                "cargo_necessario": etapa["cargo_necessario"],
            })
    return tarefas_globais

@app.get("/api/colaboradores")
async def get_colaboradores():
    colaboradores, _ = load_data()
    return colaboradores

@app.get("/api/projetos")
async def get_projetos():
    _, projetos = load_data()
    return projetos

@app.post("/api/executar-algoritmo")
async def executar_algoritmo(params: AlgoritmoParams):
    try:
        colaboradores, projetos = load_data()
        ref_date = datetime.datetime.strptime(params.ref_date, "%Y-%m-%d").date()
        
        colaboradores = convert_ausencias(colaboradores, ref_date)
        tarefas_globais = montar_tarefas_globais(projetos)
        
        best_ind, best_val, hist_fit, detalhes_penalidades, ocorrencias_penalidades = ga.algoritmo_genetico(
            params.tam_pop, params.n_gen, params.pc, params.pm, tarefas_globais, colaboradores
        )
        
        # Reconstrói cronograma
        project_end = {}
        rows = []
        
        for i, tsk in enumerate(tarefas_globais):
            cid = best_ind[i]
            colab = next(c for c in colaboradores if c["id"] == cid)
            duracao = tsk["duracao_dias"]

            fim_colab = max([r["fim_dias"] + 1 for r in rows if r["colaborador"] == colab["nome"]] or [0])
            fim_proj = project_end.get(tsk["projeto"], 0)

            start = max(fim_colab, fim_proj)
            while start in colab["ausencias"] or (ref_date + datetime.timedelta(days=start)).weekday() >= 5:
                start += 1

            end = start
            duracao_restante = duracao
            while duracao_restante > 0:
                if end not in colab["ausencias"] and (ref_date + datetime.timedelta(days=end)).weekday() < 5:
                    duracao_restante -= 1
                end += 1

            project_end[tsk["projeto"]] = end

            start_date = (ref_date + datetime.timedelta(days=start)).strftime("%d/%m/%Y")
            end_date = (ref_date + datetime.timedelta(days=end - 1)).strftime("%d/%m/%Y")

            rows.append({
                "projeto": tsk["projeto"],
                "nome_tarefa": tsk["nome"],
                "inicio_dias": start,
                "data_inicio": start_date,
                "fim_dias": end - 1,
                "data_fim": end_date,
                "colaborador": colab["nome"],
                "duracao_dias": duracao,
            })

        return ResultadoAlgoritmo(
            tarefas=rows,
            melhor_fitness=best_val,
            historico_fitness=hist_fit,
            penalidades=detalhes_penalidades,
            ocorrencias_penalidades=ocorrencias_penalidades
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)