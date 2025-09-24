<template>
  <div class="calendar-container">
    <div class="filters-section">
      <h3>Filtros</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-select v-model="filtros.projetos" multiple placeholder="Selecione projetos" style="width: 100%">
            <el-option v-for="proj in projetosUnicos" :key="proj" :label="proj" :value="proj" />
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-select v-model="filtros.colaboradores" multiple placeholder="Selecione colaboradores" style="width: 100%">
            <el-option v-for="colab in colaboradoresUnicos" :key="colab" :label="colab" :value="colab" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <div class="calendar-section">
      <h3>Calendário de Alocação</h3>
      <el-card class="calendar-card">
        <div class="calendar-wrapper">
          <FullCalendar :options="calendarOptions" />
        </div>
      </el-card>
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
          backgroundColor: projeto?.color || '#409EFF',
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
.calendar-container {
  padding: 20px;
}

.filters-section {
  margin-bottom: 30px;
}

.calendar-section {
  margin-top: 20px;
}

.calendar-card {
  padding: 20px;
}

.calendar-wrapper {
  min-height: 600px;
}

h3 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

:deep(.fc) {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

:deep(.fc-toolbar) {
  margin-bottom: 20px;
}

:deep(.fc-toolbar-title) {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

:deep(.fc-button) {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
}

:deep(.fc-button:hover) {
  background-color: #337ecc;
  border-color: #337ecc;
}

:deep(.fc-button:focus) {
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

:deep(.fc-daygrid-day-number) {
  color: #606266;
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
  color: #409eff;
  font-weight: 500;
}

:deep(.fc-popover) {
  border: 1px solid #dcdfe6;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .calendar-container {
    padding: 10px;
  }
  
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