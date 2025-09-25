<template>
  <div class="space-y-8">
    <div>
      <h3 class="text-lg font-semibold text-text-primary mb-4">Filtros</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="caption block mb-2">Projetos</label>
          <select v-model="filtros.projetos" multiple class="form-select h-32">
            <option v-for="proj in projetosUnicos" :key="proj" :value="proj">
              {{ proj }}
            </option>
          </select>
        </div>
        <div>
          <label class="caption block mb-2">Colaboradores</label>
          <select v-model="filtros.colaboradores" multiple class="form-select h-32">
            <option v-for="colab in colaboradoresUnicos" :key="colab" :value="colab">
              {{ colab }}
            </option>
          </select>
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