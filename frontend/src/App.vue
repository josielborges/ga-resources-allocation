<template>
  <div class="h-screen bg-background-default font-sans overflow-hidden">
    <div class="flex h-full">
      <!-- Menu Lateral -->
      <div class="w-64 bg-gradient-to-b from-cyan-600 to-green-400 text-white overflow-y-auto">
        <div class="p-4">
          <h2 class="text-lg font-semibold mb-6">Roadmaps & Estimativas</h2>
          <nav class="space-y-1">
            <template v-for="item in menuItems" :key="item.id">
              <!-- Item normal -->
              <button 
                v-if="!item.submenu"
                @click="activeModule = item.id"
                :class="[
                  'w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  activeModule === item.id 
                    ? 'bg-white bg-opacity-20 text-white shadow-md' 
                    : 'text-white hover:bg-white hover:bg-opacity-15'
                ]"
              >
                <component :is="item.icon" class="w-5 h-5" />
                {{ item.label }}
              </button>
              
              <!-- Item com submenu -->
              <div v-else>
                <button 
                  @click="item.expanded = !item.expanded"
                  :class="[
                    'w-full flex items-center justify-between gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                    item.submenu.some(sub => activeModule === sub.id)
                      ? 'bg-white bg-opacity-20 text-white shadow-md' 
                      : 'text-white hover:bg-white hover:bg-opacity-15'
                  ]"
                >
                  <div class="flex items-center gap-3">
                    <component :is="item.icon" class="w-5 h-5" />
                    {{ item.label }}
                  </div>
                  <svg 
                    :class="['w-4 h-4 transition-transform', item.expanded ? 'rotate-180' : '']"
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                <!-- Submenu -->
                <div v-if="item.expanded" class="ml-8 mt-1 space-y-1">
                  <button 
                    v-for="subItem in item.submenu" 
                    :key="subItem.id"
                    @click="activeModule = subItem.id"
                    :class="[
                      'w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                      activeModule === subItem.id 
                        ? 'bg-white bg-opacity-20 text-white shadow-md' 
                        : 'text-white hover:bg-white hover:bg-opacity-15'
                    ]"
                  >
                    <component :is="subItem.icon" class="w-4 h-4" />
                    {{ subItem.label }}
                  </button>
                </div>
              </div>
            </template>
          </nav>
        </div>
      </div>

      <!-- Área do Roadmap com header estendido -->
      <div v-if="activeModule === 'roadmap'" class="flex-1 flex flex-col">
        <!-- Header estendido -->
        <div class="text-white px-6 py-4 shadow-sm flex-shrink-0" style="background: linear-gradient(to bottom, #0891B2, #0C94AD);">
          <h1 class="text-xl font-semibold">{{ getModuleTitle() }}</h1>
        </div>
        
        <!-- Conteúdo do roadmap -->
        <div class="flex flex-1 overflow-hidden">
          <!-- Parâmetros Sidebar -->
          <div class="w-72 bg-background-paper border-r border-divider flex-shrink-0">
            <div class="p-4">
            <div class="bg-white rounded-md shadow-sm p-4">
              <h3 class="text-base font-semibold text-text-primary mb-4">Parâmetros do algoritmo</h3>
              
              <form class="space-y-4">
                <div>
                  <label class="caption block mb-2">População</label>
                  <input 
                    v-model="params.tam_pop" 
                    type="range" 
                    min="10" 
                    max="100" 
                    class="form-slider"
                  />
                  <div class="flex justify-between text-sm text-text-secondary mt-1">
                    <span>10</span>
                    <span class="font-medium">{{ params.tam_pop }}</span>
                    <span>100</span>
                  </div>
                </div>
                
                <div>
                  <label class="caption block mb-2">Gerações</label>
                  <input 
                    v-model="params.n_gen" 
                    type="range" 
                    min="5" 
                    max="1000" 
                    class="form-slider"
                  />
                  <div class="flex justify-between text-sm text-text-secondary mt-1">
                    <span>5</span>
                    <span class="font-medium">{{ params.n_gen }}</span>
                    <span>1000</span>
                  </div>
                </div>
                
                <div>
                  <label class="caption block mb-2">Crossover</label>
                  <input 
                    v-model="params.pc" 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    class="form-slider"
                  />
                  <div class="flex justify-between text-sm text-text-secondary mt-1">
                    <span>0</span>
                    <span class="font-medium">{{ params.pc }}</span>
                    <span>1</span>
                  </div>
                </div>
                
                <div>
                  <label class="caption block mb-2">Mutação</label>
                  <input 
                    v-model="params.pm" 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    class="form-slider"
                  />
                  <div class="flex justify-between text-sm text-text-secondary mt-1">
                    <span>0</span>
                    <span class="font-medium">{{ params.pm }}</span>
                    <span>1</span>
                  </div>
                </div>
                
                <div>
                  <label class="caption block mb-2">Data de Referência</label>
                  <input 
                    v-model="params.ref_date" 
                    type="date" 
                    class="form-input"
                  />
                </div>
                
                <button 
                  @click="executarAlgoritmo" 
                  :disabled="loading" 
                  class="bg-primary-main text-white px-4 py-2 rounded-sm text-sm font-medium w-full mt-4 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-light transition-colors"
                  type="button"
                >
                  <span v-if="loading" class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Executando...
                  </span>
                  <span v-else>Executar Algoritmo</span>
                </button>
              </form>
            </div>
            </div>
          </div>
          
          <!-- Conteúdo principal -->
          <div class="flex-1 p-4 overflow-y-auto">
            <div v-if="!resultado" class="mt-6">
              <div class="bg-semantic-info-light border border-semantic-info-main rounded-md p-3 mb-4">
                <div class="flex items-center">
                  <svg class="w-4 h-4 text-semantic-info-main mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-semantic-info-main text-sm">Configure os parâmetros e execute o algoritmo</span>
                </div>
              </div>
              <div class="bg-white rounded-md shadow-sm p-4">
                <h4 class="text-base font-medium text-text-primary mb-2">Dados:</h4>
                <div class="text-sm text-text-secondary space-y-1">
                  <p>Colaboradores: {{ colaboradores.length }}</p>
                  <p>Projetos: {{ projetos.length }}</p>
                </div>
              </div>
            </div>

            <div v-if="resultado" class="bg-white rounded-md shadow-sm">
              <div class="border-b border-divider px-4">
                <nav class="flex space-x-6">
                  <button 
                    v-for="tab in tabs" 
                    :key="tab.name"
                    @click="activeTab = tab.name"
                    :class="[
                      'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
                      activeTab === tab.name 
                        ? 'border-primary-main text-primary-main' 
                        : 'border-transparent text-text-secondary hover:text-text-primary hover:border-gray-300'
                    ]"
                  >
                    {{ tab.label }}
                  </button>
                </nav>
              </div>
              
              <div class="p-4">
                <DadosTab v-if="activeTab === 'dados'" :colaboradores="colaboradores" :projetos="projetos" />
                <FitnessTab v-if="activeTab === 'fitness'" :historico="resultado.historico_fitness" :melhor="resultado.melhor_fitness" />
                <ConflitosTab v-if="activeTab === 'conflitos'" :penalidades="resultado.penalidades" :ocorrencias="resultado.ocorrencias_penalidades" />
                <GanttTab v-if="activeTab === 'gantt'" :tarefas="resultado.tarefas" />
                <CalendarioTab v-if="activeTab === 'calendario'" :tarefas="resultado.tarefas" :projetos="projetos" />
                <MapaAlocacaoTab v-if="activeTab === 'mapa'" :tarefas="resultado.tarefas" :projetos="projetos" :colaboradores="colaboradores" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content (outros módulos) -->
      <div v-else class="flex-1 flex flex-col">
        <!-- Header (outros módulos) -->
        <div class="text-white px-6 py-4 shadow-sm flex-shrink-0" style="background: linear-gradient(to bottom, #0891B2, #0C94AD);">
          <h1 class="text-xl font-semibold">{{ getModuleTitle() }}</h1>
        </div>
        
        <!-- Content -->
        <div class="flex-1 p-4 overflow-y-auto">
          <!-- Módulo Projetos -->
          <div v-if="activeModule === 'projetos'">
            <ProjetosCrud />
          </div>

          <!-- Módulo Colaboradores -->
          <div v-if="activeModule === 'colaboradores'">
            <ColaboradoresCrud />
          </div>

          <!-- Módulo Cargos -->
          <div v-if="activeModule === 'cargos'">
            <CargosCrud />
          </div>

          <!-- Módulo Habilidades -->
          <div v-if="activeModule === 'habilidades'">
            <HabilidadesCrud />
          </div>

          <!-- Módulo Relatórios -->
          <div v-if="activeModule === 'relatorios'" class="bg-white rounded-md shadow-sm p-6">
            <p class="text-text-secondary">Módulo de relatórios em desenvolvimento...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { CpuChipIcon, FolderIcon, UserGroupIcon, DocumentChartBarIcon, CogIcon, BriefcaseIcon, AcademicCapIcon } from '@heroicons/vue/24/outline'
