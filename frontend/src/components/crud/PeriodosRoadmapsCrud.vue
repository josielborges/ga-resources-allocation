<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-semibold text-text-primary">Períodos de Roadmaps</h2>
    </div>

    <div class="bg-white rounded-md shadow-sm overflow-hidden">
      <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-3 py-2">
        <h3 class="text-white font-medium text-sm">Anos Cadastrados</h3>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-main mx-auto"></div>
        <p class="mt-2 text-text-secondary text-sm">Carregando...</p>
      </div>
      
      <div v-else class="p-3 space-y-1.5">
        <div 
          v-for="periodo in periodosOrdenados" 
          :key="periodo.id"
          class="group p-2 border border-gray-200 rounded-md hover:border-blue-300 hover:bg-gray-50 transition-all"
        >
          <div v-if="editandoPeriodo === periodo.id" class="flex items-center space-x-2">
            <input 
              v-model.number="formEdit.ano"
              type="number"
              min="2020"
              max="2050"
              class="w-20 px-2 py-0.5 text-xs border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input 
              v-model="formEdit.inicio"
              type="date"
              class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input 
              v-model="formEdit.termino"
              type="date"
              class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button @click="salvarEdicao(periodo)" class="text-green-600 hover:text-green-800 p-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </button>
            <button @click="cancelarEdicao" class="text-gray-600 hover:text-gray-800 p-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <div v-else class="flex items-center justify-between">
            <div class="flex-1">
              <div class="font-medium text-sm text-gray-900">Ano {{ periodo.ano }}</div>
              <div class="text-xs text-gray-500 mt-0.5">
                {{ formatarData(periodo.inicio) }} até {{ formatarData(periodo.termino) }}
              </div>
            </div>
            <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button @click="iniciarEdicao(periodo)" class="text-blue-600 hover:text-blue-800 p-1" title="Editar">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              <button @click="confirmarExclusao(periodo)" class="text-red-600 hover:text-red-800 p-1" title="Excluir">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Add Periodo -->
        <div class="p-2 border-2 border-dashed border-blue-300 rounded-md bg-blue-50">
          <div class="flex items-center space-x-2">
            <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            <input 
              v-model.number="form.ano"
              type="number"
              min="2020"
              max="2050"
              placeholder="Ano"
              class="w-20 px-2 py-0.5 text-xs border border-blue-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input 
              v-model="form.inicio"
              type="date"
              placeholder="Início"
              class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input 
              v-model="form.termino"
              type="date"
              placeholder="Término"
              class="flex-1 px-2 py-0.5 text-xs border border-blue-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button 
              @click="adicionar"
              :disabled="!form.ano || !form.inicio || !form.termino"
              class="bg-blue-600 text-white px-2 py-0.5 rounded text-xs font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Adicionar
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <ConfirmModal 
      :show="showConfirmModal"
      :title="'Confirmar exclusão'"
      :message="`Tem certeza que deseja excluir o período do ano ${itemParaExcluir?.ano}?`"
      @confirm="executarExclusao"
      @cancel="cancelarExclusao"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ConfirmModal from '../modals/ConfirmModal.vue'

export default {
  name: 'PeriodosRoadmapsCrud',
  components: {
    ConfirmModal
  },
  data() {
    return {
      periodos: [],
      loading: false,
      editandoPeriodo: null,
      form: {
        ano: null,
        inicio: '',
        termino: ''
      },
      formEdit: {
        ano: null,
        inicio: '',
        termino: ''
      },
      showConfirmModal: false,
      itemParaExcluir: null
    }
  },
  computed: {
    periodosOrdenados() {
      return [...this.periodos].sort((a, b) => b.ano - a.ano)
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      this.loading = true
      try {
        const response = await axios.get('/api/periodos-roadmaps')
        this.periodos = response.data
      } catch (error) {
        console.error('Erro ao carregar períodos:', error)
      } finally {
        this.loading = false
      }
    },
    
    iniciarEdicao(periodo) {
      this.editandoPeriodo = periodo.id
      this.formEdit = {
        ano: periodo.ano,
        inicio: periodo.inicio,
        termino: periodo.termino
      }
    },
    
    cancelarEdicao() {
      this.editandoPeriodo = null
      this.formEdit = { ano: null, inicio: '', termino: '' }
    },
    
    async salvarEdicao(periodo) {
      if (!this.formEdit.ano || !this.formEdit.inicio || !this.formEdit.termino) {
        this.cancelarEdicao()
        return
      }
      try {
        const response = await axios.put(`/api/periodos-roadmaps/${periodo.id}`, this.formEdit)
        const index = this.periodos.findIndex(p => p.id === periodo.id)
        if (index !== -1) {
          this.periodos[index] = response.data
        }
        this.cancelarEdicao()
      } catch (error) {
        console.error('Erro ao salvar período:', error)
        this.cancelarEdicao()
      }
    },
    
    async adicionar() {
      if (!this.form.ano || !this.form.inicio || !this.form.termino) return
      try {
        const response = await axios.post('/api/periodos-roadmaps', this.form)
        this.periodos.push(response.data)
        this.form = { ano: null, inicio: '', termino: '' }
      } catch (error) {
        console.error('Erro ao adicionar período:', error)
      }
    },
    
    confirmarExclusao(periodo) {
      this.itemParaExcluir = periodo
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        await axios.delete(`/api/periodos-roadmaps/${this.itemParaExcluir.id}`)
        const index = this.periodos.findIndex(p => p.id === this.itemParaExcluir.id)
        if (index !== -1) {
          this.periodos.splice(index, 1)
        }
        this.cancelarExclusao()
      } catch (error) {
        console.error('Erro ao excluir período:', error)
        this.cancelarExclusao()
      }
    },
    
    cancelarExclusao() {
      this.showConfirmModal = false
      this.itemParaExcluir = null
    },
    
    formatarData(data) {
      if (!data) return '-'
      const [ano, mes, dia] = data.split('-')
      return `${dia}/${mes}/${ano}`
    }
  }
}
</script>
