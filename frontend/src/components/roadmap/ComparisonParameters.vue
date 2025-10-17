<template>
  <div class="bg-white rounded-md shadow-sm p-4">
    <h4 class="text-sm font-semibold text-gray-900 mb-3">Parâmetros para Comparação</h4>
    
    <div class="mb-4">
      <h5 class="text-xs font-semibold text-blue-600 mb-2 uppercase tracking-wide">Algoritmo Genético</h5>
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">População</label>
          <input :value="gaParams.tam_pop" @input="updateGaParam('tam_pop', $event.target.value)" type="number" min="10" max="100" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Gerações</label>
          <input :value="gaParams.n_gen" @input="updateGaParam('n_gen', $event.target.value)" type="number" min="10" max="500" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Crossover</label>
          <input :value="gaParams.pc" @input="updateGaParam('pc', $event.target.value)" type="number" min="0" max="1" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Mutação</label>
          <input :value="gaParams.pm" @input="updateGaParam('pm', $event.target.value)" type="number" min="0" max="1" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
        </div>
      </div>
    </div>
    
    <div class="mb-4">
      <h5 class="text-xs font-semibold text-green-600 mb-2 uppercase tracking-wide">Colônia de Formigas</h5>
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Formigas</label>
          <input :value="acoParams.tam_pop" @input="updateAcoParam('tam_pop', $event.target.value)" type="number" min="10" max="50" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Iterações</label>
          <input :value="acoParams.n_gen" @input="updateAcoParam('n_gen', $event.target.value)" type="number" min="5" max="50" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Alpha</label>
          <input :value="acoParams.alpha" @input="updateAcoParam('alpha', $event.target.value)" type="number" min="0.1" max="3" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Beta</label>
          <input :value="acoParams.beta" @input="updateAcoParam('beta', $event.target.value)" type="number" min="0.1" max="5" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Rho</label>
          <input :value="acoParams.rho" @input="updateAcoParam('rho', $event.target.value)" type="number" min="0.1" max="0.9" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
        </div>
      </div>
    </div>
    
    <button 
      @click="$emit('compare')" 
      :disabled="loading" 
      class="bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-purple-700 transition-colors shadow-sm"
    >
      <span v-if="loading" class="flex items-center justify-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Comparando...
      </span>
      <span v-else>Executar Comparação</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ComparisonParameters',
  props: {
    gaParams: { type: Object, required: true },
    acoParams: { type: Object, required: true },
    loading: { type: Boolean, default: false }
  },
  emits: ['update:gaParams', 'update:acoParams', 'compare'],
  methods: {
    updateGaParam(key, value) {
      this.$emit('update:gaParams', { ...this.gaParams, [key]: parseFloat(value) })
    },
    updateAcoParam(key, value) {
      this.$emit('update:acoParams', { ...this.acoParams, [key]: parseFloat(value) })
    }
  }
}
</script>
