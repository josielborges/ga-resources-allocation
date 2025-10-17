<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-semibold text-text-primary">Tribos & Squads</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Tribos Section -->
      <div class="bg-white rounded-md shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-3 py-2">
          <h3 class="text-white font-medium text-sm">Tribos</h3>
        </div>
        
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-main mx-auto"></div>
          <p class="mt-2 text-text-secondary text-sm">Carregando...</p>
        </div>
        
        <div v-else class="p-3 space-y-1.5">
          <div 
            v-for="tribo in tribosOrdenadas" 
            :key="tribo.id"
            @click="selecionarTribo(tribo)"
            class="group p-2 border rounded-md cursor-pointer transition-all"
            :class="triboSelecionada?.id === tribo.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'"
          >
            <div v-if="editandoTribo === tribo.id" @click.stop class="flex items-center space-x-2">
              <input 
                v-model="nomeEditandoTribo"
                @keyup.enter="salvarEdicaoTribo(tribo)"
                @keyup.escape="cancelarEdicaoTribo"
                class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                ref="inputEditTribo"
              />
              <button @click="salvarEdicaoTribo(tribo)" class="text-green-600 hover:text-green-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </button>
              <button @click="cancelarEdicaoTribo" class="text-gray-600 hover:text-gray-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-else class="flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium text-sm text-gray-900">{{ tribo.nome }}</div>
                <div class="text-xs text-gray-500 mt-0.5">{{ getSquadCount(tribo.id) }} squads</div>
              </div>
              <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click.stop="iniciarEdicaoTribo(tribo)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click.stop="confirmarExclusaoTribo(tribo)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Add Tribo -->
          <div class="p-2 border-2 border-dashed border-blue-300 rounded-md bg-blue-50">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              <input 
                v-model="novaTribo"
                @keyup.enter="adicionarTribo"
                placeholder="Nova tribo..."
                class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button 
                @click="adicionarTribo"
                :disabled="!novaTribo.trim()"
                class="bg-blue-600 text-white px-2 py-0.5 rounded text-xs font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Adicionar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Squads Section -->
      <div class="bg-white rounded-md shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 px-3 py-2 flex justify-between items-center">
          <h3 class="text-white font-medium text-sm">
            Squads
            <span v-if="triboSelecionada" class="text-orange-100 text-xs ml-2">
              - {{ triboSelecionada.nome }}
            </span>
            <span v-else-if="mostrarTodas" class="text-orange-100 text-xs ml-2">
              - Todas
            </span>
          </h3>
          <button 
            @click="toggleMostrarTodas"
            class="text-white text-xs px-2 py-0.5 rounded bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors"
          >
            {{ mostrarTodas ? 'Ocultar' : 'Ver Todas' }}
          </button>
        </div>
        
        <div v-if="!triboSelecionada && !mostrarTodas" class="p-6 text-center text-gray-500">
          <svg class="w-10 h-10 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          <p class="text-sm">Selecione uma tribo para ver suas squads</p>
        </div>
        
        <div v-else class="p-3 space-y-1.5">
          <div 
            v-for="squad in squadsFiltradasOrdenadas" 
            :key="squad.id"
            class="group p-2 border border-gray-200 rounded-md hover:border-orange-300 hover:bg-gray-50 transition-all"
          >
            <div v-if="editandoSquad === squad.id" class="flex items-center space-x-2">
              <input 
                v-model="nomeEditandoSquad"
                @keyup.enter="salvarEdicaoSquad(squad)"
                @keyup.escape="cancelarEdicaoSquad"
                class="flex-1 px-2 py-0.5 text-xs border border-orange-300 rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
                ref="inputEditSquad"
              />
              <button @click="salvarEdicaoSquad(squad)" class="text-green-600 hover:text-green-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </button>
              <button @click="cancelarEdicaoSquad" class="text-gray-600 hover:text-gray-800 p-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-else class="flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium text-sm text-gray-900">{{ squad.nome }}</div>
                <div v-if="mostrarTodas" class="text-xs text-gray-500 mt-0.5">{{ squad.tribo.nome }}</div>
              </div>
              <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click="iniciarEdicaoSquad(squad)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click="confirmarExclusaoSquad(squad)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Add Squad -->
          <div v-if="triboSelecionada" class="p-2 border-2 border-dashed border-orange-300 rounded-md bg-orange-50">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              <input 
                v-model="novaSquad"
                @keyup.enter="adicionarSquad"
                placeholder="Nova squad..."
                class="flex-1 px-2 py-0.5 text-xs border border-orange-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <button 
                @click="adicionarSquad"
                :disabled="!novaSquad.trim()"
                class="bg-orange-600 text-white px-2 py-0.5 rounded text-xs font-medium hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed"
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
import ConfirmModal from '../modals/ConfirmModal.vue'
import NotificationModal from '../modals/NotificationModal.vue'

