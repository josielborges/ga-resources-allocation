<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-text-primary">Cronograma Gantt</h3>
      <span class="text-sm text-gray-600 font-medium">{{ dataFinalCronograma }}</span>
    </div>
    
    <!-- Visão por Projetos -->
    <div class="bg-white rounded-md shadow-sm overflow-x-auto mb-6">
      <div class="px-4 py-2 bg-gray-100 border-b">
        <h4 class="text-sm font-medium text-gray-700">Projetos</h4>
      </div>
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

    <!-- Visão por Tarefas -->
    <div class="bg-white rounded-md shadow-sm overflow-x-auto">
      <div class="px-4 py-2 bg-gray-100 border-b">
        <h4 class="text-sm font-medium text-gray-700">Tarefas</h4>
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-20">Projeto</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-32">Tarefa</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Início</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-20">Fim</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase w-28">Colaborador</th>
            <th class="px-3 py-2 text-center text-xs font-medium text-gray-500 uppercase w-16">Dias</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase min-w-48">Timeline</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(tarefa, index) in tarefas" :key="index" :class="index % 2 === 0 ? 'bg-gray-50' : 'bg-white'" class="hover:bg-blue-50">
            <td class="px-3 py-1.5 text-sm">
              <span 
                class="px-2 py-0.5 text-white text-xs font-medium rounded"
                :style="{ backgroundColor: getProjectColor(tarefa.projeto) }"
              >
                {{ tarefa.projeto }}
              </span>
            </td>
            <td class="px-3 py-1.5 text-sm font-medium">{{ tarefa.nome_tarefa }}</td>
            <td class="px-3 py-1.5 text-xs text-gray-600">{{ tarefa.data_inicio }}</td>
            <td class="px-3 py-1.5 text-xs text-gray-600">{{ tarefa.data_fim }}</td>
            <td class="px-3 py-1.5 text-sm">{{ tarefa.colaborador }}</td>
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
        data_inicio: grupo.tarefas[0]?.data_inicio || '',
        data_fim: grupo.tarefas.reduce((latest, t) => t.data_fim > latest ? t.data_fim : latest, grupo.tarefas[0]?.data_fim || '')
      }))
    },
    dataFinalCronograma() {
      if (!this.tarefas || this.tarefas.length === 0) return ''
      const dataFinal = this.tarefas.reduce((latest, t) => t.data_fim > latest ? t.data_fim : latest, this.tarefas[0]?.data_fim || '')
      return `Fim: ${dataFinal}`
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
</style>