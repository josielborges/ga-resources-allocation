<template>
  <div class="relative">
    <button 
      @click.stop="toggleModal"
      class="sheets-habilidades-btn"
    >
      <span v-if="selectedHabilidades.length === 0" class="text-gray-500">
        Selecionar...
      </span>
      <span v-else class="text-gray-900">
        {{ selectedHabilidades.length }} habilidade{{ selectedHabilidades.length > 1 ? 's' : '' }}
      </span>
      <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>
    
    <!-- Modal compacto -->
    <div 
      v-if="showModal"
      class="fixed z-[9999] w-64 bg-white border border-gray-300 shadow-lg p-3"
      :style="modalPosition"
      @click.stop
    >
      <div class="mb-2">
        <input 
          v-model="searchTerm"
          type="text"
          placeholder="Buscar..."
          class="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-primary-main"
        />
      </div>
      
      <div class="max-h-32 overflow-y-auto space-y-1">
        <label 
          v-for="habilidade in filteredHabilidades" 
          :key="habilidade.id" 
          class="flex items-center text-xs hover:bg-gray-50 p-1 rounded cursor-pointer"
          @click.stop
        >
          <input 
            type="checkbox" 
            :value="habilidade.nome"
            :checked="selectedHabilidades.includes(habilidade.nome)"
            @change="toggleHabilidade(habilidade.nome)"
            class="mr-2 text-primary-main"
          />
          <span class="truncate">{{ habilidade.nome }}</span>
        </label>
      </div>
      
      <div v-if="selectedHabilidades.length > 0" class="mt-2 pt-2 border-t border-gray-200">
        <div class="text-xs text-gray-600 mb-1">Selecionadas:</div>
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="hab in selectedHabilidades" 
            :key="hab"
            class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-primary-100 text-primary-800"
          >
            {{ hab.length > 8 ? hab.substring(0, 8) + '...' : hab }}
            <button 
              @click.stop="removeHabilidade(hab)"
              class="ml-1 hover:text-primary-600"
            >
              ×
            </button>
          </span>
        </div>
      </div>
      
      <div class="mt-2 pt-2 border-t border-gray-200">
        <button 
          @click.stop="closeModal"
          class="w-full px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded"
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HabilidadesSelect',
  props: {
    modelValue: {
      type: Array,
      default: () => []
    },
    habilidades: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      showModal: false,
      searchTerm: '',
      buttonRect: null
    }
  },
  computed: {
    selectedHabilidades() {
      return this.modelValue || []
    },
    filteredHabilidades() {
      if (!this.searchTerm.trim()) return this.habilidades
      return this.habilidades.filter(hab => 
        hab.nome.toLowerCase().includes(this.searchTerm.toLowerCase())
      )
    },
    modalPosition() {
      if (!this.buttonRect) return { top: '0px', left: '0px', borderRadius: '4px' }
      return {
        top: `${this.buttonRect.bottom + 2}px`,
        left: `${Math.max(0, this.buttonRect.right - 256)}px`,
        borderRadius: '4px'
      }
    }
  },
  methods: {
    toggleModal(event) {
      console.log('HabilidadesSelect: toggleModal called')
      event.stopPropagation()
      
      if (!this.showModal) {
        // Capturar posição do botão antes de abrir
        this.buttonRect = event.target.getBoundingClientRect()
      }
      
      this.showModal = !this.showModal
      if (this.showModal) {
        this.searchTerm = ''
      }
    },
    toggleHabilidade(habilidade) {
      const current = [...this.selectedHabilidades]
      const index = current.indexOf(habilidade)
      
      if (index > -1) {
        current.splice(index, 1)
      } else {
        current.push(habilidade)
      }
      
      this.$emit('update:modelValue', current)
    },
    removeHabilidade(habilidade) {
      const current = [...this.selectedHabilidades]
      const index = current.indexOf(habilidade)
      if (index > -1) {
        current.splice(index, 1)
        this.$emit('update:modelValue', current)
      }
    },
    closeModal() {
      this.showModal = false
    },
    handleClickOutside(event) {
      if (this.showModal && this.$el && !this.$el.contains(event.target)) {
        this.showModal = false
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<style scoped>
.sheets-habilidades-btn {
  width: 100%;
  height: 32px;
  border: none;
  outline: none;
  padding: 0 8px;
  font-size: 13px;
  background: transparent;
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  font-family: inherit;
}

.sheets-habilidades-btn:hover {
  background: #f8f9fa;
}

.sheets-habilidades-btn:focus {
  background: white;
  box-shadow: inset 0 0 0 2px #1a73e8;
  z-index: 1;
  position: relative;
}

.sheets-habilidades-btn * {
  pointer-events: none;
}
</style>