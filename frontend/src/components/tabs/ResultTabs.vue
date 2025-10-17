<template>
  <div class="bg-white rounded-md shadow-sm">
    <div class="border-b border-divider px-4">
      <div class="flex justify-between items-center">
        <nav class="flex space-x-6">
          <button 
            v-for="tab in tabs" 
            :key="tab.name"
            @click="$emit('update:activeTab', tab.name)"
            :class="[
              'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === tab.name 
                ? 'border-primary-main text-primary-main' 
                : 'border-transparent text-text-secondary hover:text-text-primary hover:border-gray-300'
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
        <button 
          @click="$emit('save')" 
          class="bg-green-600 text-white px-3 py-1.5 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
        >
          Salvar Resultado
        </button>
      </div>
    </div>
    
    <div class="p-4">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultTabs',
  props: {
    activeTab: { type: String, required: true }
  },
  emits: ['update:activeTab', 'save'],
  data() {
    return {
      tabs: [
        { name: 'dados', label: 'Dados' },
        { name: 'fitness', label: 'Fitness' },
        { name: 'conflitos', label: 'Conflitos' },
        { name: 'gantt', label: 'Gantt' },
        { name: 'calendario', label: 'Calendário' },
        { name: 'mapa', label: 'Mapa de Alocação' },
        { name: 'comparacao', label: 'Comparação' }
      ]
    }
  }
}
</script>
