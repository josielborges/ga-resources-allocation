<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
      <h3 class="text-lg font-semibold mb-4">{{ title }}</h3>
      <div class="mb-2">
        <div class="flex justify-between text-sm text-gray-600 mb-1">
          <span>Geração {{ current }} de {{ total }}</span>
          <span>{{ calculatedPercent }}% ({{ current }}/{{ total }})</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-cyan-600 to-green-400 transition-all duration-300"
            :style="{ width: calculatedPercent + '%' }"
          ></div>
        </div>
      </div>
      <div class="text-sm text-gray-600 mt-3">
        <span class="font-medium">Melhor Fitness:</span> {{ fitness.toFixed(2) }}
      </div>
      <div v-if="loading" class="mt-4 pt-4 border-t border-gray-200">
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <svg class="animate-spin h-4 w-4 text-cyan-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Aguardando resultado completo...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  props: {
    show: Boolean,
    title: { type: String, default: 'Executando Algoritmo' },
    current: { type: Number, default: 0 },
    total: { type: Number, default: 100 },
    percent: { type: Number, default: 0 },
    fitness: { type: Number, default: 0 },
    loading: { type: Boolean, default: false }
  },
  computed: {
    calculatedPercent() {
      if (this.total === 0) return 0
      const percent = Math.round((this.current / this.total) * 100)
      return Math.min(percent, 100)
    }
  }
}
</script>
