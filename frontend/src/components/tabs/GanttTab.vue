<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-3">
        <h3 class="text-lg font-semibold text-text-primary">Cronograma Gantt</h3>
        <button 
          v-if="totalViolacoes > 0"
          @click="showViolationsModal = true"
          class="flex items-center gap-1.5 px-3 py-1.5 bg-red-50 border border-red-300 rounded-md hover:bg-red-100 transition-colors"
          title="Clique para ver detalhes das violações"
        >
          <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-xs font-semibold text-red-700">{{ totalViolacoes }} {{ totalViolacoes === 1 ? 'Violação' : 'Violações' }}</span>
        </button>
      </div>
      <span class="text-sm text-gray-600 font-medium">{{ dataFinalCronograma }}</span>
    </div>
    
    <!-- Violations Modal -->
    <div v-if="showViolationsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showViolationsModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden" @click.stop>
        <div class="bg-red-50 border-b border-red-200 px-4 py-3 flex justify-between items-center">
          <h4 class="text-lg font-semibold text-red-800 flex items-center gap-2">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            Violações de Restrições
          </h4>
          <button @click="showViolationsModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[calc(80vh-60px)]">
          <div v-for="(tipo, key) in violacoesRelevantes" :key="key" class="mb-4">
            <div class="bg-orange-50 border-l-4 border-orange-400 p-3 mb-2">
              <h5 class="text-sm font-semibold text-orange-800">{{ translatePenalty(key) }} ({{ tipo.count }})</h5>
            </div>
            <div v-if="tipo.details && tipo.details.length > 0" class="bg-white border rounded-md overflow-hidden">
              <table class="min-w-full divide-y divide-gray-200 text-xs">
                <thead class="bg-gray-50">
                  <tr>
                    <th v-for="(value, colKey) in tipo.details[0]" :key="colKey" class="px-2 py-1.5 text-left text-xs font-medium text-gray-500 uppercase">
                      {{ colKey }}
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(item, idx) in tipo.details" :key="idx" class="hover:bg-gray-50">
                    <td v-for="(value, colKey) in item" :key="colKey" class="px-2 py-1.5 text-xs">
                      {{ formatViolationValue(key, colKey, value) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
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
                <div class="flex items-center gap-1">
                  <span 
                    class="px-2 py-0.5 text-white text-xs font-medium rounded"
                    :style="{ backgroundColor: getProjectColor(projeto.nome) }"
                  >
                    {{ projeto.nome }}
                  </span>
                  <span 
                    v-if="projetosComDeadline[projeto.nome] && (projetosComDeadline[projeto.nome].deadline_beyond_schedule || projetosComDeadline[projeto.nome].inicio_beyond_schedule || projetosComDeadline[projeto.nome].using_actual_start)"
                    class="text-amber-500 text-xs"
                    :title="getDateInconsistencyMessage(projeto.nome)"
                  >
                    ⚠️
                  </span>
                </div>
              </td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_inicio }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_fim }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.total_tarefas }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.duracao_total }}</td>
              <td class="px-3 py-1.5">
                <div class="gantt-timeline-compact">
                  <div 
                    v-if="projetosComDeadline[projeto.nome] && projetosComDeadline[projeto.nome].inicio_dias !== null"
                    :style="getStartStyle(projetosComDeadline[projeto.nome].inicio_dias)"
                    :title="`Início: ${projetosComDeadline[projeto.nome].inicio}`"
                    class="start-marker"
                  ></div>
                  <div 
                    class="gantt-bar-compact" 
                    :style="getGanttStyleAgrupado(projeto)"
                    :title="`${projeto.nome} (${projeto.total_tarefas} tarefas, ${projeto.duracao_total} dias)`"
                  >
                    <span class="gantt-text-compact">{{ projeto.duracao_total }}d</span>
                  </div>
                  <div 
                    v-if="projetosComDeadline[projeto.nome] && projetosComDeadline[projeto.nome].deadline_dias !== null"
                    :style="getDeadlineStyle(projetosComDeadline[projeto.nome].deadline_dias)"
                    :title="`Prazo: ${projetosComDeadline[projeto.nome].deadline}`"
                    class="deadline-marker"
                  ></div>
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
                <div class="flex items-center gap-1">
                  <span 
                    class="px-2 py-0.5 text-white text-xs font-medium rounded"
                    :style="{ backgroundColor: getProjectColor(projeto.nome) }"
                  >
                    {{ projeto.nome }}
                  </span>
                  <span 
                    v-if="projetosComDeadline[projeto.nome] && (projetosComDeadline[projeto.nome].deadline_beyond_schedule || projetosComDeadline[projeto.nome].inicio_beyond_schedule || projetosComDeadline[projeto.nome].using_actual_start)"
                    class="text-amber-500 text-xs"
                    :title="getDateInconsistencyMessage(projeto.nome)"
                  >
                    ⚠️
                  </span>
                </div>
              </td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_inicio }}</td>
              <td class="px-3 py-1.5 text-xs text-gray-600">{{ projeto.data_fim }}</td>
              <td class="px-3 py-1.5 text-sm text-center font-medium">{{ projeto.duracao_total }}</td>
              <td class="px-3 py-1.5">
                <div class="gantt-timeline-intervals">
                  <div 
                    v-if="projetosComDeadline[projeto.nome] && projetosComDeadline[projeto.nome].inicio_dias !== null"
                    :style="getStartStyle(projetosComDeadline[projeto.nome].inicio_dias)"
                    :title="`Início: ${projetosComDeadline[projeto.nome].inicio}`"
                    class="start-marker"
                  ></div>
                  <div 
                    v-for="(intervalo, idx) in projeto.intervalos" 
                    :key="idx"
                    class="gantt-interval" 
                    :style="getIntervalStyle(intervalo, projeto.nome)"
                    :title="`${projeto.nome} - Intervalo ${idx + 1} (${intervalo.duracao} dias)`"
                  >
                    <span class="gantt-interval-text">{{ intervalo.duracao }}d</span>
                  </div>
                  <div 
                    v-if="projetosComDeadline[projeto.nome] && projetosComDeadline[projeto.nome].deadline_dias !== null"
                    :style="getDeadlineStyle(projetosComDeadline[projeto.nome].deadline_dias)"
                    :title="`Prazo: ${projetosComDeadline[projeto.nome].deadline}`"
                    class="deadline-marker"
                  ></div>
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
                    v-if="projetosComDeadline[tarefa.projeto] && projetosComDeadline[tarefa.projeto].inicio_dias !== null"
                    :style="getStartStyle(projetosComDeadline[tarefa.projeto].inicio_dias)"
                    :title="`Início: ${projetosComDeadline[tarefa.projeto].inicio}`"
                    class="start-marker"
                  ></div>
                  <div 
                    class="gantt-bar-compact" 
                    :style="getGanttStyle(tarefa)"
                    :title="`${tarefa.nome_tarefa} (${tarefa.duracao_dias} dias)`"
                  >
                    <span class="gantt-text-compact">{{ tarefa.duracao_dias }}d</span>
                  </div>
                  <div 
                    v-if="projetosComDeadline[tarefa.projeto] && projetosComDeadline[tarefa.projeto].deadline_dias !== null"
                    :style="getDeadlineStyle(projetosComDeadline[tarefa.projeto].deadline_dias)"
                    :title="`Prazo: ${projetosComDeadline[tarefa.projeto].deadline}`"
                    class="deadline-marker"
                  ></div>
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
    },
    penalidades: {
      type: Object,
      default: () => ({})
    },
    ocorrencias: {
      type: Object,
      default: () => ({})
    },
    projetos: {
      type: Array,
      default: () => []
    },
    refDate: {
      type: String,
      default: '2025-01-01'
    }
  },
  data() {
    return {
      activeTab: 'projetos',
      showViolationsModal: false
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
      
      return Object.values(grupos).map(grupo => {
        const tarefaInicio = grupo.tarefas.find(t => t.inicio_dias === grupo.inicio_dias)
        const tarefaFim = grupo.tarefas.find(t => t.fim_dias === grupo.fim_dias)
        return {
          ...grupo,
          total_tarefas: grupo.tarefas.length,
          duracao_total: grupo.fim_dias - grupo.inicio_dias + 1,
          data_inicio: tarefaInicio?.data_inicio || '',
          data_fim: tarefaFim?.data_fim || ''
        }
      }).sort((a, b) => a.fim_dias - b.fim_dias)
    },
    dataFinalCronograma() {
      if (!this.tarefas || this.tarefas.length === 0) return ''
      const tarefaFinal = this.tarefas.reduce((latest, t) => t.fim_dias > latest.fim_dias ? t : latest, this.tarefas[0])
      return `Fim: ${tarefaFinal.data_fim}`
    },
    projetosComIntervalos() {
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
        
        const tarefaInicio = grupo.tarefas.find(t => t.inicio_dias === grupo.inicio_dias)
        const tarefaFim = grupo.tarefas.find(t => t.fim_dias === grupo.fim_dias)
        
        return {
          ...grupo,
          intervalos,
          duracao_total: intervalos.reduce((total, int) => total + int.duracao, 0),
          data_inicio: tarefaInicio?.data_inicio || '',
          data_fim: tarefaFim?.data_fim || ''
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
    },
    violacoesRelevantes() {
      const relevantes = {}
      const ignorar = ['gaps_projeto', 'makespan', 'resource_idle_time']
      
      Object.keys(this.ocorrencias || {}).forEach(key => {
        if (!ignorar.includes(key) && this.ocorrencias[key] && this.ocorrencias[key].length > 0) {
          relevantes[key] = {
            count: this.ocorrencias[key].length,
            details: this.ocorrencias[key]
          }
        }
      })
      
      return relevantes
    },
    totalViolacoes() {
      return Object.values(this.violacoesRelevantes).reduce((sum, v) => sum + v.count, 0)
    },
    projetosComDeadline() {
      const map = {}
      // Get unique project names from tasks
      const projectNames = [...new Set(this.tarefas.map(t => t.projeto))]
      
      projectNames.forEach(nome => {
        const projeto = this.projetos.find(p => p.nome === nome)
        const projetoAgrupado = this.projetosAgrupados.find(p => p.nome === nome)
        
        // Only show start marker if project has configured start date in database
        const hasConfiguredStart = projeto?.inicio != null
        const deadlineDias = projeto?.termino ? this.calcularDiasDesdeReferencia(projeto.termino) : null
        
        // For start dates: only use actual execution if there's a configured start date to compare against
        const inicioDias = hasConfiguredStart ? 
                          (projetoAgrupado ? projetoAgrupado.inicio_dias : this.calcularDiasDesdeReferencia(projeto.inicio)) :
                          null
        
        map[nome] = {
          deadline: projeto?.termino || null,
          deadline_dias: deadlineDias,
          deadline_beyond_schedule: deadlineDias && deadlineDias > this.duracaoMaxima,
          inicio: hasConfiguredStart ? 
                 (projetoAgrupado ? this.formatDateFromDays(projetoAgrupado.inicio_dias) : projeto.inicio) : 
                 null,
          inicio_dias: inicioDias,
          inicio_beyond_schedule: inicioDias && inicioDias > this.duracaoMaxima,
          using_actual_start: hasConfiguredStart && !!projetoAgrupado,
          has_configured_start: hasConfiguredStart
        }
      })
      return map
    },
  },
  methods: {
    translatePenalty(key) {
      const translations = {
        'habilidades_incorretas': 'Habilidades Incorretas',
        'cargo_incorreto': 'Cargo Incorreto',
        'ausencias': 'Ausências',
        'sobreposicoes_colaborador': 'Sobreposições de Colaborador',
        'sobreposicoes_projeto': 'Sobreposições de Projeto',
        'gaps_projeto': 'Intervalos entre Tarefas',
        'resource_idle_time': 'Tempo Ocioso de Recursos',
        'deadline_violation': 'Violação de Prazo',
        'project_start_violation': 'Violação de Data de Início',
        'makespan': 'Duração Total do Projeto',
        'work_period_violation': 'Violação de Período de Trabalho',
        'vacation_conflict': 'Conflito com Férias'
      }
      return translations[key] || key
    },
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
    },
    formatDateFromDays(days) {
      const refDate = new Date(this.refDate)
      const targetDate = new Date(refDate)
      targetDate.setDate(targetDate.getDate() + days)
      return targetDate.toISOString().split('T')[0] // Returns YYYY-MM-DD format
    },
    calcularDiasDesdeReferencia(dataStr) {
      if (!dataStr) return 0
      
      // Use the refDate prop instead of first task date for consistency
      const refDate = new Date(this.refDate)
      const [ano, mes, dia] = dataStr.split('-')
      const targetDate = new Date(ano, mes - 1, dia)
      
      return Math.floor((targetDate - refDate) / (1000 * 60 * 60 * 24))
    },
    getDeadlineStyle(deadlineDias) {
      // Don't show deadline marker if it's beyond the actual schedule
      if (deadlineDias > this.duracaoMaxima) {
        return { display: 'none' }
      }
      
      const proporcao = (deadlineDias / this.duracaoMaxima) * 100
      return {
        left: `${Math.max(0, proporcao)}%`,
        position: 'absolute',
        top: '0',
        bottom: '0',
        width: '2px',
        backgroundColor: '#dc2626',
        zIndex: 10
      }
    },
    getStartStyle(startDias) {
      // Don't show start marker if it's beyond the actual schedule
      if (startDias > this.duracaoMaxima) {
        return { display: 'none' }
      }
      
      const proporcao = (startDias / this.duracaoMaxima) * 100
      return {
        left: `${Math.max(0, proporcao)}%`,
        position: 'absolute',
        top: '0',
        bottom: '0',
        width: '2px',
        backgroundColor: '#16a34a',
        zIndex: 10
      }
    },
    getDateInconsistencyMessage(projectName) {
      const project = this.projetosComDeadline[projectName]
      if (!project) return ''
      
      const messages = []
      if (project.deadline_beyond_schedule) {
        const deadlineDate = new Date(project.deadline).toLocaleDateString('pt-BR')
        messages.push(`Deadline configurado (${deadlineDate}) está além do cronograma executado`)
      }
      if (project.inicio_beyond_schedule) {
        const startDate = new Date(project.inicio).toLocaleDateString('pt-BR')
        messages.push(`Data de início configurada (${startDate}) está além do cronograma executado`)
      }
      if (project.has_configured_start && project.using_actual_start) {
        messages.push(`Usando data de início real da execução (algoritmo ajustou devido a restrições)`)
      }
      if (!project.has_configured_start) {
        messages.push(`Projeto sem data de início configurada - usando execução livre`)
      }
      
      return messages.join('. ')
    },
    formatViolationValue(violationType, key, value) {
      if (violationType === 'deadline_violation' && (key === 'termino_planejado' || key === 'termino_real')) {
        const refDate = new Date(this.refDate)
        const targetDate = new Date(refDate)
        targetDate.setDate(targetDate.getDate() + value)
        return targetDate.toLocaleDateString('pt-BR')
      }
      return value
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

.deadline-marker {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #dc2626;
  z-index: 10;
  cursor: help;
}

.deadline-marker::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -3px;
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 6px solid #dc2626;
}

.start-marker {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #16a34a;
  z-index: 10;
  cursor: help;
}

.start-marker::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -3px;
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 6px solid #16a34a;
}
</style>