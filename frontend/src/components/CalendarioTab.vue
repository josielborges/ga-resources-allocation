<template>
  <div class="space-y-3">
    <!-- Filtros -->
    <div class="bg-white rounded-md shadow-sm border border-gray-200">
      <div class="bg-blue-50 border-b border-blue-200 px-3 py-1.5 flex items-center justify-between cursor-pointer" @click="filtrosExpanded = !filtrosExpanded">
        <h3 class="flex items-center gap-1.5 text-xs font-semibold text-blue-800">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          Filtros
        </h3>
        <svg class="w-4 h-4 text-blue-800 transition-transform" :class="filtrosExpanded ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>
      <div v-if="filtrosExpanded" class="grid grid-cols-1 md:grid-cols-2 gap-3 p-3">
        <!-- Projetos -->
        <div class="bg-gray-50 rounded border border-gray-200 p-2">
          <div class="flex items-center justify-between mb-2">
            <h4 class="text-xs font-semibold text-gray-700 flex items-center gap-1">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Projetos
            </h4>
            <span class="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-medium">{{ filtros.projetos.length }}/{{ projetosUnicos.length }}</span>
          </div>
          <div class="grid grid-cols-2 gap-0.5 max-h-24 overflow-y-auto bg-white border border-gray-200 rounded p-1.5 mb-2">
            <div 
              v-for="proj in projetosUnicos" 
              :key="proj" 
              @click="toggleProjeto(proj)"
              class="flex items-center gap-1.5 cursor-pointer hover:bg-blue-50 px-1.5 py-1 rounded transition-colors"
              :class="filtros.projetos.includes(proj) ? 'bg-blue-100' : ''"
            >
              <div class="w-3 h-3 rounded border flex items-center justify-center flex-shrink-0" :class="filtros.projetos.includes(proj) ? 'bg-blue-600 border-blue-600' : 'border-gray-300'">
                <svg v-if="filtros.projetos.includes(proj)" class="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
              </div>
              <span class="text-xs text-gray-700 truncate">{{ proj }}</span>
            </div>
          </div>
          <div class="flex gap-1">
            <button @click="selecionarTodosProjetos" class="flex-1 text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 transition-colors font-medium">
              Todos
            </button>
            <button @click="limparProjetos" class="flex-1 text-xs bg-white text-gray-700 px-2 py-1 rounded border border-gray-300 hover:bg-gray-50 transition-colors">
              Limpar
            </button>
          </div>
        </div>
        
        <!-- Colaboradores -->
        <div class="bg-gray-50 rounded border border-gray-200 p-2">
          <div class="flex items-center justify-between mb-2">
            <h4 class="text-xs font-semibold text-gray-700 flex items-center gap-1">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
              </svg>
              Colaboradores
            </h4>
            <span class="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-medium">{{ filtros.colaboradores.length }}/{{ colaboradoresUnicos.length }}</span>
          </div>
          <div class="grid grid-cols-2 gap-0.5 max-h-24 overflow-y-auto bg-white border border-gray-200 rounded p-1.5 mb-2">
            <div 
              v-for="colab in colaboradoresUnicos" 
              :key="colab" 
              @click="toggleColaborador(colab)"
              class="flex items-center gap-1.5 cursor-pointer hover:bg-green-50 px-1.5 py-1 rounded transition-colors"
              :class="filtros.colaboradores.includes(colab) ? 'bg-green-100' : ''"
            >
              <div class="w-3 h-3 rounded border flex items-center justify-center flex-shrink-0" :class="filtros.colaboradores.includes(colab) ? 'bg-green-600 border-green-600' : 'border-gray-300'">
                <svg v-if="filtros.colaboradores.includes(colab)" class="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
              </div>
              <span class="text-xs text-gray-700 truncate">{{ colab }}</span>
            </div>
          </div>
          <div class="flex gap-1">
            <button @click="selecionarTodosColaboradores" class="flex-1 text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700 transition-colors font-medium">
              Todos
            </button>
            <button @click="limparColaboradores" class="flex-1 text-xs bg-white text-gray-700 px-2 py-1 rounded border border-gray-300 hover:bg-gray-50 transition-colors">
              Limpar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Seletor de Ano -->
    <div class="bg-white rounded-md shadow-sm border border-gray-200 p-3">
      <div class="flex items-center justify-center gap-3">
        <button @click="selectedYear--" class="px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium">
          ← Ano Anterior
        </button>
        <span class="text-lg font-bold text-gray-700">{{ selectedYear }}</span>
        <button @click="selectedYear++" class="px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium">
          Próximo Ano →
        </button>
      </div>
    </div>

    <!-- Calendário em 3 Colunas -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
      <div v-for="month in 12" :key="`${selectedYear}-${month}`" class="bg-white rounded-md shadow-sm border border-gray-200">
        <div class="calendar-wrapper">
          <FullCalendar :key="`cal-${selectedYear}-${month}`" :options="getCalendarOptions(month)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