import DadosTab from './components/DadosTab.vue'
import FitnessTab from './components/FitnessTab.vue'
import ConflitosTab from './components/ConflitosTab.vue'
import GanttTab from './components/GanttTab.vue'
import CalendarioTab from './components/CalendarioTab.vue'
import MapaAlocacaoTab from './components/MapaAlocacaoTab.vue'
import ProjetosCrud from './components/ProjetosCrud.vue'
import ColaboradoresCrud from './components/ColaboradoresCrud.vue'
import HabilidadesCrud from './components/HabilidadesCrud.vue'
import CargosCrud from './components/CargosCrud.vue'

export default {
  name: 'App',
  components: {
    DadosTab,
    FitnessTab,
    ConflitosTab,
    GanttTab,
    CalendarioTab,
    MapaAlocacaoTab,
    ProjetosCrud,
    ColaboradoresCrud,
    HabilidadesCrud,
    CargosCrud,
    CpuChipIcon,
    FolderIcon,
    UserGroupIcon,
    DocumentChartBarIcon,
    CogIcon,
    BriefcaseIcon,
    AcademicCapIcon
  },
  data() {
    return {
      activeModule: 'roadmap',
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
      projetos: [],
      menuItems: [
        { id: 'roadmap', label: 'Gerador de Roadmap', icon: 'CpuChipIcon' },
        // { id: 'estimativa', label: 'Gerador de Estimativa', icon: 'CpuChipIcon' },
        { id: 'projetos', label: 'Projetos', icon: 'FolderIcon' },
        { id: 'colaboradores', label: 'Colaboradores', icon: 'UserGroupIcon' },
        { 
          id: 'configuracoes', 
          label: 'Configurações', 
          icon: 'CogIcon',
          expanded: false,
          submenu: [
            { id: 'cargos', label: 'Cargos', icon: 'BriefcaseIcon' },
            { id: 'habilidades', label: 'Habilidades', icon: 'AcademicCapIcon' }
          ]
        },
        // { id: 'relatorios', label: 'Relatórios', icon: 'DocumentChartBarIcon' }
      ],
      tabs: [
        { name: 'dados', label: 'Dados' },
        { name: 'fitness', label: 'Fitness' },
        { name: 'conflitos', label: 'Conflitos' },
        { name: 'gantt', label: 'Gantt' },
        { name: 'calendario', label: 'Calendário' },
        { name: 'mapa', label: 'Mapa de Alocação' }
      ]
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
        console.log(`Carregados ${this.colaboradores.length} colaboradores e ${this.projetos.length} projetos`)
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        console.error('Erro ao carregar dados:', error.message)
      }
    },
    async executarAlgoritmo() {
      this.loading = true
      try {
        const response = await axios.post('/api/executar-algoritmo', this.params)
        this.resultado = response.data
        this.activeTab = 'gantt'
        console.log('Algoritmo executado com sucesso!')
      } catch (error) {
        console.error('Erro ao executar algoritmo')
      } finally {
        this.loading = false
      }
    },
    getModuleTitle() {
      const titles = {
        'roadmap': 'Gerador de Roadmap',
        'estimativa': 'Gerador de Estimativa',
        'projetos': 'Gerenciamento de Projetos',
        'colaboradores': 'Gerenciamento de Colaboradores',
        'cargos': 'Gerenciamento de Cargos',
        'habilidades': 'Gerenciamento de Habilidades',
        'relatorios': 'Relatórios e Análises'
      }
      return titles[this.activeModule] || 'Sistema de Alocação'
    }
  }
}
</script>

<style>
.form-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #0891B2 0%, #0C94AD 100%);
  outline: none;
  cursor: pointer;
}

.form-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ffffff;
  border: 2px solid #0891B2;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ffffff;
  border: 2px solid #0891B2;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Scrollbar Styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #0891B2, #0C94AD);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #0e7490, #0a7c96);
}

@media (max-width: 768px) {
  .flex {
    flex-direction: column;
  }
  
  .w-64, .w-72 {
    width: 100% !important;
    height: auto;
  }
}
</style>