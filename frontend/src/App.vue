<template>
  <div id="app">
    <el-container class="app-container">
      <el-aside width="320px" class="sidebar">
        <el-card class="params-card">
          <template #header>
            <h3>Parâmetros do Algoritmo</h3>
          </template>
          
          <el-form :model="params" label-position="top" size="small">
            <el-form-item label="População">
              <el-slider v-model="params.tam_pop" :min="10" :max="100" show-input />
            </el-form-item>
            
            <el-form-item label="Gerações">
              <el-slider v-model="params.n_gen" :min="5" :max="1000" show-input />
            </el-form-item>
            
            <el-form-item label="Crossover">
              <el-slider v-model="params.pc" :min="0" :max="1" :step="0.1" show-input />
            </el-form-item>
            
            <el-form-item label="Mutação">
              <el-slider v-model="params.pm" :min="0" :max="1" :step="0.1" show-input />
            </el-form-item>
            
            <el-form-item label="Data de Referência">
              <el-date-picker 
                v-model="params.ref_date" 
                type="date" 
                format="YYYY-MM-DD"
                style="width: 100%" 
              />
            </el-form-item>
            
            <el-button 
              type="primary" 
              @click="executarAlgoritmo" 
              :loading="loading" 
              size="default"
              style="width: 100%; margin-top: 10px"
            >
              {{ loading ? 'Executando...' : 'Executar Algoritmo' }}
            </el-button>
          </el-form>
        </el-card>
      </el-aside>

      <el-main class="main-content">
        <div class="header">
          <h1>Alocação de Recursos - Algoritmo Genético</h1>
        </div>
        
        <div v-if="!resultado" class="welcome-section">
          <el-alert 
            title="Configure os parâmetros e execute o algoritmo na barra lateral" 
            type="info" 
            show-icon 
            :closable="false"
          />
          <el-card style="margin-top: 20px">
            <h4>Dados Carregados:</h4>
            <p>Colaboradores: {{ colaboradores.length }}</p>
            <p>Projetos: {{ projetos.length }}</p>
          </el-card>
        </div>

        <div v-if="resultado" class="results-section">
          <el-tabs v-model="activeTab" class="result-tabs">
            <el-tab-pane label="Dados" name="dados">
              <DadosTab :colaboradores="colaboradores" :projetos="projetos" />
            </el-tab-pane>
            
            <el-tab-pane label="Fitness" name="fitness">
              <FitnessTab :historico="resultado.historico_fitness" :melhor="resultado.melhor_fitness" />
            </el-tab-pane>
            
            <el-tab-pane label="Conflitos" name="conflitos">
              <ConflitosTab :penalidades="resultado.penalidades" :ocorrencias="resultado.ocorrencias_penalidades" />
            </el-tab-pane>
            
            <el-tab-pane label="Gantt" name="gantt">
              <GanttTab :tarefas="resultado.tarefas" />
            </el-tab-pane>
            
            <el-tab-pane label="Calendário" name="calendario">
              <CalendarioTab :tarefas="resultado.tarefas" :projetos="projetos" />
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'
import DadosTab from './components/DadosTab.vue'
import FitnessTab from './components/FitnessTab.vue'
import ConflitosTab from './components/ConflitosTab.vue'
import GanttTab from './components/GanttTab.vue'
import CalendarioTab from './components/CalendarioTab.vue'

export default {
  name: 'App',
  components: {
    DadosTab,
    FitnessTab,
    ConflitosTab,
    GanttTab,
    CalendarioTab
  },
  data() {
    return {
      params: {
        tam_pop: 20,
        n_gen: 100,
        pc: 0.7,
        pm: 0.3,
        ref_date: '2025-01-01'
      },
      loading: false,
      activeTab: 'dados',
      resultado: null,
      colaboradores: [],
      projetos: []
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      try {
        console.log('Carregando dados...')
        const [colabRes, projRes] = await Promise.all([
          axios.get('/api/colaboradores'),
          axios.get('/api/projetos')
        ])
        console.log('Colaboradores:', colabRes.data)
        console.log('Projetos:', projRes.data)
        this.colaboradores = colabRes.data
        this.projetos = projRes.data
        this.$message.success(`Carregados ${this.colaboradores.length} colaboradores e ${this.projetos.length} projetos`)
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        this.$message.error('Erro ao carregar dados: ' + error.message)
      }
    },
    async executarAlgoritmo() {
      this.loading = true
      try {
        const response = await axios.post('/api/executar-algoritmo', this.params)
        this.resultado = response.data
        this.activeTab = 'gantt'
        this.$message.success('Algoritmo executado com sucesso!')
      } catch (error) {
        this.$message.error('Erro ao executar algoritmo')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  height: 100vh;
  background-color: #f8f9fa;
}

.app-container {
  height: 100vh;
}

.sidebar {
  background-color: #ffffff;
  border-right: 1px solid #e4e7ed;
  padding: 20px;
  overflow-y: auto;
}

.params-card {
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.main-content {
  padding: 20px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

.header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #409eff;
}

.header h1 {
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.welcome-section {
  margin-top: 50px;
}

.results-section {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.result-tabs {
  min-height: 500px;
}

.el-form-item {
  margin-bottom: 18px;
}

.el-slider {
  margin: 10px 0;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100% !important;
    height: auto;
  }
  
  .main-content {
    padding: 10px;
  }
}
</style>