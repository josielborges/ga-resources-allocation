import datetime
import random
from typing import List, Dict, Tuple

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
    @staticmethod
    def criar_individuo(num_tarefas: int, lista_colab_ids: list) -> list:
        return [random.choice(lista_colab_ids) for _ in range(num_tarefas)]

    @staticmethod
    def populacao_inicial(tam_pop: int, num_tarefas: int, lista_colab_ids: list) -> list:
        return [
            GeneticAlgorithm.criar_individuo(num_tarefas, lista_colab_ids)
            for _ in range(tam_pop)
        ]

    @staticmethod
    def avaliar(individuo: list, tarefas_globais: list, colaboradores: list, peso_makespan: int = 200) -> tuple:
        alocacoes = {col["id"]: [] for col in colaboradores}
        fim_projeto = {t["projeto"]: 0 for t in tarefas_globais}
        intervalos_projetos = {t["projeto"]: [] for t in tarefas_globais}

        penalidades = {
            "habilidades_incorretas": 0,
            "cargo_incorreto": 0,
            "ausencias": 0,
            "sobreposicoes_colaborador": 0,
            "sobreposicoes_projeto": 0
        }

        ocorrencias_penalidades = {
            "habilidades_incorretas": [],
            "cargo_incorreto": [],
            "ausencias": [],
            "sobreposicoes_colaborador": [],
            "sobreposicoes_projeto": [],
        }

        makespan = 0

        for i, tarefa in enumerate(tarefas_globais):
            cid = individuo[i]
            colab = next(c for c in colaboradores if c["id"] == cid)

            if not tarefa["habilidades_necessarias"].issubset(colab["habilidades"]):
                penalidades["habilidades_incorretas"] += 10_000
                ocorrencias_penalidades["habilidades_incorretas"].append({
                    "projeto": tarefa["projeto"],
                    "tarefa": tarefa["nome"],
                    "colaborador": colab["nome"],
                    "habilidades_necessarias": ", ".join(tarefa["habilidades_necessarias"]),
                    "habilidades_colaborador": ", ".join(colab["habilidades"])
                })

            if tarefa["cargo_necessario"] != colab["cargo"]:
                penalidades["cargo_incorreto"] += 10_000
                ocorrencias_penalidades["cargo_incorreto"].append({
                    "projeto": tarefa["projeto"],
                    "tarefa": tarefa["nome"],
                    "colaborador": colab["nome"],
                    "cargo_necessario": tarefa["cargo_necessario"],
                    "cargo_colaborador": colab["cargo"]
                })

            proj_atual = tarefa["projeto"]
            ultimo_fim_proj = fim_projeto[proj_atual]
            ultimo_fim_colab = max(e for (_, e) in alocacoes[cid]) if alocacoes[cid] else 0

            inicio_tarefa = max(ultimo_fim_proj, ultimo_fim_colab)
            while inicio_tarefa in colab["ausencias"]:
                inicio_tarefa += 1

            fim_tarefa = inicio_tarefa
            duracao_restante = tarefa["duracao_dias"]
            while duracao_restante > 0:
                if fim_tarefa not in colab["ausencias"]:
                    duracao_restante -= 1
                fim_tarefa += 1

            for dia in range(inicio_tarefa, fim_tarefa):
                if dia in colab["ausencias"]:
                    penalidades["ausencias"] += 500
                    break

            fim_projeto[proj_atual] = fim_tarefa
            alocacoes[cid].append((inicio_tarefa, fim_tarefa))
            intervalos_projetos[proj_atual].append((inicio_tarefa, fim_tarefa))

            if fim_tarefa > makespan:
                makespan = fim_tarefa

        # Penalizar sobreposições
        for cid, intervals in alocacoes.items():
            intervals_sorted = sorted(intervals, key=lambda x: x[0])
            for i1 in range(len(intervals_sorted)):
                for i2 in range(i1 + 1, len(intervals_sorted)):
                    s1, e1 = intervals_sorted[i1]
                    s2, e2 = intervals_sorted[i2]
                    if (s1 < e2) and (s2 < e1):
                        penalidades["sobreposicoes_colaborador"] += 2000

        penalidades["makespan"] = makespan * peso_makespan
        fitness = sum(penalidades.values())

        return fitness, penalidades, ocorrencias_penalidades

    @staticmethod
    def torneio(populacao: list, fitnesses: list, k: int = 3) -> int:
        indices = random.sample(range(len(populacao)), k)
        best_idx = indices[0]
        best_fit = fitnesses[best_idx]
        for idx in indices[1:]:
            if fitnesses[idx] < best_fit:
                best_fit = fitnesses[idx]
                best_idx = idx
        return best_idx

    @staticmethod
    def crossover(ind1: list, ind2: list) -> tuple:
        size = len(ind1)
        if size < 2:
            return ind1[:], ind2[:]
        cx = random.randint(1, size - 1)
        f1 = ind1[:cx] + ind2[cx:]
        f2 = ind2[:cx] + ind1[cx:]
        return f1, f2

    @staticmethod
    def mutacao(individuo: list, lista_colab_ids: list, taxa_mut: float = 0.1) -> list:
        for i in range(len(individuo)):
            if random.random() < taxa_mut:
                individuo[i] = random.choice(lista_colab_ids)
        return individuo

    def algoritmo_genetico(self, tam_pop: int, n_gen: int, pc: float, pm: float, 
                          tarefas_globais: list, colaboradores: list) -> tuple:
        num_t = len(tarefas_globais)
        colab_ids = [c["id"] for c in colaboradores]

        pop = self.populacao_inicial(tam_pop, num_t, colab_ids)
        fits_and_penalties = [self.avaliar(ind, tarefas_globais, colaboradores) for ind in pop]
        fits = [item[0] for item in fits_and_penalties]
        penalties = [item[1] for item in fits_and_penalties]
        penalties_occurrences = [item[2] for item in fits_and_penalties]

        best_sol = None
        best_fit = float("inf")
        best_penalty = {}
        best_penalty_occurrences = {}
        historico_fitness = []

        for _ in range(n_gen):
            new_pop = []

            for i, f in enumerate(fits):
                if f < best_fit:
                    best_fit = f
                    best_sol = pop[i][:]
                    best_penalty = penalties[i]
                    best_penalty_occurrences = penalties_occurrences[i]

            historico_fitness.append(best_fit)

            while len(new_pop) < tam_pop:
                p1 = pop[self.torneio(pop, fits)]
                p2 = pop[self.torneio(pop, fits)]

                if random.random() < pc:
                    c1, c2 = self.crossover(p1, p2)
                else:
                    c1, c2 = p1[:], p2[:]

                if random.random() < pm:
                    c1 = self.mutacao(c1, colab_ids, 0.1)
                if random.random() < pm:
                    c2 = self.mutacao(c2, colab_ids, 0.1)

                new_pop.append(c1)
                if len(new_pop) < tam_pop:
                    new_pop.append(c2)

            fits_and_penalties = [self.avaliar(ind, tarefas_globais, colaboradores) for ind in new_pop]
            pop = new_pop
            fits = [item[0] for item in fits_and_penalties]
            penalties = [item[1] for item in fits_and_penalties]
            penalties_occurrences = [item[2] for item in fits_and_penalties]

        return best_sol, best_fit, historico_fitness, best_penalty, best_penalty_occurrences