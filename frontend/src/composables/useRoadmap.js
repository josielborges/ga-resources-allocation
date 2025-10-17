import { ref } from 'vue'
import axios from 'axios'

export function useRoadmap() {
  const loading = ref(false)
  const resultado = ref(null)
  const comparacaoResultado = ref(null)
  const resultadosSalvos = ref([])
  const executedColaboradores = ref([])
  const showProgress = ref(false)
  const progressData = ref({ current: 0, total: 100, percent: 0, fitness: 0 })
  const progressLoading = ref(false)

  async function executarAlgoritmo(params, selectedProjects, selectedCollaborators, selectedTransversais, simulatedMembers, colaboradores, allColaboradores) {
    loading.value = true
    showProgress.value = true
    progressData.value = { current: 0, total: 1, percent: 0, fitness: 0 }
    
    const selectedSquadMembers = colaboradores.filter(c => selectedCollaborators.includes(c.id))
    const selectedTransversalMembers = allColaboradores.filter(c => selectedTransversais.includes(c.id))
    
    try {
      const colaborador_ids = [...selectedSquadMembers.map(c => c.id), ...selectedTransversalMembers.map(c => c.id)]
      const payload = {
        ...params,
        projeto_ids: selectedProjects,
        colaborador_ids: colaborador_ids,
        simulated_members: simulatedMembers.map(m => ({
          nome: m.nome,
          cargo_id: m.cargo.id,
          habilidade_names: m.habilidades.map(h => h.nome),
          inicio: m.inicio || null,
          termino: m.termino || null
        }))
      }
      
      const streamEndpoint = params.algorithm === 'ga' ? '/api/executar-algoritmo-stream' : '/api/executar-aco-stream'
      const regularEndpoint = params.algorithm === 'ga' ? '/api/executar-algoritmo' : '/api/executar-aco'
      
      const response = await fetch(streamEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))
            
            if (data.error) {
              alert('Erro ao executar algoritmo: ' + data.error)
              showProgress.value = false
              loading.value = false
              return
            }
            
            if (data.type === 'progress') {
              progressData.value.current = data.generation
              progressData.value.total = data.total_generations
              progressData.value.fitness = data.best_fitness
            } else if (data.type === 'complete') {
              progressLoading.value = true
              const finalResponse = await axios.post(regularEndpoint, payload)
              resultado.value = finalResponse.data
              executedColaboradores.value = [...selectedSquadMembers, ...selectedTransversalMembers]
              showProgress.value = false
              progressLoading.value = false
              loading.value = false
              return
            }
          }
        }
      }
    } catch (error) {
      alert('Erro ao executar algoritmo: ' + error.message)
      showProgress.value = false
      loading.value = false
    }
  }

  async function compararAlgoritmos(refDate, gaParams, acoParams) {
    loading.value = true
    try {
      const response = await axios.post('/api/comparar-algoritmos', {
        ref_date: refDate,
        ga_params: gaParams,
        aco_params: acoParams
      })
      comparacaoResultado.value = response.data
    } finally {
      loading.value = false
    }
  }

  async function carregarResultadosSalvos(squadId, year) {
    try {
      const params = {}
      if (squadId) params.squad_id = squadId
      if (year) params.ano = year
      const response = await axios.get('/api/resultados-salvos', { params })
      resultadosSalvos.value = response.data
    } catch (error) {
      console.error('Erro ao carregar resultados salvos:', error)
    }
  }

  async function salvarResultado(name, params, resultadoData, executedColabs, simulatedMembers, squadId, year) {
    if (!name.trim()) return
    try {
      let roadmapEndDate = null
      if (resultadoData?.tarefas?.length) {
        const tarefaFinal = resultadoData.tarefas.reduce((latest, t) => 
          t.fim_dias > latest.fim_dias ? t : latest, resultadoData.tarefas[0])
        if (tarefaFinal?.data_fim) {
          const [dia, mes, ano] = tarefaFinal.data_fim.split('/')
          roadmapEndDate = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
        }
      }
      
      await axios.post('/api/resultados-salvos', {
        nome: name,
        algoritmo: params.algorithm,
        melhor_fitness: resultadoData.melhor_fitness,
        roadmap_end_date: roadmapEndDate,
        squad_id: squadId,
        ano: year,
        tarefas: resultadoData.tarefas,
        historico_fitness: resultadoData.historico_fitness,
        penalidades: resultadoData.penalidades,
        ocorrencias_penalidades: resultadoData.ocorrencias_penalidades,
        parametros: {
          ...params,
          roadmap_end_date: roadmapEndDate,
          saved_colaboradores: executedColabs,
          simulated_members: simulatedMembers.map(m => ({
            nome: m.nome,
            cargo_id: m.cargo.id,
            cargo: m.cargo,
            habilidade_names: m.habilidades.map(h => h.nome),
            habilidades: m.habilidades,
            inicio: m.inicio,
            termino: m.termino
          }))
        }
      })
      await carregarResultadosSalvos(squadId, year)
    } catch (error) {
      console.error('Erro ao salvar resultado:', error)
    }
  }

  async function carregarResultado(id, cargos, habilidades) {
    try {
      const response = await axios.get(`/api/resultados-salvos/${id}`)
      const saved = response.data
      resultado.value = {
        tarefas: saved.tarefas,
        melhor_fitness: saved.melhor_fitness,
        historico_fitness: saved.historico_fitness,
        penalidades: saved.penalidades,
        ocorrencias_penalidades: saved.ocorrencias_penalidades
      }
      
      if (saved.parametros.saved_colaboradores) {
        executedColaboradores.value = saved.parametros.saved_colaboradores
      }
      
      return saved.parametros
    } catch (error) {
      console.error('Erro ao carregar resultado:', error)
    }
  }

  async function deletarResultado(id, squadId, year) {
    try {
      await axios.delete(`/api/resultados-salvos/${id}`)
      await carregarResultadosSalvos(squadId, year)
    } catch (error) {
      console.error('Erro ao deletar resultado:', error)
    }
  }

  return {
    loading,
    resultado,
    comparacaoResultado,
    resultadosSalvos,
    executedColaboradores,
    showProgress,
    progressData,
    progressLoading,
    executarAlgoritmo,
    compararAlgoritmos,
    carregarResultadosSalvos,
    salvarResultado,
    carregarResultado,
    deletarResultado
  }
}
