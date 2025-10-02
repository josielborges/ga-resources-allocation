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
          <tr v-for="projeto in projetosOrdenados" :key="projeto.id" class="hover:bg-gray-50">
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
      <div class="bg-white rounded-lg w-full max-w-5xl max-h-[98vh] flex flex-col overflow-hidden">
        <!-- Header -->
        <div class="flex justify-between items-center px-4 py-3 border-b border-gray-200">
          <h3 class="text-lg font-semibold">{{ editandoProjeto ? 'Editar Projeto' : 'Novo Projeto' }}</h3>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- Content -->
        <div class="flex-1 overflow-y-auto px-4 py-3">
          <div class="space-y-4">
            <!-- Dados do Projeto -->
            <div class="grid grid-cols-3 gap-4">
              <div class="col-span-2">
                <label class="block text-sm font-medium mb-1">Nome do Projeto</label>
                <input 
                  v-model="form.nome" 
                  type="text" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium mb-1">Cor</label>
                <input 
                  v-model="form.color" 
                  type="color" 
                  class="w-full h-10 border border-gray-300 rounded-md cursor-pointer"
                />
              </div>
            </div>
            
            <!-- Etapas -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-base font-medium">Etapas</h4>
                <button 
                  type="button" 
                  @click="adicionarEtapa" 
                  class="bg-primary-main text-white px-2 py-1 rounded text-xs font-medium hover:bg-primary-light transition-colors flex items-center space-x-1"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  <span>Adicionar</span>
                </button>
              </div>
              
              <div class="sheets-container border border-gray-200 rounded overflow-hidden shadow-sm">
                <table class="sheets-table">
                  <thead>
                    <tr class="sheets-header">
                      <th class="sheets-cell sheets-header-cell w-10 text-center">#</th>
                      <th class="sheets-cell sheets-header-cell min-w-[200px]">Nome da Etapa</th>
                      <th class="sheets-cell sheets-header-cell w-16 text-center">Dias</th>
                      <th class="sheets-cell sheets-header-cell w-32">Cargo</th>
                      <th class="sheets-cell sheets-header-cell w-24 text-center">Pred.</th>
                      <th class="sheets-cell sheets-header-cell min-w-[150px]">Habilidades</th>
                      <th class="sheets-cell sheets-header-cell w-12 text-center">Ações</th>
                    </tr>
                  </thead>
                  <tbody ref="etapasContainer">
                    <tr v-for="(etapa, index) in form.etapas" :key="`etapa-${etapa.nome}-${index}`" class="sheets-row group" :data-index="index">
                      <td class="sheets-cell sheets-number-cell">
                        <div class="drag-handle sheets-drag-handle" :title="`Etapa ${index + 1} - Arraste para reordenar`">
                          <svg class="w-3 h-3 text-gray-400 group-hover:text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                          </svg>
                          <span class="text-xs font-medium ml-1">{{ index + 1 }}</span>
                        </div>
                      </td>
                      <td class="sheets-cell nome-cell">
                        <div class="nome-container">
                          <div 
                            class="predecessor-link-nome"
                            draggable="true"
                            @dragstart="handlePredecessorDragStart(index, $event)"
                            @dragend="handleDragEnd"
                            title="Arraste para criar dependência"
                          >
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"></path>
                            </svg>
                          </div>
                          <input 
                            v-model="etapa.nome" 
                            type="text" 
                            required
                            placeholder="Digite o nome da etapa"
                            class="sheets-input nome-input"
                            @dragover.prevent="handleDragOver(index, $event)"
                            @dragleave="handleDragLeave"
                            @drop="handlePredecessorDrop(index, $event)"
                            :class="{ 'drop-active': dragOverIndex === index }"
                          />
                        </div>
                      </td>
                      <td class="sheets-cell">
                        <input 
                          v-model.number="etapa.duracao_dias" 
                          type="number" 
                          min="1" 
                          max="365"
                          required
                          class="sheets-input text-center font-medium"
                          placeholder="0"
                        />
                      </td>
                      <td class="sheets-cell">
                        <select 
                          v-model="etapa.cargo_necessario_id" 
                          required
                          class="sheets-select text-sm"
                        >
                          <option value="" class="text-gray-400">Selecionar cargo</option>
                          <option v-for="cargo in cargosOrdenados" :key="cargo.id" :value="cargo.id" class="text-gray-900">
                            {{ cargo.nome }}
                          </option>
                        </select>
                      </td>
                      <td class="sheets-cell predecessoras-cell">
                        <div class="predecessoras-compact">
                          <span 
                            v-if="!etapa.predecessoras || etapa.predecessoras.length === 0"
                            class="text-gray-300 text-xs font-medium"
                          >
                            -
                          </span>
                          <div v-else class="predecessoras-badges">
                            <span 
                              v-for="predIndex in etapa.predecessoras" 
                              :key="predIndex"
                              class="predecessor-badge"
                              @click="removePredecessora(index, predIndex)"
                              :title="`Depende da etapa ${predIndex + 1} (clique para remover)`"
                            >
                              {{ predIndex + 1 }}
                            </span>
                          </div>
                        </div>
                      </td>
                      <td class="sheets-cell habilidades-cell" @mousedown.stop @click.stop>
                        <div @click.stop class="h-full">
                          <HabilidadesSelect 
                            v-model="etapa.habilidades_necessarias"
                            :habilidades="habilidadesOrdenadas"
                          />
                        </div>
                      </td>
                      <td class="sheets-cell text-center">
                        <button 
                          type="button" 
                          @click="removerEtapa(index)" 
                          class="sheets-delete-btn group-hover:opacity-100"
                          title="Remover esta etapa"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="flex justify-end space-x-2 px-4 py-2 border-t border-gray-200 bg-gray-50">
          <button 
            type="button" 
            @click="fecharModal" 
            class="px-4 py-1.5 text-sm text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button 
            type="button"
            @click="salvarProjeto"
            :disabled="salvando"
            class="px-4 py-1.5 text-sm bg-primary-main text-white rounded hover:bg-primary-light disabled:opacity-50 flex items-center space-x-1"
          >
            <svg v-if="salvando" class="animate-spin w-3 h-3" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ salvando ? 'Salvando...' : 'Salvar' }}</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal de confirmação -->
    <ConfirmModal 
      :show="showConfirmModal"
      :title="'Confirmar exclusão'"
      :message="`Tem certeza que deseja excluir o projeto '${itemParaExcluir?.nome}'?`"
      @confirm="executarExclusao"
      @cancel="cancelarExclusao"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ConfirmModal from './ConfirmModal.vue'
