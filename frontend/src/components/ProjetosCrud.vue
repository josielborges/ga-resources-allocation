<template>
  <div class="space-y-6">
    <!-- Header com botão de adicionar -->
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold text-text-primary">Projetos</h2>
      <button 
        @click="abrirModal()" 
        class="bg-primary-main text-white px-4 py-2 rounded-sm text-sm font-medium hover:bg-primary-light transition-colors"
      >
        Novo Projeto
      </button>
    </div>

    <!-- Tabela de projetos -->
    <div class="bg-white rounded-md shadow-sm overflow-hidden">
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-main mx-auto"></div>
        <p class="mt-2 text-text-secondary">Carregando projetos...</p>
      </div>
      
      <div v-else-if="projetos.length === 0" class="p-8 text-center text-text-secondary">
        Nenhum projeto encontrado
      </div>
      
      <table v-else class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Projeto</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Etapas</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duração Total</th>
            <th class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="projeto in projetos" :key="projeto.id" class="hover:bg-gray-50">
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full mr-2" :style="{ backgroundColor: projeto.color }"></div>
                <div class="text-sm font-medium text-gray-900">{{ projeto.nome }}</div>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ projeto.etapas.length }} etapas</div>
              <div class="text-xs text-gray-500" v-if="projeto.etapas.length > 0">
                {{ projeto.etapas.map(e => e.nome).join(', ') }}
              </div>
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
              {{ projeto.etapas.reduce((total, etapa) => total + etapa.duracao_dias, 0) }} dias
            </td>
            <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button 
                  @click="abrirModal(projeto)" 
                  class="text-indigo-600 hover:text-indigo-900 p-1"
                  title="Editar"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button 
                  @click="confirmarExclusao(projeto)" 
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

    <!-- Modal de edição/criação -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" style="margin: 0; padding: 16px;">
      <div class="bg-white rounded-lg w-full max-w-5xl max-h-[95vh] flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h3 class="text-xl font-semibold">{{ editandoProjeto ? 'Editar Projeto' : 'Novo Projeto' }}</h3>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="salvarProjeto" class="space-y-6">
            <!-- Dados do Projeto -->
            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-text-primary mb-2">Nome do Projeto</label>
                <input 
                  v-model="form.nome" 
                  type="text" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-main"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-text-primary mb-2">Cor</label>
                <div class="flex items-center space-x-3">
                  <input 
                    v-model="form.color" 
                    type="color" 
                    class="w-16 h-10 border border-gray-300 rounded-md cursor-pointer"
                  />
                  <span class="text-sm text-gray-500">{{ form.color }}</span>
                </div>
              </div>
            </div>
            
            <!-- Etapas -->
            <div>
              <div class="mb-4">
                <h4 class="text-lg font-medium text-text-primary">Etapas do Projeto</h4>
              </div>
              
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <!-- Etapas Existentes -->
                <div v-for="(etapa, index) in form.etapas" :key="index" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <!-- Card Header -->
                  <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                      <div class="w-6 h-6 bg-primary-main text-white rounded-full flex items-center justify-center text-xs font-bold">
                        {{ index + 1 }}
                      </div>
                      <span class="font-medium text-gray-900">Etapa {{ index + 1 }}</span>
                    </div>
                    <button 
                      type="button" 
                      @click="removerEtapa(index)" 
                      class="text-red-500 hover:text-red-700 p-1 rounded-md hover:bg-red-50"
                      title="Remover Etapa"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                  
                  <!-- Card Content -->
                  <div class="space-y-3">
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-1">Nome da Etapa</label>
                      <input 
                        v-model="etapa.nome" 
                        type="text" 
                        required
                        placeholder="Ex: Análise de Requisitos"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
                      />
                    </div>
                    
                    <div class="grid grid-cols-2 gap-3">
                      <div>
                        <label class="block text-xs font-medium text-gray-700 mb-1">Duração</label>
                        <div class="relative">
                          <input 
                            v-model.number="etapa.duracao_dias" 
                            type="number" 
                            min="1" 
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
                          />
                          <span class="absolute right-3 top-2 text-xs text-gray-500">dias</span>
                        </div>
                      </div>
                      
                      <div>
                        <label class="block text-xs font-medium text-gray-700 mb-1">Cargo</label>
                        <select 
                          v-model="etapa.cargo_necessario_id" 
                          required
                          class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
                        >
                          <option value="">Selecionar</option>
                          <option v-for="cargo in cargos" :key="cargo.id" :value="cargo.id">
                            {{ cargo.nome }}
                          </option>
                        </select>
                      </div>
                    </div>
                    
                    <div>
                      <label class="block text-xs font-medium text-gray-700 mb-2">Habilidades Necessárias</label>
                      <div class="max-h-20 overflow-y-auto border border-gray-200 rounded-md p-2 bg-white">
                        <div class="grid grid-cols-2 gap-1">
                          <label v-for="habilidade in habilidades" :key="habilidade.id" class="flex items-center text-xs hover:bg-gray-50 p-1 rounded">
                            <input 
                              type="checkbox" 
                              :value="habilidade.nome"
                              v-model="etapa.habilidades_necessarias"
                              class="mr-2 text-primary-main"
                            />
                            <span class="truncate">{{ habilidade.nome }}</span>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Botão Adicionar Etapa -->
                <button 
                  type="button" 
                  @click="adicionarEtapa" 
                  class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-primary-main hover:bg-primary-50 transition-colors flex flex-col items-center justify-center space-y-3 min-h-[200px]"
                >
                  <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  <span class="text-gray-600 font-medium">Adicionar Etapa</span>
                </button>
              </div>
            </div>
          </form>
        </div>
        
        <!-- Footer -->
        <div class="flex justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50 rounded-b-lg">
          <button 
            type="button" 
            @click="fecharModal" 
            class="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 font-medium"
          >
            Cancelar
          </button>
          <button 
            @click="salvarProjeto"
            :disabled="salvando"
            class="px-6 py-2 bg-primary-main text-white rounded-md hover:bg-primary-light disabled:opacity-50 font-medium flex items-center space-x-2"
          >
            <svg v-if="salvando" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ salvando ? 'Salvando...' : 'Salvar Projeto' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProjetosCrud',
  data() {
    return {
      projetos: [],
      cargos: [],
      habilidades: [],
      loading: false,
      salvando: false,
      showModal: false,
      editandoProjeto: null,
      form: {
        nome: '',
        color: '#3B82F6',
        etapas: []
      }
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      this.loading = true
      try {
        const [projetosRes, cargosRes, habilidadesRes] = await Promise.all([
          axios.get('/api/projetos'),
          axios.get('/api/cargos'),
          axios.get('/api/habilidades')
        ])
        this.projetos = projetosRes.data
        this.cargos = cargosRes.data
        this.habilidades = habilidadesRes.data
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.loading = false
      }
    },
    
    abrirModal(projeto = null) {
      this.editandoProjeto = projeto
      if (projeto) {
        this.form = {
          nome: projeto.nome,
          color: projeto.color,
          etapas: projeto.etapas.map(etapa => ({
            nome: etapa.nome,
            duracao_dias: etapa.duracao_dias,
            cargo_necessario_id: etapa.cargo_necessario.id,
            habilidades_necessarias: etapa.habilidades_necessarias.map(h => h.nome)
          }))
        }
      } else {
        this.form = {
          nome: '',
          color: '#3B82F6',
          etapas: []
        }
      }
      this.showModal = true
    },
    
    fecharModal() {
      this.showModal = false
      this.editandoProjeto = null
    },
    
    adicionarEtapa() {
      this.form.etapas.push({
        nome: '',
        duracao_dias: 1,
        cargo_necessario_id: '',
        habilidades_necessarias: []
      })
    },
    
    removerEtapa(index) {
      this.form.etapas.splice(index, 1)
    },
    
    async salvarProjeto() {
      this.salvando = true
      try {
        if (this.editandoProjeto) {
          await axios.put(`/api/projetos/${this.editandoProjeto.id}`, this.form)
        } else {
          await axios.post('/api/projetos', this.form)
        }
        await this.carregarDados()
        this.fecharModal()
      } catch (error) {
        console.error('Erro ao salvar projeto:', error)
        if (error.response?.status === 404) {
          alert('Projeto não encontrado. Recarregando dados...')
          await this.carregarDados()
          this.fecharModal()
        } else {
          alert('Erro ao salvar projeto. Verifique os dados e tente novamente.')
        }
      } finally {
        this.salvando = false
      }
    },
    
    async confirmarExclusao(projeto) {
      if (confirm(`Tem certeza que deseja excluir o projeto "${projeto.nome}"?`)) {
        try {
          await axios.delete(`/api/projetos/${projeto.id}`)
          await this.carregarDados()
        } catch (error) {
          console.error('Erro ao excluir projeto:', error)
        }
      }
    }
  }
}
</script>