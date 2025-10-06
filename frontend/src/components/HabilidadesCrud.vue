<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold text-text-primary">Habilidades</h2>
      <div class="flex items-center space-x-2">
        <label class="text-sm font-medium text-gray-700">Filtrar por cargo:</label>
        <select 
          v-model="cargoSelecionado" 
          @change="carregarDados"
          class="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-main"
        >
          <option value="">Todos os cargos</option>
          <option v-for="cargo in cargosOrdenados" :key="cargo.id" :value="cargo.id">
            {{ cargo.nome }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tabela de habilidades -->
    <div class="bg-white rounded-md shadow-sm overflow-hidden">
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-main mx-auto"></div>
        <p class="mt-2 text-text-secondary">Carregando habilidades...</p>
      </div>
      
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th @click="ordenarPor('cargo')" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
              <div class="flex items-center space-x-1">
                <span>Cargo</span>
                <svg v-if="ordenacao.campo === 'cargo'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path v-if="ordenacao.direcao === 'asc'" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                  <path v-else d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"/>
                </svg>
              </div>
            </th>
            <th @click="ordenarPor('nome')" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
              <div class="flex items-center space-x-1">
                <span>Nome</span>
                <svg v-if="ordenacao.campo === 'nome'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path v-if="ordenacao.direcao === 'asc'" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                  <path v-else d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"/>
                </svg>
              </div>
            </th>
            <th class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="habilidade in habilidadesOrdenadas" :key="habilidade.id" class="hover:bg-gray-50">
            <td class="px-4 py-2">
              <select 
                v-if="editando === habilidade.id"
                v-model="cargoEditando"
                class="w-full px-3 py-1.5 text-sm border border-blue-300 rounded-md bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option v-for="cargo in cargosOrdenados" :key="cargo.id" :value="cargo.id">
                  {{ cargo.nome }}
                </option>
              </select>
              <div v-else class="text-sm text-gray-900 py-1">{{ habilidade.cargo.nome }}</div>
            </td>
            <td class="px-4 py-2">
              <input 
                v-if="editando === habilidade.id"
                v-model="nomeEditando"
                @keyup.enter="salvarEdicao(habilidade)"
                @keyup.escape="cancelarEdicao"
                class="w-full px-3 py-1.5 text-sm border border-blue-300 rounded-md bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                ref="inputEdit"
              />
              <div v-else class="text-sm font-medium text-gray-900 py-1">{{ habilidade.nome }}</div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <template v-if="editando === habilidade.id">
                  <button 
                    @click="salvarEdicao(habilidade)"
                    class="text-green-600 hover:text-green-800 p-1.5 rounded-md hover:bg-green-50 transition-colors"
                    title="Salvar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </button>
                  <button 
                    @click="cancelarEdicao"
                    class="text-gray-600 hover:text-gray-800 p-1.5 rounded-md hover:bg-gray-50 transition-colors"
                    title="Cancelar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </template>
                <template v-else>
                  <button 
                    @click="iniciarEdicao(habilidade)" 
                    class="text-blue-600 hover:text-blue-800 p-1.5 rounded-md hover:bg-blue-50 transition-colors"
                    title="Editar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button 
                    @click="confirmarExclusao(habilidade)" 
                    class="text-red-600 hover:text-red-900 p-1"
                    title="Excluir"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </template>
              </div>
            </td>
          </tr>
          <!-- Linha para adicionar nova habilidade -->
          <tr class="bg-blue-50 border-t-2 border-blue-200">
            <td class="px-4 py-3">
              <select 
                v-model="novoCargoId"
                class="w-full px-3 py-1.5 text-sm border border-blue-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Selecionar cargo</option>
                <option v-for="cargo in cargosOrdenados" :key="cargo.id" :value="cargo.id">
                  {{ cargo.nome }}
                </option>
              </select>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                <input 
                  v-model="novaHabilidade"
                  @keyup.enter="adicionarHabilidade"
                  placeholder="Adicionar nova habilidade..."
                  class="flex-1 px-3 py-1.5 text-sm border border-blue-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </td>
            <td class="px-4 py-3 text-right">
              <button 
                @click="adicionarHabilidade"
                :disabled="!novaHabilidade.trim() || !novoCargoId"
                class="bg-blue-600 text-white px-3 py-1.5 rounded-md text-xs font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Adicionar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Modal de confirmação -->
    <ConfirmModal 
      :show="showConfirmModal"
      :title="'Confirmar exclusão'"
      :message="`Tem certeza que deseja excluir a habilidade '${itemParaExcluir?.nome}'?`"
      @confirm="executarExclusao"
      @cancel="cancelarExclusao"
    />
    
    <!-- Modal de notificação -->
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
  name: 'HabilidadesCrud',
  components: {
    ConfirmModal,
    NotificationModal
  },
  data() {
    return {
      habilidades: [],
      cargos: [],
      loading: false,
      editando: null,
      nomeEditando: '',
      cargoEditando: '',
      novaHabilidade: '',
      novoCargoId: '',
      cargoSelecionado: '',
      ordenacao: { campo: 'nome', direcao: 'asc' },
      showConfirmModal: false,
      itemParaExcluir: null,
      showNotification: false,
      notificationTitle: '',
      notificationMessage: ''
    }
  },
  computed: {
    habilidadesOrdenadas() {
      const sorted = [...this.habilidades].sort((a, b) => {
        let valorA, valorB
        if (this.ordenacao.campo === 'cargo') {
          valorA = a.cargo.nome
          valorB = b.cargo.nome
        } else {
          valorA = a.nome
          valorB = b.nome
        }
        const resultado = valorA.localeCompare(valorB)
        return this.ordenacao.direcao === 'asc' ? resultado : -resultado
      })
      return sorted
    },
    cargosOrdenados() {
      return [...this.cargos].sort((a, b) => a.nome.localeCompare(b.nome))
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      this.loading = true
      try {
        const [habilidadesRes, cargosRes] = await Promise.all([
          axios.get('/api/habilidades', { params: this.cargoSelecionado ? { cargo_id: this.cargoSelecionado } : {} }),
          axios.get('/api/cargos')
        ])
        this.habilidades = habilidadesRes.data
        this.cargos = cargosRes.data
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    
    ordenarPor(campo) {
      if (this.ordenacao.campo === campo) {
        this.ordenacao.direcao = this.ordenacao.direcao === 'asc' ? 'desc' : 'asc'
      } else {
        this.ordenacao.campo = campo
        this.ordenacao.direcao = 'asc'
      }
    },
    
    iniciarEdicao(habilidade) {
      this.editando = habilidade.id
      this.nomeEditando = habilidade.nome
      this.cargoEditando = habilidade.cargo.id
      this.$nextTick(() => {
        this.$refs.inputEdit?.[0]?.focus()
      })
    },
    
    cancelarEdicao() {
      this.editando = null
      this.nomeEditando = ''
      this.cargoEditando = ''
    },
    
    async salvarEdicao(habilidade) {
      if (!this.nomeEditando.trim() || !this.cargoEditando) {
        this.cancelarEdicao()
        return
      }
      try {
        const response = await axios.put(`/api/habilidades/${habilidade.id}`, { 
          nome: this.nomeEditando.trim(),
          cargo_id: this.cargoEditando
        })
        const index = this.habilidades.findIndex(h => h.id === habilidade.id)
        if (index !== -1) {
          this.habilidades[index] = response.data
        }
        this.cancelarEdicao()
      } catch (error) {
        console.error('Erro ao salvar habilidade:', error)
        this.cancelarEdicao()
      }
    },
    
    async adicionarHabilidade() {
      if (!this.novaHabilidade.trim() || !this.novoCargoId) return
      try {
        const response = await axios.post('/api/habilidades', { 
          nome: this.novaHabilidade.trim(),
          cargo_id: this.novoCargoId
        })
        this.habilidades.push(response.data)
        this.novaHabilidade = ''
        this.novoCargoId = ''
      } catch (error) {
        console.error('Erro ao adicionar habilidade:', error)
      }
    },
    
    confirmarExclusao(habilidade) {
      this.itemParaExcluir = habilidade
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        await axios.delete(`/api/habilidades/${this.itemParaExcluir.id}`)
        const index = this.habilidades.findIndex(h => h.id === this.itemParaExcluir.id)
        if (index !== -1) {
          this.habilidades.splice(index, 1)
        }
        this.cancelarExclusao()
      } catch (error) {
        console.error('Erro ao excluir habilidade:', error)
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
    },
    
    fecharNotificacao() {
      this.showNotification = false
      this.notificationTitle = ''
      this.notificationMessage = ''
    }
  }
}
</script>