export default {
  name: 'TribosSquadsCrud',
  components: {
    ConfirmModal,
    NotificationModal
  },
  data() {
    return {
      tribos: [],
      squads: [],
      loading: false,
      triboSelecionada: null,
      mostrarTodas: false,
      editandoTribo: null,
      nomeEditandoTribo: '',
      editandoSquad: null,
      nomeEditandoSquad: '',
      novaTribo: '',
      novaSquad: '',
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
    tribosOrdenadas() {
      return [...this.tribos].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    squadsFiltradasOrdenadas() {
      if (this.mostrarTodas) {
        return [...this.squads].sort((a, b) => a.nome.localeCompare(b.nome))
      }
      if (!this.triboSelecionada) return []
      return [...this.squads]
        .filter(s => s.tribo.id === this.triboSelecionada.id)
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
        const [tribosRes, squadsRes] = await Promise.all([
          axios.get('/api/tribos'),
          axios.get('/api/squads')
        ])
        this.tribos = tribosRes.data
        this.squads = squadsRes.data
        
        if (this.triboSelecionada) {
          this.triboSelecionada = this.tribos.find(t => t.id === this.triboSelecionada.id)
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    
    getSquadCount(triboId) {
      return this.squads.filter(s => s.tribo.id === triboId).length
    },
    
    selecionarTribo(tribo) {
      this.triboSelecionada = tribo
      this.mostrarTodas = false
    },
    
    toggleMostrarTodas() {
      this.mostrarTodas = !this.mostrarTodas
      if (this.mostrarTodas) {
        this.triboSelecionada = null
      }
    },
    
    // Tribo methods
    iniciarEdicaoTribo(tribo) {
      this.editandoTribo = tribo.id
      this.nomeEditandoTribo = tribo.nome
      this.$nextTick(() => {
        this.$refs.inputEditTribo?.[0]?.focus()
      })
    },
    
    cancelarEdicaoTribo() {
      this.editandoTribo = null
      this.nomeEditandoTribo = ''
    },
    
    async salvarEdicaoTribo(tribo) {
      if (!this.nomeEditandoTribo.trim()) {
        this.cancelarEdicaoTribo()
        return
      }
      try {
        const response = await axios.put(`/api/tribos/${tribo.id}`, { 
          nome: this.nomeEditandoTribo.trim()
        })
        const index = this.tribos.findIndex(t => t.id === tribo.id)
        if (index !== -1) {
          this.tribos[index] = response.data
        }
        if (this.triboSelecionada?.id === tribo.id) {
          this.triboSelecionada = response.data
        }
        this.cancelarEdicaoTribo()
      } catch (error) {
        console.error('Erro ao salvar tribo:', error)
        this.cancelarEdicaoTribo()
      }
    },
    
    async adicionarTribo() {
      if (!this.novaTribo.trim()) return
      try {
        const response = await axios.post('/api/tribos', { 
          nome: this.novaTribo.trim()
        })
        this.tribos.push(response.data)
        this.novaTribo = ''
      } catch (error) {
        console.error('Erro ao adicionar tribo:', error)
      }
    },
    
    confirmarExclusaoTribo(tribo) {
      this.itemParaExcluir = tribo
      this.tipoExclusao = 'tribo'
      this.confirmModalTitle = 'Confirmar exclusão'
      this.confirmModalMessage = `Tem certeza que deseja excluir a tribo '${tribo.nome}'?`
      this.showConfirmModal = true
    },
    
    // Squad methods
    iniciarEdicaoSquad(squad) {
      this.editandoSquad = squad.id
      this.nomeEditandoSquad = squad.nome
      this.$nextTick(() => {
        this.$refs.inputEditSquad?.[0]?.focus()
      })
    },
    
    cancelarEdicaoSquad() {
      this.editandoSquad = null
      this.nomeEditandoSquad = ''
    },
    
    async salvarEdicaoSquad(squad) {
      if (!this.nomeEditandoSquad.trim()) {
        this.cancelarEdicaoSquad()
        return
      }
      try {
        const response = await axios.put(`/api/squads/${squad.id}`, { 
          nome: this.nomeEditandoSquad.trim(),
          tribo_id: squad.tribo.id
        })
        const index = this.squads.findIndex(s => s.id === squad.id)
        if (index !== -1) {
          this.squads[index] = response.data
        }
        this.cancelarEdicaoSquad()
      } catch (error) {
        console.error('Erro ao salvar squad:', error)
        this.cancelarEdicaoSquad()
      }
    },
    
    async adicionarSquad() {
      if (!this.novaSquad.trim() || !this.triboSelecionada) return
      try {
        const response = await axios.post('/api/squads', { 
          nome: this.novaSquad.trim(),
          tribo_id: this.triboSelecionada.id
        })
        this.squads.push(response.data)
        this.novaSquad = ''
      } catch (error) {
        console.error('Erro ao adicionar squad:', error)
      }
    },
    
    confirmarExclusaoSquad(squad) {
      this.itemParaExcluir = squad
      this.tipoExclusao = 'squad'
      this.confirmModalTitle = 'Confirmar exclusão'
      this.confirmModalMessage = `Tem certeza que deseja excluir a squad '${squad.nome}'?`
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        if (this.tipoExclusao === 'tribo') {
          await axios.delete(`/api/tribos/${this.itemParaExcluir.id}`)
          const index = this.tribos.findIndex(t => t.id === this.itemParaExcluir.id)
          if (index !== -1) {
            this.tribos.splice(index, 1)
          }
          if (this.triboSelecionada?.id === this.itemParaExcluir.id) {
            this.triboSelecionada = null
          }
        } else {
          await axios.delete(`/api/squads/${this.itemParaExcluir.id}`)
          const index = this.squads.findIndex(s => s.id === this.itemParaExcluir.id)
          if (index !== -1) {
            this.squads.splice(index, 1)
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
