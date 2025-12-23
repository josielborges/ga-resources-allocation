<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[85vh] flex flex-col">
      <div class="px-6 py-4 border-b flex justify-between items-center">
        <h3 class="text-lg font-semibold">Resultados Salvos ({{ resultados.length }})</h3>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="flex-1 overflow-y-auto p-6">
        <div v-if="resultados.length === 0" class="text-center py-8 text-gray-500">
          <svg class="w-16 h-16 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>Nenhum resultado salvo ainda</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div 
            v-for="resultado in resultados" 
            :key="resultado.id" 
            @click="$emit('load', resultado.id)"
            class="bg-white border rounded-lg p-4 hover:shadow-lg transition-all group relative cursor-pointer h-[130px]"
          >
            <button 
              @click.stop="$emit('delete', resultado.id)" 
              class="absolute top-2 right-2 p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors opacity-0 group-hover:opacity-100"
              title="Deletar"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
            <div class="flex items-start justify-between mb-2 pr-6">
              <h5 class="font-semibold text-gray-900 text-sm line-clamp-2 flex-1">{{ resultado.nome }}</h5>
              <span class="text-xs px-2 py-0.5 rounded flex-shrink-0 ml-2 bg-purple-100 text-purple-700">{{ resultado.algoritmo ? resultado.algoritmo.toUpperCase() : 'CP' }}</span>
            </div>
            <div class="text-xs text-gray-600 space-y-1">
              <p><span class="font-medium">Fitness:</span> {{ resultado.melhor_fitness.toFixed(2) }}</p>
              <p v-if="resultado.parametros?.projeto_ids" class="flex items-center gap-1">
                <span class="font-medium">Projetos:</span> {{ resultado.parametros.projeto_ids.length }}
              </p>
              <p><span class="font-medium">Salvo em:</span> {{ formatDate(resultado.data_execucao) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadResultModal',
  props: {
    resultados: { type: Array, default: () => [] }
  },
  emits: ['close', 'load', 'delete'],
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>
