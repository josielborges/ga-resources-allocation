<template>
  <div class="space-y-8">
    <div>
      <div class="bg-blue-50 border-l-4 border-blue-400 p-3 mb-4">
        <h3 class="text-lg font-semibold text-blue-800 flex items-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          Filtros
        </h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-md shadow-sm p-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Projetos
            <span class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">{{ filtros.projetos.length }}/{{ projetosUnicos.length }}</span>
          </h4>
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <label v-for="proj in projetosUnicos" :key="proj" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
              <input 
                type="checkbox" 
                :value="proj" 
                v-model="filtros.projetos"
                class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <span class="text-sm text-gray-700">{{ proj }}</span>
            </label>
          </div>
          <div class="mt-3 flex gap-2">
            <button @click="selecionarTodosProjetos" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200">
              Todos
            </button>
            <button @click="limparProjetos" class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200">
              Limpar
            </button>
          </div>
        </div>
        <div class="bg-white rounded-md shadow-sm p-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
            </svg>
            Colaboradores
            <span class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">{{ filtros.colaboradores.length }}/{{ colaboradoresUnicos.length }}</span>
          </h4>
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <label v-for="colab in colaboradoresUnicos" :key="colab" class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
              <input 
                type="checkbox" 
                :value="colab" 
                v-model="filtros.colaboradores"
                class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
              />
              <span class="text-sm text-gray-700">{{ colab }}</span>
            </label>
          </div>
          <div class="mt-3 flex gap-2">
            <button @click="selecionarTodosColaboradores" class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded hover:bg-green-200">
              Todos
            </button>
            <button @click="limparColaboradores" class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200">
              Limpar
            </button>
          </div>
        </div>
      </div>
    </div>

    <div>
      <h3 class="text-lg font-semibold text-text-primary mb-4">Calendário de Alocação</h3>
      <div class="card">
        <div class="calendar-wrapper">
          <FullCalendar :options="calendarOptions" />
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
      }
    }
  },
  computed: {
    projetosUnicos() {
      return [...new Set(this.tarefas.map(t => t.projeto))]
    },
    colaboradoresUnicos() {
      return [...new Set(this.tarefas.map(t => t.colaborador))]
    },
    tarefasFiltradas() {
      return this.tarefas.filter(t => 
        (this.filtros.projetos.length === 0 || this.filtros.projetos.includes(t.projeto)) &&
        (this.filtros.colaboradores.length === 0 || this.filtros.colaboradores.includes(t.colaborador))
      )
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
    },
    calendarOptions() {
      return {
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        initialDate: this.primeiraDataAlocacao,
        locale: 'pt-br',
        events: this.eventos,
        height: 'auto',
        aspectRatio: 1.35,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth'
        },
        buttonText: {
          today: 'Hoje',
          month: 'Mês'
        },
        weekends: false,
        dayMaxEvents: 3,
        moreLinkClick: 'popover',
        eventDisplay: 'block',
        displayEventTime: false,
        eventClassNames: 'custom-event',
        eventDidMount: function(info) {
          info.el.setAttribute('title', `${info.event.extendedProps.projeto} - ${info.event.extendedProps.tarefa}`)
        }
      }
    }
  },
  mounted() {
    this.filtros.projetos = this.projetosUnicos
    this.filtros.colaboradores = this.colaboradoresUnicos
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
    }
  }
}
</script>

<style scoped>
.calendar-wrapper {
  min-height: 600px;
}

:deep(.fc) {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

:deep(.fc-toolbar) {
  margin-bottom: 20px;
}

:deep(.fc-toolbar-title) {
  font-size: 20px;
  font-weight: 600;
  color: #495057;
}

:deep(.fc-button) {
  background-color: #3f6ad8;
  border-color: #3f6ad8;
  color: white;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
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
}

:deep(.fc-event) {
  border-radius: 4px;
  border: none;
  font-size: 12px;
  font-weight: 500;
  margin: 1px 0;
  padding: 2px 4px;
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
}

:deep(.fc-popover) {
  border: 1px solid #e9ecef;
  box-shadow: 0 0.46875rem 2.1875rem rgba(4, 9, 20, 0.03), 0 0.9375rem 1.40625rem rgba(4, 9, 20, 0.03), 0 0.25rem 0.53125rem rgba(4, 9, 20, 0.05), 0 0.125rem 0.1875rem rgba(4, 9, 20, 0.03);
}

@media (max-width: 768px) {
  .calendar-wrapper {
    min-height: 400px;
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