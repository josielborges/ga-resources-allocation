<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-semibold text-text-primary">Cargos & Habilidades</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Cargos Section -->
      <div class="bg-white rounded-md shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-purple-500 to-purple-600 px-3 py-2">
          <h3 class="text-white font-medium text-sm">Cargos</h3>
        </div>
        
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-main mx-auto"></div>
          <p class="mt-2 text-text-secondary text-sm">Carregando...</p>
        </div>
        
        <div v-else class="p-3 space-y-1.5">
          <div 
            v-for="cargo in cargosOrdenados" 
            :key="cargo.id"
            @click="selecionarCargo(cargo)"
            class="group p-2 border rounded-md cursor-pointer transition-all"
            :class="cargoSelecionado?.id === cargo.id ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'"
          >
            <div v-if="editandoCargo === cargo.id" @click.stop class="flex items-center space-x-2">
              <input 
                v-model="nomeEditandoCargo"
                @keyup.enter="salvarEdicaoCargo(cargo)"
                @keyup.escape="cancelarEdicaoCargo"
                class="flex-1 px-2 py-0.5 text-xs border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
                ref="inputEditCargo"
              />
              <button @click="salvarEdicaoCargo(cargo)" class="text-green-600 hover:text-green-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </button>
              <button @click="cancelarEdicaoCargo" class="text-gray-600 hover:text-gray-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-else class="flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium text-sm text-gray-900">{{ cargo.nome }}</div>
                <div class="text-xs text-gray-500 mt-0.5">{{ getHabilidadeCount(cargo.id) }} habilidades</div>
              </div>
              <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click.stop="iniciarEdicaoCargo(cargo)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click.stop="confirmarExclusaoCargo(cargo)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Add Cargo -->
          <div class="p-2 border-2 border-dashed border-purple-300 rounded-md bg-purple-50">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              <input 
                v-model="novoCargo"
                @keyup.enter="adicionarCargo"
                placeholder="Novo cargo..."
                class="flex-1 px-2 py-0.5 text-xs border border-purple-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button 
                @click="adicionarCargo"
                :disabled="!novoCargo.trim()"
                class="bg-purple-600 text-white px-2 py-0.5 rounded text-xs font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Adicionar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Habilidades Section -->
      <div class="bg-white rounded-md shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-green-500 to-green-600 px-3 py-2">
          <h3 class="text-white font-medium text-sm">
            Habilidades
            <span v-if="cargoSelecionado" class="text-green-100 text-xs ml-2">
              - {{ cargoSelecionado.nome }}
            </span>
          </h3>
        </div>
        
        <div v-if="!cargoSelecionado" class="p-6 text-center text-gray-500">
          <svg class="w-10 h-10 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
          <p class="text-sm">Selecione um cargo para ver suas habilidades</p>
        </div>
        
        <div v-else class="p-3 space-y-1.5">
          <div 
            v-for="habilidade in habilidadesFiltradasOrdenadas" 
            :key="habilidade.id"
            class="group p-2 border border-gray-200 rounded-md hover:border-green-300 hover:bg-gray-50 transition-all"
          >
            <div v-if="editandoHabilidade === habilidade.id" class="flex items-center space-x-2">
              <input 
                v-model="nomeEditandoHabilidade"
                @keyup.enter="salvarEdicaoHabilidade(habilidade)"
                @keyup.escape="cancelarEdicaoHabilidade"
                class="flex-1 px-2 py-0.5 text-xs border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
                ref="inputEditHabilidade"
              />
              <button @click="salvarEdicaoHabilidade(habilidade)" class="text-green-600 hover:text-green-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </button>
              <button @click="cancelarEdicaoHabilidade" class="text-gray-600 hover:text-gray-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-else class="flex items-center justify-between">
              <div class="font-medium text-sm text-gray-900">{{ habilidade.nome }}</div>
              <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click="iniciarEdicaoHabilidade(habilidade)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click="confirmarExclusaoHabilidade(habilidade)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Add Habilidade -->
          <div class="p-2 border-2 border-dashed border-green-300 rounded-md bg-green-50">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              <input 
                v-model="novaHabilidade"
                @keyup.enter="adicionarHabilidade"
                placeholder="Nova habilidade..."
                class="flex-1 px-2 py-0.5 text-xs border border-green-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <button 
                @click="adicionarHabilidade"
                :disabled="!novaHabilidade.trim()"
                class="bg-green-600 text-white px-2 py-0.5 rounded text-xs font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Adicionar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <ConfirmModal 
      :show="showConfirmModal"
      :title="confirmModalTitle"
      :message="confirmModalMessage"
      @confirm="executarExclusao"
      @cancel="cancelarExclusao"
    />
    
    <NotificationModal 
      :show="showNotification"
      :title="notificationTitle"
      :message="notificationMessage"
      @close="fecharNotificacao"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ConfirmModal from './ConfirmModal.vue'
