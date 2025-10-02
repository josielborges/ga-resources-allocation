<template>
  <div class="relative">
    <div class="habilidades-container">
      <!-- Selected habilidades as pills -->
      <div v-if="selectedHabilidades.length > 0" class="selected-tags">
        <span 
          v-for="hab in selectedHabilidades" 
          :key="hab"
          class="habilidade-pill"
          :title="hab"
          @click.stop="removeHabilidade(hab)"
        >
          {{ abbreviateText(hab) }}
        </span>
      </div>
      
      <!-- Add button -->
      <span 
        @click.stop="toggleModal"
        class="add-pill"
        :class="{ 'first-item': selectedHabilidades.length === 0 }"
      >
        <span v-if="selectedHabilidades.length === 0">Selecionar habilidades</span>
        <span v-else>+</span>
      </span>
    </div>
    
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
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
          >
            {{ abbreviateText(hab) }}
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

    abbreviateText(text) {
      const stopWords = ['de', 'da', 'do', 'das', 'dos', 'e', 'em', 'com', 'para', 'por', 'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas']
      return text
        .split(' ')
        .filter(word => !stopWords.includes(word.toLowerCase()))
        .map(word => word.charAt(0).toUpperCase() + word.slice(1, 5).toLowerCase())
        .join(' ')
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
.habilidades-container {
  width: 100%;
  min-height: 32px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
  background: transparent;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  flex: 1;
}

.habilidade-pill {
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
  background: #dcfce7;
  color: #166534;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-width: fit-content;
}

.habilidade-pill:hover {
  background: #bbf7d0;
  transform: scale(1.02);
}

.add-pill {
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px dashed #d1d5db;
}

.add-pill:hover {
  background: #e5e7eb;
  color: #374151;
}

.add-pill.first-item {
  color: #9ca3af;
  border: none;
  background: transparent;
}

.add-pill.first-item:hover {
  background: #f9fafb;
  color: #374151;
}
</style>