import HabilidadesSelect from './HabilidadesSelect.vue'
import Sortable from 'sortablejs'

export default {
  name: 'ProjetosCrud',
  components: {
    ConfirmModal,
    HabilidadesSelect
  },
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
      },
      showConfirmModal: false,
      itemParaExcluir: null,
      draggedIndex: null,
      dragOverIndex: null
    }
  },
  computed: {
    projetosOrdenados() {
      return [...this.projetos].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    cargosOrdenados() {
      return [...this.cargos].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    habilidadesOrdenadas() {
      return [...this.habilidades].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    
    etapasComPredecessoras() {
      return this.form.etapas.map((etapa, index) => {
        const predecessoraIndex = etapa.predecessora_id
        return {
          ...etapa,
          predecessora_id: predecessoraIndex !== null && predecessoraIndex < this.form.etapas.length 
            ? this.form.etapas[predecessoraIndex]?.id || null 
            : null
        }
      })
    }
  },
  async mounted() {
    await this.carregarDados()
  },
  
  watch: {
    showModal(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.initSortable()
        })
      }
    }
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
          etapas: projeto.etapas
            .sort((a, b) => (a.ordem || 0) - (b.ordem || 0))
            .map((etapa, index) => {
              // Encontrar índices das predecessoras
              const predecessorasIndices = []
              if (etapa.predecessoras && etapa.predecessoras.length > 0) {
                const etapasOrdenadas = projeto.etapas.sort((a, b) => (a.ordem || 0) - (b.ordem || 0))
                etapa.predecessoras.forEach(pred => {
                  const predIndex = etapasOrdenadas.findIndex(e => e.id === pred.id)
                  if (predIndex !== -1) {
                    predecessorasIndices.push(predIndex)
                  }
                })
              }
              
              return {
                nome: etapa.nome,
                duracao_dias: etapa.duracao_dias,
                cargo_necessario_id: etapa.cargo_necessario.id,
                habilidades_necessarias: etapa.habilidades_necessarias.map(h => h.nome),
                ordem: etapa.ordem !== undefined ? etapa.ordem : index,
                predecessoras: predecessorasIndices
              }
            })
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
        habilidades_necessarias: [],
        ordem: this.form.etapas.length,
        predecessoras: []
      })
    },
    
    removerEtapa(index) {
      this.form.etapas.splice(index, 1)
    },
    
    async salvarProjeto() {
      console.log('ProjetosCrud: salvarProjeto called')
      this.salvando = true
      try {
        const formData = {
          ...this.form,
          etapas: this.form.etapas.map((etapa, index) => ({
            ...etapa,
            predecessoras_ids: etapa.predecessoras || []
          }))
        }
        
        if (this.editandoProjeto) {
          await axios.put(`/api/projetos/${this.editandoProjeto.id}`, formData)
        } else {
          await axios.post('/api/projetos', formData)
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
    
    confirmarExclusao(projeto) {
      this.itemParaExcluir = projeto
      this.showConfirmModal = true
    },
    
    async executarExclusao() {
      try {
        await axios.delete(`/api/projetos/${this.itemParaExcluir.id}`)
        await this.carregarDados()
        this.cancelarExclusao()
      } catch (error) {
        console.error('Erro ao excluir projeto:', error)
        this.cancelarExclusao()
      }
    },
    
    cancelarExclusao() {
      this.showConfirmModal = false
      this.itemParaExcluir = null
    },
    
    handlePredecessorDragStart(index, event) {
      console.log('Drag start:', index)
      this.draggedIndex = index
      event.dataTransfer.setData('text/plain', index.toString())
      event.dataTransfer.effectAllowed = 'copy'
      event.stopPropagation()
    },
    
    handleDragEnd() {
      console.log('Drag end')
      this.draggedIndex = null
      this.dragOverIndex = null
    },
    
    handleDragOver(targetIndex, event) {
      event.preventDefault()
      this.dragOverIndex = targetIndex
    },
    
    handleDragLeave() {
      this.dragOverIndex = null
    },
    
    handlePredecessorDrop(targetIndex, event) {
      event.preventDefault()
      console.log('Drop on:', targetIndex)
      const sourceIndex = parseInt(event.dataTransfer.getData('text/plain'))
      console.log('Source:', sourceIndex, 'Target:', targetIndex)
      
      if (sourceIndex !== targetIndex) {
        // Inverter lógica: targetIndex vira predecessor de sourceIndex
        if (!this.form.etapas[sourceIndex].predecessoras) {
          this.form.etapas[sourceIndex].predecessoras = []
        }
        
        if (!this.form.etapas[sourceIndex].predecessoras.includes(targetIndex)) {
          this.form.etapas[sourceIndex].predecessoras.push(targetIndex)
          console.log('Added predecessor:', targetIndex, 'to', sourceIndex)
        }
      }
      
      this.dragOverIndex = null
    },
    
    removePredecessora(etapaIndex, predecessoraIndex) {
      const predecessoras = this.form.etapas[etapaIndex].predecessoras
      const index = predecessoras.indexOf(predecessoraIndex)
      if (index > -1) {
        predecessoras.splice(index, 1)
      }
    },
    
    initSortable() {
      if (this.$refs.etapasContainer) {
        Sortable.create(this.$refs.etapasContainer, {
          animation: 150,
          ghostClass: 'sortable-ghost',
          chosenClass: 'sortable-chosen',
          dragClass: 'sortable-drag',
          handle: '.drag-handle',
          onEnd: (evt) => {
            const oldIndex = evt.oldIndex
            const newIndex = evt.newIndex
            
            if (oldIndex !== newIndex && oldIndex < this.form.etapas.length && newIndex < this.form.etapas.length) {
              // Criar uma nova cópia do array para forçar reatividade
              const etapas = [...this.form.etapas]
              const movedItem = etapas.splice(oldIndex, 1)[0]
              etapas.splice(newIndex, 0, movedItem)
              
              // Atualizar ordem e ajustar predecessoras
              etapas.forEach((etapa, index) => {
                etapa.ordem = index
                if (etapa.predecessoras) {
                  // Ajustar índices das predecessoras baseado na nova ordem
                  etapa.predecessoras = etapa.predecessoras
                    .map(predIndex => {
                      if (predIndex === oldIndex) return newIndex
                      if (oldIndex < newIndex) {
                        if (predIndex > oldIndex && predIndex <= newIndex) return predIndex - 1
                      } else {
                        if (predIndex >= newIndex && predIndex < oldIndex) return predIndex + 1
                      }
                      return predIndex
                    })
                    .filter(p => p < index) // Manter apenas predecessoras válidas
                }
              })
              
              // Substituir o array completo para garantir reatividade
              this.form.etapas = etapas
            }
          }
        })
      }
    }
  }
}
</script>

<style scoped>
/* Modern Table Style */
.sheets-container {
  background: white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.sheets-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.sheets-cell {
  border-right: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  padding: 0;
  margin: 0;
  height: 36px;
  vertical-align: middle;
  position: relative;
  transition: all 0.15s ease;
}

.sheets-header {
  background: linear-gradient(to bottom, #f9fafb, #f3f4f6);
  border-bottom: 2px solid #e5e7eb;
}

.sheets-header-cell {
  font-weight: 600;
  color: #475569;
  font-size: 11px;
  padding: 8px 6px;
  border-right: 1px solid #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.sheets-row:hover {
  background: #f9fafb;
}

.sheets-row:hover .sheets-cell {
  background: #f9fafb;
  border-color: #e5e7eb;
}

.sheets-number-cell {
  background: #f9fafb;
  text-align: center;
  font-weight: 500;
  color: #6b7280;
  width: 40px;
  border-right: 2px solid #e5e7eb;
}

.sheets-drag-handle {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  font-size: 11px;
  user-select: none;
  border-radius: 2px;
  transition: all 0.2s ease;
}

.sheets-drag-handle:active {
  cursor: grabbing;
}

.sheets-drag-handle:hover {
  background: #dbeafe;
  color: #2563eb;
  transform: scale(1.02);
}

.sheets-input, .sheets-select {
  width: 100%;
  height: 36px;
  border: none;
  outline: none;
  padding: 0 8px;
  font-size: 13px;
  background: transparent;
  font-family: inherit;
  transition: all 0.15s ease;
}

.sheets-input:focus, .sheets-select:focus {
  background: white;
  box-shadow: inset 0 0 0 2px #3b82f6;
  z-index: 1;
  position: relative;
  border-radius: 4px;
}

.sheets-input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.sheets-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 6px center;
  background-repeat: no-repeat;
  background-size: 16px;
  padding-right: 28px;
}

.sheets-delete-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #9ca3af;
  cursor: pointer;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.sheets-delete-btn:hover {
  background: #fef2f2;
  color: #dc2626;
  transform: scale(1.1);
  opacity: 1;
}

.group:hover .sheets-delete-btn {
  opacity: 1;
}

/* Sortable styles */
.sortable-ghost {
  opacity: 0.5;
  background: #e8f0fe;
}

.sortable-chosen {
  background: #e8f0fe;
}

.sortable-drag {
  background: #e8f0fe;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Remove default table spacing */
.sheets-table td, .sheets-table th {
  padding: 0;
  margin: 0;
}

/* Predecessoras styles */
.predecessoras-container {
  display: flex;
  align-items: center;
  height: 28px;
  padding: 0 4px;
  gap: 4px;
}

.predecessoras-tags {
  display: flex;
  gap: 2px;
  flex-wrap: wrap;
}

.predecessor-tag {
  background: #e8f0fe;
  color: #1a73e8;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  font-weight: 500;
}

.predecessor-tag:hover {
  background: #d2e3fc;
}

.predecessor-remove {
  font-size: 12px;
  font-weight: bold;
  opacity: 0.7;
}

.predecessor-remove:hover {
  opacity: 1;
  color: #d93025;
}

.predecessor-drop-zone {
  flex: 1;
  min-height: 24px;
  border: 1px dashed transparent;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.predecessor-drop-zone.drop-active {
  border-color: #1a73e8;
  background: #e8f0fe;
}

.predecessor-drop-zone.drop-active .drop-hint {
  color: #1a73e8;
  font-weight: 500;
}

.sheets-drag-handle[draggable="true"] {
  cursor: grab;
}

.sheets-drag-handle[draggable="true"]:active {
  cursor: grabbing;
}

.nome-cell {
  position: relative;
}

.nome-container {
  display: flex;
  align-items: center;
  height: 28px;
}

.predecessor-link-nome {
  cursor: grab;
  padding: 6px;
  margin-right: 6px;
  border-radius: 3px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  user-select: none;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s ease;
}

.predecessor-link-nome:hover {
  background: #dbeafe;
  border-color: #3b82f6;
  color: #2563eb;
  transform: scale(1.05);
}

.predecessor-link-nome:active {
  cursor: grabbing;
  transform: scale(0.95);
}

.nome-input {
  flex: 1;
}

.nome-input.drop-active {
  background: #e8f0fe;
  border-color: #1a73e8;
}

.predecessoras-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  padding: 0 4px;
}

.predecessoras-badges {
  display: flex;
  gap: 3px;
  flex-wrap: wrap;
  justify-content: center;
}

.predecessor-badge {
  background: #dbeafe;
  color: #2563eb;
  font-size: 10px;
  font-weight: 700;
  padding: 3px 6px;
  border-radius: 6px;
  cursor: pointer;
  user-select: none;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  border: 1px solid #bfdbfe;
}

.predecessor-badge:hover {
  background: #1d4ed8;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}
</style>