export default {
  name: 'CalendarioTab',
  components: { FullCalendar },
  props: {
    tarefas: Array,
    projetos: Array
  },
  data() {
    return {
      filtros: {
        projetos: [],
        colaboradores: []
      },
      filtrosExpanded: true,
      selectedYear: new Date().getFullYear()
    }
  },
  computed: {
    todosProjetosUnicos() {
      return [...new Set(this.tarefas.map(t => t.projeto))]
    },
    todosColaboradoresUnicos() {
      return [...new Set(this.tarefas.map(t => t.colaborador))]
    },
    projetosUnicos() {
      return this.todosProjetosUnicos
    },
    colaboradoresUnicos() {
      return this.todosColaboradoresUnicos
    },
    tarefasFiltradas() {
      if (this.filtros.projetos.length === 0 && this.filtros.colaboradores.length === 0) {
        return this.tarefas
      }
      return this.tarefas.filter(t => {
        const projetoMatch = this.filtros.projetos.length === 0 || this.filtros.projetos.includes(t.projeto)
        const colaboradorMatch = this.filtros.colaboradores.length === 0 || this.filtros.colaboradores.includes(t.colaborador)
        return projetoMatch && colaboradorMatch
      })
    },
    primeiraDataAlocacao() {
      if (this.tarefas.length === 0) return new Date().toISOString().split('T')[0]
      const primeiraData = this.tarefas.reduce((min, tarefa) => {
        const dataInicio = this.convertToISODate(tarefa.data_inicio)
        return dataInicio < min ? dataInicio : min
      }, this.convertToISODate(this.tarefas[0].data_inicio))
      return primeiraData
    },
    eventos() {
      return this.tarefasFiltradas.map(tarefa => {
        const projeto = this.projetos.find(p => p.nome === tarefa.projeto)
        return {
          title: `${tarefa.nome_tarefa} - ${tarefa.colaborador}`,
          start: this.convertToISODate(tarefa.data_inicio),
          end: this.convertToISODate(tarefa.data_fim, true),
          backgroundColor: projeto?.color || '#3f6ad8',
          extendedProps: {
            projeto: tarefa.projeto,
            tarefa: tarefa.nome_tarefa,
            colaborador: tarefa.colaborador,
            duracao: tarefa.duracao_dias
          }
        }
      })
    }
  },
  mounted() {
    this.filtros.projetos = [...this.todosProjetosUnicos]
    this.filtros.colaboradores = [...this.todosColaboradoresUnicos]
  },
  methods: {
    convertToISODate(dateStr, addDay = false) {
      const [day, month, year] = dateStr.split('/')
      const date = new Date(year, month - 1, day)
      if (addDay) {
        date.setDate(date.getDate() + 1)
      }
      return date.toISOString().split('T')[0]
    },
    toggleProjeto(proj) {
      const index = this.filtros.projetos.indexOf(proj)
      if (index > -1) {
        this.filtros.projetos.splice(index, 1)
      } else {
        this.filtros.projetos.push(proj)
      }
    },
    toggleColaborador(colab) {
      const index = this.filtros.colaboradores.indexOf(colab)
      if (index > -1) {
        this.filtros.colaboradores.splice(index, 1)
      } else {
        this.filtros.colaboradores.push(colab)
      }
    },
    selecionarTodosProjetos() {
      this.filtros.projetos = [...this.projetosUnicos]
    },
    limparProjetos() {
      this.filtros.projetos = []
    },
    selecionarTodosColaboradores() {
      this.filtros.colaboradores = [...this.colaboradoresUnicos]
    },
    limparColaboradores() {
      this.filtros.colaboradores = []
    },
    getCalendarOptions(month) {
      const initialDate = new Date(this.selectedYear, month - 1, 1)
      return {
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        initialDate: initialDate.toISOString().split('T')[0],
        locale: 'pt-br',
        events: this.eventos,
        height: 'auto',
        aspectRatio: 1.2,
        headerToolbar: {
          left: '',
          center: 'title',
          right: ''
        },
        weekends: false,
        dayMaxEvents: 2,
        moreLinkClick: 'popover',
        eventDisplay: 'block',
        displayEventTime: false,
        eventClassNames: 'custom-event',
        eventDidMount: function(info) {
          info.el.setAttribute('title', `${info.event.extendedProps.projeto} - ${info.event.extendedProps.tarefa}`)
        }
      }
    }
  }
}
</script>

