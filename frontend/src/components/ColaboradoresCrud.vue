<template>
  <div class="space-y-6">
    <!-- Header com botão de adicionar -->
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold text-text-primary">Colaboradores</h2>
      <button 
        @click="abrirModal()" 
        class="bg-primary-main text-white px-4 py-2 rounded-sm text-sm font-medium hover:bg-primary-light transition-colors"
      >
        Novo Colaborador
      </button>
    </div>

    <!-- Tabs -->
    <div class="bg-white rounded-md shadow-sm overflow-hidden">
      <div class="border-b border-gray-200">
        <nav class="flex space-x-4 px-4">
          <button
            v-if="selectedSquadId"
            @click="activeTab = 'squad'"
            :class="[
              'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'squad'
                ? 'border-orange-500 text-orange-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Membros do Squad ({{ squadMembers.length }})
          </button>
          <button
            @click="activeTab = 'transversal'"
            :class="[
              'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'transversal'
                ? 'border-purple-500 text-purple-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Transversais ({{ transversalMembers.length }})
          </button>
          <button
            @click="activeTab = 'others'"
            :class="[
              'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === 'others'
                ? 'border-gray-500 text-gray-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Outros ({{ otherMembers.length }})
          </button>
        </nav>
      </div>

      <!-- Squad Members Table -->
      <div v-if="activeTab === 'squad' && selectedSquadId">
      <div v-if="squadMembers.length === 0" class="p-8 text-center text-text-secondary">
        Nenhum membro encontrado para este squad
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cargo</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Habilidades</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ausências</th>
            <th class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="colaborador in squadMembers" :key="colaborador.id" class="hover:bg-gray-50">
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ colaborador.nome }}</div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span class="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {{ colaborador.cargo.nome }}
              </span>
            </td>
            <td class="px-4 py-2">
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="habilidade in colaborador.habilidades" 
                  :key="habilidade.id"
                  class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                >
                  {{ habilidade.nome }}
                </span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
              {{ colaborador.ausencias.length }}
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button 
                  @click="abrirModal(colaborador)" 
                  class="text-indigo-600 hover:text-indigo-900 p-1"
                  title="Editar"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button 
                  @click="confirmarExclusao(colaborador)" 
                  class="text-red-600 hover:text-red-900 p-1"
                  title="Excluir"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      </div>

      <!-- Transversal Members Table -->
      <div v-if="activeTab === 'transversal'">

      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cargo</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Habilidades</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ausências</th>
            <th class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="colaborador in transversalMembers" :key="colaborador.id" class="hover:bg-gray-50">
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ colaborador.nome }}</div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span class="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {{ colaborador.cargo.nome }}
              </span>
            </td>
            <td class="px-4 py-2">
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="habilidade in colaborador.habilidades" 
                  :key="habilidade.id"
                  class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                >
                  {{ habilidade.nome }}
                </span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
              {{ colaborador.ausencias.length }}
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button 
                  @click="abrirModal(colaborador)" 
                  class="text-indigo-600 hover:text-indigo-900 p-1"
                  title="Editar"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button 
                  @click="confirmarExclusao(colaborador)" 
                  class="text-red-600 hover:text-red-900 p-1"
                  title="Excluir"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      </div>

      <!-- Other Members Table -->
      <div v-if="activeTab === 'others'">
      <div class="bg-gray-50 px-4 py-3 border-b border-gray-200">
        <div class="flex items-center justify-end mb-2">
          <button 
            v-if="filterSquadId || filterHabilidades.length > 0"
            @click="clearFilters" 
            class="text-xs text-primary-main hover:underline"
          >
            Limpar filtros
          </button>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <select 
              v-model="filterSquadId" 
              class="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-primary-main"
            >
              <option :value="null">Todos os squads</option>
              <option v-for="squad in squads" :key="squad.id" :value="squad.id">
                {{ squad.nome }}
              </option>
            </select>
          </div>
          <div class="border border-gray-300 rounded px-2 py-1 bg-white max-h-[60px] overflow-y-auto">
            <div class="flex flex-wrap gap-1">
              <span 
                v-for="habilidade in habilidadesOrdenadas" 
                :key="habilidade.id"
                @click="toggleFilterHabilidade(habilidade.id)"
                class="text-xs px-1.5 py-0.5 rounded cursor-pointer transition-colors"
                :class="filterHabilidades.includes(habilidade.id) ? 'bg-green-100 text-green-700 font-medium' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
              >
                {{ habilidade.nome }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cargo</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Squad</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Habilidades</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ausências</th>
            <th class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="colaborador in otherMembers" :key="colaborador.id" class="hover:bg-gray-50">
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ colaborador.nome }}</div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span class="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {{ colaborador.cargo.nome }}
              </span>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span v-if="colaborador.squad" class="px-2 py-0.5 text-xs font-medium bg-orange-100 text-orange-800 rounded-full">
                {{ colaborador.squad.nome }}
              </span>
              <span v-else class="text-xs text-gray-400">-</span>
            </td>
            <td class="px-4 py-2">
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="habilidade in colaborador.habilidades" 
                  :key="habilidade.id"
                  class="px-2 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                >
                  {{ habilidade.nome }}
                </span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
              {{ colaborador.ausencias.length }}
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button 
                  @click="abrirModal(colaborador)" 
                  class="text-indigo-600 hover:text-indigo-900 p-1"
                  title="Editar"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button 
                  @click="confirmarExclusao(colaborador)" 
                  class="text-red-600 hover:text-red-900 p-1"
                  title="Excluir"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="otherMembers.length === 0" class="p-8 text-center text-text-secondary">
        Nenhum colaborador encontrado com os filtros aplicados
      </div>
      </div>
    </div>

    <!-- Modal de edição/criação -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" style="margin: 0; padding: 16px;">
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[95vh] flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold">{{ editandoColaborador ? 'Editar Colaborador' : 'Novo Colaborador' }}</h3>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-4">
          <form @submit.prevent="salvarColaborador" class="space-y-3">
            <!-- Nome e Cargo -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-text-primary mb-1">Nome</label>
                <input 
                  v-model="form.nome" 
                  type="text" 
                  required
                  class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-main"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-text-primary mb-1">Cargo</label>
                <select 
                  v-model="form.cargo_id" 
                  required
                  class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-main"
                >
                  <option value="">Selecionar cargo</option>
                  <option v-for="cargo in cargos" :key="cargo.id" :value="cargo.id">
                    {{ cargo.nome }}
                  </option>
                </select>
              </div>
            </div>
            
            <!-- Transversal e Squad -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-text-primary mb-1">Tipo</label>
                <label class="flex items-center space-x-2 cursor-pointer px-3 py-1.5 border border-gray-300 rounded-md hover:bg-gray-50">
                  <input 
                    type="checkbox" 
                    v-model="form.transversal"
                    @change="onTransversalChange"
                    class="w-4 h-4 text-purple-600 rounded border-gray-300 focus:ring-purple-500"
                  />
                  <span class="text-sm">Transversal</span>
                </label>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-text-primary mb-1">Squad</label>
                <select 
                  v-model="form.squad_id" 
                  :disabled="form.transversal"
                  class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-main disabled:bg-gray-100 disabled:cursor-not-allowed"
                >
                  <option :value="null">Selecionar squad</option>
                  <option v-for="squad in squads" :key="squad.id" :value="squad.id">
                    {{ squad.nome }} ({{ squad.tribo.nome }})
                  </option>
                </select>
              </div>
            </div>
            
            <!-- Habilidades -->
            <div>
              <label class="block text-sm font-medium text-text-primary mb-1">Habilidades ({{ form.habilidades_ids.length }} selecionadas)</label>
              <div class="border border-gray-200 rounded-md p-2 bg-white min-h-[80px] max-h-[120px] overflow-y-auto">
                <div class="flex flex-wrap gap-1">
                  <span 
                    v-for="habilidade in habilidadesOrdenadas" 
                    :key="habilidade.id"
                    @click="toggleHabilidade(habilidade.id)"
                    class="text-xs px-2 py-1 rounded cursor-pointer transition-colors"
                    :class="form.habilidades_ids.includes(habilidade.id) ? 'bg-green-100 text-green-700 font-medium' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                  >
                    {{ habilidade.nome }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Ausências -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <label class="block text-sm font-medium text-text-primary">Ausências</label>
                <button 
                  type="button" 
                  @click="adicionarAusencia" 
                  class="text-primary-main hover:text-primary-light text-xs font-medium"
                >
                  + Adicionar
                </button>
              </div>
              <div class="space-y-1.5">
                <div v-for="(ausencia, index) in form.ausencias" :key="index" class="flex items-center space-x-2">
                  <input 
                    v-model="ausencia.data" 
                    type="date" 
                    required
                    class="flex-1 px-2 py-1.5 border border-gray-300 rounded-md text-xs focus:outline-none focus:ring-1 focus:ring-primary-main"
                  />
                  <button 
                    type="button" 
                    @click="removerAusencia(index)" 
                    class="text-red-500 hover:text-red-700 p-0.5"
                    title="Remover"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
        
        <!-- Footer -->
        <div class="flex justify-end space-x-3 p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
          <button 
            type="button" 
            @click="fecharModal" 
            class="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 font-medium"
          >
            Cancelar
          </button>
          <button 
            @click="salvarColaborador"
            :disabled="salvando"
            class="px-6 py-2 bg-primary-main text-white rounded-md hover:bg-primary-light disabled:opacity-50 font-medium flex items-center space-x-2"
          >
            <svg v-if="salvando" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ salvando ? 'Salvando...' : 'Salvar Colaborador' }}</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal de confirmação -->
    <ConfirmModal 
      :show="showConfirmModal"
      :title="'Confirmar exclusão'"
      :message="`Tem certeza que deseja excluir o colaborador '${itemParaExcluir?.nome}'?`"
      @confirm="executarExclusao"
      @cancel="cancelarExclusao"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ConfirmModal from './ConfirmModal.vue'

