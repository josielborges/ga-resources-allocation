<template>
  <div class="gantt-container">
    <h3>Cronograma Gantt</h3>
    
    <el-card class="gantt-card">
      <el-table 
        :data="tarefas" 
        size="small" 
        style="width: 100%"
        :row-class-name="getRowClassName"
        stripe
      >
        <el-table-column prop="projeto" label="Projeto" width="140" fixed>
          <template #default="scope">
            <el-tag :color="getProjectColor(scope.row.projeto)" size="small">
              {{ scope.row.projeto }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="nome_tarefa" label="Tarefa" min-width="180" />
        
        <el-table-column prop="data_inicio" label="Início" width="100" />
        
        <el-table-column prop="data_fim" label="Fim" width="100" />
        
        <el-table-column prop="colaborador" label="Colaborador" width="140" />
        
        <el-table-column prop="duracao_dias" label="Dias" width="80" align="center" />
        
        <el-table-column label="Cronograma Visual" min-width="250">
          <template #default="scope">
            <div class="gantt-timeline">
              <div 
                class="gantt-bar" 
                :style="getGanttStyle(scope.row)"
                :title="`${scope.row.nome_tarefa} (${scope.row.duracao_dias} dias)`"
              >
                <span class="gantt-text">{{ scope.row.duracao_dias }}d</span>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
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
      const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#9C27B0', '#FF9800']
      const projects = [...new Set(this.tarefas.map(t => t.projeto))]
      const colorMap = {}
      projects.forEach((project, index) => {
        colorMap[project] = colors[index % colors.length]
      })
      return colorMap
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
        backgroundColor: this.projectColors[tarefa.projeto] || '#409EFF',
        height: '20px',
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
      return this.projectColors[projeto] || '#409EFF'
    },
    getRowClassName({ row, rowIndex }) {
      return rowIndex % 2 === 0 ? 'even-row' : 'odd-row'
    }
  }
}
</script>

<style scoped>
.gantt-container {
  padding: 20px;
}

.gantt-card {
  margin-top: 20px;
  overflow-x: auto;
}

.gantt-timeline {
  width: 100%;
  height: 25px;
  background: linear-gradient(to right, #f5f5f5 0%, #e8e8e8 100%);
  position: relative;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.gantt-bar {
  position: absolute;
  top: 2px;
  height: 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.gantt-bar:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}

.gantt-text {
  font-size: 10px;
  font-weight: bold;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

h3 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.el-tag {
  font-weight: 500;
}

:deep(.even-row) {
  background-color: #fafafa;
}

:deep(.odd-row) {
  background-color: #ffffff;
}

:deep(.el-table__row:hover) {
  background-color: #f0f9ff;
}
</style>