<style scoped>
.calendar-wrapper {
  min-height: 250px;
  padding: 6px;
}

:deep(.fc) {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

:deep(.fc-toolbar) {
  margin-bottom: 8px;
}

:deep(.fc-col-header-cell) {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 2px;
}

:deep(.fc-daygrid-day) {
  font-size: 11px;
}

:deep(.fc-toolbar-title) {
  font-size: 13px;
  font-weight: 600;
  color: #495057;
}

:deep(.fc-button) {
  background-color: #3f6ad8;
  border-color: #3f6ad8;
  color: white;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 12px;
}

:deep(.fc-button:hover) {
  background-color: #7996e3;
  border-color: #7996e3;
}

:deep(.fc-button:focus) {
  box-shadow: 0 0 0 2px rgba(63, 106, 216, 0.2);
}

:deep(.fc-daygrid-day-number) {
  color: #6c757d;
  font-weight: 500;
  font-size: 11px;
  padding: 2px;
}

:deep(.fc-event) {
  border-radius: 2px;
  border: none;
  font-size: 11px;
  font-weight: 500;
  margin: 1px 0;
  padding: 0px 2px;
}

:deep(.fc-event-title) {
  font-weight: 500;
}

:deep(.fc-daygrid-event) {
  margin-top: 1px;
}

:deep(.fc-more-link) {
  color: #3f6ad8;
  font-weight: 500;
  font-size: 11px;
}

:deep(.fc-popover) {
  border: 1px solid #e9ecef;
  box-shadow: 0 0.46875rem 2.1875rem rgba(4, 9, 20, 0.03), 0 0.9375rem 1.40625rem rgba(4, 9, 20, 0.03), 0 0.25rem 0.53125rem rgba(4, 9, 20, 0.05), 0 0.125rem 0.1875rem rgba(4, 9, 20, 0.03);
}

:deep(.fc-popover-header) {
  font-size: 11px;
  padding: 4px 8px;
}

:deep(.fc-popover-title) {
  font-size: 11px;
}

:deep(.fc-popover-body) {
  font-size: 11px;
}

@media (max-width: 768px) {
  .calendar-wrapper {
    min-height: 350px;
  }
  
  :deep(.fc-toolbar) {
    flex-direction: column;
    gap: 10px;
  }
  
  :deep(.fc-toolbar-chunk) {
    display: flex;
    justify-content: center;
  }
}
</style>