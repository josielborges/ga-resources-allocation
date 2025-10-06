<template>
  <div class="relative" ref="componentRef">
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
      class="fixed z-[9999] w-96 bg-white border border-gray-300 shadow-xl rounded p-1"
      :style="modalPosition"
      @click.stop
    >
      <div class="grid grid-cols-3 gap-0.5">
        <div 
          v-for="habilidade in habilidades" 
          :key="habilidade.id" 
          class="text-xs px-1 py-0.5 rounded cursor-pointer transition-colors text-center truncate"
          :class="selectedHabilidades.includes(habilidade.nome) ? 'bg-green-100 text-green-800 font-medium' : 'hover:bg-gray-50 text-gray-700'"
          @click.stop="toggleHabilidade(habilidade.nome)"
          :title="habilidade.nome"
        >
          {{ habilidade.nome }}
        </div>
      </div>
      
      <div class="mt-1 pt-1 border-t border-gray-200 flex justify-between items-center">
        <span class="text-xs text-gray-600">{{ selectedHabilidades.length }} sel.</span>
        <button 
          @click.stop="closeModal"
          class="px-2 py-0.5 text-xs bg-green-600 text-white rounded hover:bg-green-700"
        >
          OK
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
      buttonRect: null
    }
  },
  computed: {
    selectedHabilidades() {
      return this.modelValue || []
    },

    modalPosition() {
      if (!this.buttonRect) return { top: '0px', left: '0px' }
      return {
        top: `${this.buttonRect.bottom + 2}px`,
        left: `${Math.max(0, this.buttonRect.right - 384)}px`
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
      if (this.showModal && this.$refs.componentRef && !this.$refs.componentRef.contains(event.target)) {
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
  border-radius: 6px;
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