import NotificationModal from './NotificationModal.vue'

export default {
  name: 'CargosHabilidadesCrud',
  components: {
    ConfirmModal,
    NotificationModal
  },
  data() {
    return {
      cargos: [],
      habilidades: [],
      loading: false,
      cargoSelecionado: null,
      editandoCargo: null,
      nomeEditandoCargo: '',
      editandoHabilidade: null,
      nomeEditandoHabilidade: '',
      novoCargo: '',
      novaHabilidade: '',
      showConfirmModal: false,
      confirmModalTitle: '',
      confirmModalMessage: '',
      itemParaExcluir: null,
      tipoExclusao: null,
      showNotification: false,
      notificationTitle: '',
      notificationMessage: ''
    }
  },
  computed: {
    cargosOrdenados() {
      return [...this.cargos].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    habilidadesFiltradasOrdenadas() {
      if (!this.cargoSelecionado) return []
      return [...this.habilidades]
        .filter(h => h.cargo.id === this.cargoSelecionado.id)
        .sort((a, b) => a.nome.localeCompare(b.nome))
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      this.loading = true
      try {
        const [cargosRes, habilidadesRes] = await Promise.all([
          axios.get('/api/cargos'),
          axios.get('/api/habilidades')
        ])
        this.cargos = cargosRes.data
        this.habilidades = habilidadesRes.data
        
        if (this.cargoSelecionado) {
          this.cargoSelecionado = this.cargos.find(c => c.id === this.cargoSelecionado.id)
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    
    getHabilidadeCount(cargoId) {
      return this.habilidades.filter(h => h.cargo.id === cargoId).length
    },
    
    selecionarCargo(cargo) {
      this.cargoSelecionado = cargo
    },
    
    // Cargo methods
    iniciarEdicaoCargo(cargo) {
      this.editandoCargo = cargo.id
      this.nomeEditandoCargo = cargo.nome
      this.$nextTick(() => {
        this.$refs.inputEditCargo?.[0]?.focus()
      })
    },
    
    cancelarEdicaoCargo() {
      this.editandoCargo = null
      this.nomeEditandoCargo = ''
    },
    
    async salvarEdicaoCargo(cargo) {
      if (!this.nomeEditandoCargo.trim()) {
        this.cancelarEdicaoCargo()
        return
      }
      try {
        const response = await axios.put(`/api/cargos/${cargo.id}`, { 
          nome: this.nomeEditandoCargo.trim()
        })
        const index = this.cargos.findIndex(c => c.id === cargo.id)
        if (index !== -1) {
          this.cargos[index] = response.data
        }
        if (this.cargoSelecionado?.id === cargo.id) {
          this.cargoSelecionado = response.data
        }
        this.cancelarEdicaoCargo()
      } catch (error) {
        console.error('Erro ao salvar cargo:', error)
        this.cancelarEdicaoCargo()
      }
    },
    
    async adicionarCargo() {
      if (!this.novoCargo.trim()) return
      try {
        const response = await axios.post('/api/cargos', { 
          nome: this.novoCargo.trim()
        })
        this.cargos.push(response.data)
        this.novoCargo = ''
      } catch (error) {
        console.error('Erro ao adicionar cargo:', error)
      }
    },
    
    confirmarExclusaoCargo(cargo) {
      this.itemParaExcluir = cargo
      this.tipoExclusao = 'cargo'
      this.confirmModalTitle = 'Confirmar exclusão'
      this.confirmModalMessage = `Tem certeza que deseja excluir o cargo '${cargo.nome}'?`
      this.showConfirmModal = true
    },
    
    // Habilidade methods
    iniciarEdicaoHabilidade(habilidade) {
      this.editandoHabilidade = habilidade.id
      this.nomeEditandoHabilidade = habilidade.nome
      this.$nextTick(() => {
        this.$refs.inputEditHabilidade?.[0]?.focus()
      })
    },
    
    cancelarEdicaoHabilidade() {
      this.editandoHabilidade = null
      this.nomeEditandoHabilidade = ''
    },
    
    async salvarEdicaoHabilidade(habilidade) {
      if (!this.nomeEditandoHabilidade.trim()) {
        this.cancelarEdicaoHabilidade()
        return
      }
      try {
        const response = await axios.put(`/api/habilidades/${habilidade.id}`, { 
          nome: this.nomeEditandoHabilidade.trim(),
          cargo_id: habilidade.cargo.id
        })
        const index = this.habilidades.findIndex(h => h.id === habilidade.id)
        if (index !== -1) {
          this.habilidades[index] = response.data
        }
        this.cancelarEdicaoHabilidade()
      } catch (error) {
        console.error('Erro ao salvar habilidade:', error)
        this.cancelarEdicaoHabilidade()
      }
    },
    
    async adicionarHabilidade() {
      if (!this.novaHabilidade.trim() || !this.cargoSelecionado) return
      try {
        const response = await axios.post('/api/habilidades', { 
          nome: this.novaHabilidade.trim(),
          cargo_id: this.cargoSelecionado.id
        })
        this.habilidades.push(response.data)
        this.novaHabilidade = ''
      } catch (error) {
        console.error('Erro ao adicionar habilidade:', error)
      }
    },
    
    confirmarExclusaoHabilidade(habilidade) {
      this.itemParaExcluir = habilidade
      this.tipoExclusao = 'habilidade'
      this.confirmModalTitle = 'Confirmar exclusão'
      this.confirmModalMessage = `Tem certeza que deseja excluir a habilidade '${habilidade.nome}'?`
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        if (this.tipoExclusao === 'cargo') {
          await axios.delete(`/api/cargos/${this.itemParaExcluir.id}`)
          const index = this.cargos.findIndex(c => c.id === this.itemParaExcluir.id)
          if (index !== -1) {
            this.cargos.splice(index, 1)
          }
          if (this.cargoSelecionado?.id === this.itemParaExcluir.id) {
            this.cargoSelecionado = null
          }
        } else {
          await axios.delete(`/api/habilidades/${this.itemParaExcluir.id}`)
          const index = this.habilidades.findIndex(h => h.id === this.itemParaExcluir.id)
          if (index !== -1) {
            this.habilidades.splice(index, 1)
          }
        }
        this.cancelarExclusao()
      } catch (error) {
        console.error('Erro ao excluir:', error)
        if (error.response?.status === 400) {
          this.notificationTitle = 'Não é possível excluir'
          this.notificationMessage = error.response.data.detail
          this.showNotification = true
        }
        this.cancelarExclusao()
      }
    },
    
    cancelarExclusao() {
      this.showConfirmModal = false
      this.itemParaExcluir = null
      this.tipoExclusao = null
    },
    
    fecharNotificacao() {
      this.showNotification = false
      this.notificationTitle = ''
      this.notificationMessage = ''
    }
  }
}
</script>