export default {
  name: 'ColaboradoresCrud',
  components: {
    ConfirmModal
  },
  props: {
    selectedSquadId: {
      type: Number,
      default: null
    },
    allColaboradores: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      cargos: [],
      habilidades: [],
      squads: [],
      loading: false,
      salvando: false,
      showModal: false,
      editandoColaborador: null,
      form: {
        nome: '',
        cargo_id: '',
        squad_id: null,
        transversal: false,
        habilidades_ids: [],
        ausencias: []
      },
      showConfirmModal: false,
      itemParaExcluir: null,
      filterSquadId: null,
      filterHabilidades: [],
      activeTab: 'squad'
    }
  },
  computed: {
    squadMembers() {
      if (!this.selectedSquadId) return []
      return this.allColaboradores
        .filter(c => !c.transversal && c.squad?.id == this.selectedSquadId)
        .sort((a, b) => a.nome.localeCompare(b.nome))
    },
    transversalMembers() {
      return this.allColaboradores
        .filter(c => c.transversal)
        .sort((a, b) => a.nome.localeCompare(b.nome))
    },
    otherMembers() {
      let filtered = this.allColaboradores
        .filter(c => {
          if (c.transversal) return false
          if (this.selectedSquadId && c.squad?.id === this.selectedSquadId) return false
          return true
        })
      
      if (this.filterSquadId) {
        filtered = filtered.filter(c => c.squad?.id === this.filterSquadId)
      }
      
      if (this.filterHabilidades.length > 0) {
        filtered = filtered.filter(c => 
          this.filterHabilidades.every(habId => 
            c.habilidades.some(h => h.id === habId)
          )
        )
      }
      
      return filtered.sort((a, b) => a.nome.localeCompare(b.nome))
    },
    habilidadesOrdenadas() {
      return [...this.habilidades].sort((a, b) => a.nome.localeCompare(b.nome))
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  
  watch: {
    showModal(newVal) {
      if (newVal) {
        document.addEventListener('keydown', this.handleEscKey)
      } else {
        document.removeEventListener('keydown', this.handleEscKey)
      }
    },
    selectedSquadId() {
      this.clearFilters()
    }
  },
  methods: {
    async carregarDados() {
      this.loading = true
      try {
        const [cargosRes, habilidadesRes, squadsRes] = await Promise.all([
          axios.get('/api/cargos'),
          axios.get('/api/habilidades'),
          axios.get('/api/squads')
        ])
        this.cargos = cargosRes.data
        this.habilidades = habilidadesRes.data
        this.squads = squadsRes.data
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    reloadColaboradores() {
      this.$emit('reload')
    },
    
    abrirModal(colaborador = null) {
      this.editandoColaborador = colaborador
      if (colaborador) {
        this.form = {
          nome: colaborador.nome,
          cargo_id: colaborador.cargo.id,
          squad_id: colaborador.squad?.id || null,
          transversal: colaborador.transversal || false,
          habilidades_ids: colaborador.habilidades.map(h => h.id),
          ausencias: colaborador.ausencias.map(a => ({ data: a.data }))
        }
      } else {
        this.form = {
          nome: '',
          cargo_id: '',
          squad_id: null,
          transversal: false,
          habilidades_ids: [],
          ausencias: []
        }
      }
      this.showModal = true
    },
    
    fecharModal() {
      this.showModal = false
      this.editandoColaborador = null
    },
    
    adicionarAusencia() {
      this.form.ausencias.push({ data: '' })
    },
    
    removerAusencia(index) {
      this.form.ausencias.splice(index, 1)
    },
    
    async salvarColaborador() {
      this.salvando = true
      try {
        if (this.editandoColaborador) {
          await axios.put(`/api/colaboradores/${this.editandoColaborador.id}`, this.form)
        } else {
          await axios.post('/api/colaboradores', this.form)
        }
        this.reloadColaboradores()
        this.fecharModal()
      } catch (error) {
        console.error('Erro ao salvar colaborador:', error)
        alert('Erro ao salvar colaborador. Verifique os dados e tente novamente.')
      } finally {
        this.salvando = false
      }
    },
    
    confirmarExclusao(colaborador) {
      this.itemParaExcluir = colaborador
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        await axios.delete(`/api/colaboradores/${this.itemParaExcluir.id}`)
        this.reloadColaboradores()
        this.cancelarExclusao()
      } catch (error) {
        console.error('Erro ao excluir colaborador:', error)
        this.cancelarExclusao()
      }
    },
    
    toggleHabilidade(habilidadeId) {
      const index = this.form.habilidades_ids.indexOf(habilidadeId)
      if (index > -1) {
        this.form.habilidades_ids.splice(index, 1)
      } else {
        this.form.habilidades_ids.push(habilidadeId)
      }
    },
    toggleFilterHabilidade(habilidadeId) {
      const index = this.filterHabilidades.indexOf(habilidadeId)
      if (index > -1) {
        this.filterHabilidades.splice(index, 1)
      } else {
        this.filterHabilidades.push(habilidadeId)
      }
    },
    clearFilters() {
      this.filterSquadId = null
      this.filterHabilidades = []
    },
    
    onTransversalChange() {
      if (this.form.transversal) {
        this.form.squad_id = null
      }
    },
    
    handleEscKey(event) {
      if (event.key === 'Escape' && this.showModal) {
        this.fecharModal()
      }
    },
    
    cancelarExclusao() {
      this.showConfirmModal = false
      this.itemParaExcluir = null
    }
  }
}
</script>