<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-text-primary">Cronograma Gantt</h3>
      <span class="text-sm text-gray-600 font-medium">{{ dataFinalCronograma }}</span>
    </div>
    
    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          @click="activeTab = 'projetos'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeTab === 'projetos'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Projetos
        </button>
        <button
          @click="activeTab = 'intervalos'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeTab === 'intervalos'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Intervalos
        </button>
        <button
          @click="activeTab = 'tarefas'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeTab === 'tarefas'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Tarefas
        </button>
      </nav>
    </div>

    <!-- Tab Content -->
    <div class="bg-white rounded-md shadow-sm overflow-x-auto">
      <!-- Projetos Tab -->
      <div v-if="activeTab === 'projetos'">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-32">Projeto</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Início</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Fim</th>
              <th class="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase w-16">Tarefas</th>
              <th class="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase w-16">Dias</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-48">Timeline</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(projeto, index) in projetosAgrupados" :key="projeto.nome" :class="index % 2 === 0 ? 'bg-gray-50' : 'bg-white'" class="hover:bg-blue-50">
              <td class="px-3 py-1.5 text-sm">
                <span 
                  class="px-2 py-0.5 text-white text-xs font-medium rounded"
                  :style="{ backgroundColor: getProjectColor(projeto.nome) }"
                >
                  {{ projeto.nome }}
                </span>
              </td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_inicio }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_fim }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.total_tarefas }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.duracao_total }}</td>
              <td class="px-3 py-1.5">
                <div class="gantt-timeline-compact">
                  <div 
                    class="gantt-bar-compact" 
                    :style="getGanttStyleAgrupado(projeto)"
                    :title="`${projeto.nome} (${projeto.total_tarefas} tarefas, ${projeto.duracao_total} dias)`"
                  >
                    <span class="gantt-text-compact">{{ projeto.duracao_total }}d</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Intervalos Tab -->
      <div v-if="activeTab === 'intervalos'">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-32">Projeto</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Início</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Fim</th>
              <th class="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase w-16">Dias</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-48">Timeline de Intervalos</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(projeto, index) in projetosComIntervalos" :key="projeto.nome" :class="index % 2 === 0 ? 'bg-gray-50' : 'bg-white'" class="hover:bg-blue-50">
              <td class="px-3 py-1.5 text-sm">
                <span 
                  class="px-2 py-0.5 text-white text-xs font-medium rounded"
                  :style="{ backgroundColor: getProjectColor(projeto.nome) }"
                >
                  {{ projeto.nome }}
                </span>
              </td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_inicio }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_fim }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.duracao_total }}</td>
              <td class="px-3 py-1.5">
                <div class="gantt-timeline-intervals">
                  <div 
                    v-for="(intervalo, idx) in projeto.intervalos" 
                    :key="idx"
                    class="gantt-interval" 
                    :style="getIntervalStyle(intervalo, projeto.nome)"
                    :title="`${projeto.nome} - Intervalo ${idx + 1} (${intervalo.duracao} dias)`"
                  >
                    <span class="gantt-interval-text">{{ intervalo.duracao }}d</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tarefas Tab -->
      <div v-if="activeTab === 'tarefas'">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-20">Projeto</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-48">Tarefa</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Início</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Fim</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-40">Colaborador</th>
              <th class="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase w-16">Dias</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-48">Timeline</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(tarefa, index) in tarefasOrdenadas" :key="index" :class="index % 2 === 0 ? 'bg-gray-50' : 'bg-white'" class="hover:bg-blue-50">
              <td class="px-3 py-1.5 text-sm">
                <span 
                  class="px-2 py-0.5 text-white text-xs font-medium rounded"
                  :style="{ backgroundColor: getProjectColor(tarefa.projeto) }"
                >
                  {{ tarefa.projeto }}
                </span>
              </td>
              <td class="px-3 py-1.5 text-sm font-medium truncate" :title="tarefa.nome_tarefa">{{ tarefa.nome_tarefa }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ tarefa.data_inicio }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ tarefa.data_fim }}</td>
              <td class="px-3 py-1.5 text-sm font-medium">{{ tarefa.colaborador }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ tarefa.duracao_dias }}</td>
              <td class="px-3 py-1.5">
                <div class="gantt-timeline-compact">
                  <div 
                    class="gantt-bar-compact" 
                    :style="getGanttStyle(tarefa)"
                    :title="`${tarefa.nome_tarefa} (${tarefa.duracao_dias} dias)`"
                  >
                    <span class="gantt-text-compact">{{ tarefa.duracao_dias }}d</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GanttTab',
  props: {
    tarefas: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      activeTab: 'projetos'
    }
  },

  computed: {
    duracaoMaxima() {
      if (!this.tarefas || this.tarefas.length === 0) return 100
      return Math.max(...this.tarefas.map(t => t.fim_dias))
    },
    projectColors() {
      const colors = ['#3f6ad8', '#3ac47d', '#f7b924', '#d92550', '#16aaff', '#9C27B0', '#FF9800']
      const projects = [...new Set(this.tarefas.map(t => t.projeto))]
      const colorMap = {}
      projects.forEach((project, index) => {
        colorMap[project] = colors[index % colors.length]
      })
      return colorMap
    },
    projetosAgrupados() {
      const grupos = {}
      
      this.tarefas.forEach(tarefa => {
        if (!grupos[tarefa.projeto]) {
          grupos[tarefa.projeto] = {
            nome: tarefa.projeto,
            tarefas: [],
            inicio_dias: tarefa.inicio_dias,
            fim_dias: tarefa.fim_dias
          }
        }
        
        grupos[tarefa.projeto].tarefas.push(tarefa)
        grupos[tarefa.projeto].inicio_dias = Math.min(grupos[tarefa.projeto].inicio_dias, tarefa.inicio_dias)
        grupos[tarefa.projeto].fim_dias = Math.max(grupos[tarefa.projeto].fim_dias, tarefa.fim_dias)
      })
      
      return Object.values(grupos).map(grupo => ({
        ...grupo,
        total_tarefas: grupo.tarefas.length,
        duracao_total: grupo.fim_dias - grupo.inicio_dias + 1,
        data_inicio: grupo.tarefas.reduce((earliest, t) => t.data_inicio < earliest ? t.data_inicio : earliest, grupo.tarefas[0]?.data_inicio || ''),
        data_fim: grupo.tarefas.reduce((latest, t) => t.data_fim > latest ? t.data_fim : latest, grupo.tarefas[0]?.data_fim || '')
      })).sort((a, b) => a.fim_dias - b.fim_dias)
    },
    dataFinalCronograma() {
      if (!this.tarefas || this.tarefas.length === 0) return ''
      const dataFinal = this.tarefas.reduce((latest, t) => t.data_fim > latest ? t.data_fim : latest, this.tarefas[0]?.data_fim || '')
      return `Fim: ${dataFinal}`
    },
    projetosComIntervalos() {
      const grupos = {}
      
      this.tarefas.forEach(tarefa => {
        if (!grupos[tarefa.projeto]) {
          grupos[tarefa.projeto] = {
            nome: tarefa.projeto,
            tarefas: [],
            data_inicio: tarefa.data_inicio,
            data_fim: tarefa.data_fim
          }
        }
        
        grupos[tarefa.projeto].tarefas.push(tarefa)
        grupos[tarefa.projeto].data_inicio = grupos[tarefa.projeto].data_inicio < tarefa.data_inicio ? grupos[tarefa.projeto].data_inicio : tarefa.data_inicio
        grupos[tarefa.projeto].data_fim = grupos[tarefa.projeto].data_fim > tarefa.data_fim ? grupos[tarefa.projeto].data_fim : tarefa.data_fim
      })
      
      return Object.values(grupos).map(grupo => {
        const tarefasOrdenadas = grupo.tarefas.sort((a, b) => a.inicio_dias - b.inicio_dias)
        const intervalos = []
        let inicioAtual = tarefasOrdenadas[0].inicio_dias
        let fimAtual = tarefasOrdenadas[0].fim_dias
        
        for (let i = 1; i < tarefasOrdenadas.length; i++) {
          const tarefa = tarefasOrdenadas[i]
          if (tarefa.inicio_dias <= fimAtual + 1) {
            fimAtual = Math.max(fimAtual, tarefa.fim_dias)
          } else {
            intervalos.push({
              inicio: inicioAtual,
              fim: fimAtual,
              duracao: fimAtual - inicioAtual + 1
            })
            inicioAtual = tarefa.inicio_dias
            fimAtual = tarefa.fim_dias
          }
        }
        
        intervalos.push({
          inicio: inicioAtual,
          fim: fimAtual,
          duracao: fimAtual - inicioAtual + 1
        })
        
        return {
          ...grupo,
          intervalos,
          duracao_total: intervalos.reduce((total, int) => total + int.duracao, 0)
        }
      }).sort((a, b) => {
        const maxFimA = Math.max(...a.tarefas.map(t => t.fim_dias))
        const maxFimB = Math.max(...b.tarefas.map(t => t.fim_dias))
        return maxFimA - maxFimB
      })
    },
    tarefasOrdenadas() {
      const projectEndDays = {}
      this.projetosAgrupados.forEach(p => {
        projectEndDays[p.nome] = p.fim_dias
      })
      return [...this.tarefas].sort((a, b) => {
        const endDayA = projectEndDays[a.projeto] || a.fim_dias
        const endDayB = projectEndDays[b.projeto] || b.fim_dias
        return endDayA - endDayB
      })
    }
  },
  methods: {
    getGanttStyle(tarefa) {
      if (!tarefa || this.duracaoMaxima === 0) {
        return { display: 'none' }
      }
      
      const proporcaoInicio = (tarefa.inicio_dias / this.duracaoMaxima) * 100
      const proporcaoDuracao = ((tarefa.fim_dias - tarefa.inicio_dias + 1) / this.duracaoMaxima) * 100
      
      return {
        left: `${Math.max(0, proporcaoInicio)}%`,
        width: `${Math.max(2, proporcaoDuracao)}%`,
        backgroundColor: this.projectColors[tarefa.projeto] || '#3f6ad8',
        height: '14px',
        position: 'absolute',
        borderRadius: '4px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontSize: '11px',
        fontWeight: 'bold',
        boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
      }
    },
    getProjectColor(projeto) {
      return this.projectColors[projeto] || '#3f6ad8'
    },
    getGanttStyleAgrupado(projeto) {
      if (!projeto || this.duracaoMaxima === 0) {
        return { display: 'none' }
      }
      
      const proporcaoInicio = (projeto.inicio_dias / this.duracaoMaxima) * 100
      const proporcaoDuracao = (projeto.duracao_total / this.duracaoMaxima) * 100
      
      return {
        left: `${Math.max(0, proporcaoInicio)}%`,
        width: `${Math.max(2, proporcaoDuracao)}%`,
        backgroundColor: this.projectColors[projeto.nome] || '#3f6ad8',
        height: '14px',
        position: 'absolute',
        borderRadius: '4px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontSize: '11px',
        fontWeight: 'bold',
        boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
      }
    },
    getIntervalStyle(intervalo, projeto) {
      if (!intervalo || this.duracaoMaxima === 0) {
        return { display: 'none' }
      }
      
      const proporcaoInicio = (intervalo.inicio / this.duracaoMaxima) * 100
      const proporcaoDuracao = (intervalo.duracao / this.duracaoMaxima) * 100
      
      return {
        left: `${Math.max(0, proporcaoInicio)}%`,
        width: `${Math.max(2, proporcaoDuracao)}%`,
        backgroundColor: this.projectColors[projeto] || '#3f6ad8',
        height: '12px',
        position: 'absolute',
        borderRadius: '3px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontSize: '10px',
        fontWeight: 'bold',
        boxShadow: '0 1px 2px rgba(0,0,0,0.15)',
        border: '1px solid rgba(255,255,255,0.2)'
      }
    }
  }
}
</script>

<style scoped>
.gantt-timeline-compact {
  width: 100%;
  height: 18px;
  background: linear-gradient(to right, #f8f9fa 0%, #e9ecef 100%);
  position: relative;
  border-radius: 3px;
  border: 1px solid #dee2e6;
}

.gantt-bar-compact {
  position: absolute;
  top: 1px;
  height: 14px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gantt-bar-compact:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

.gantt-text-compact {
  font-size: 9px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 1px rgba(0,0,0,0.4);
}

.gantt-timeline-intervals {
  width: 100%;
  height: 16px;
  background: linear-gradient(to right, #f1f3f4 0%, #e8eaed 100%);
  position: relative;
  border-radius: 3px;
  border: 1px solid #dadce0;
}

.gantt-interval {
  position: absolute;
  top: 1px;
  height: 12px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gantt-interval:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

.gantt-interval-text {
  font-size: 8px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 1px rgba(0,0,0,0.4);
}
</style>