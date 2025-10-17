<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-5xl w-full mx-4 max-h-[90vh] flex flex-col">
      <div class="px-6 py-3 border-b flex justify-between items-center">
        <h3 class="text-base font-semibold text-text-primary">Executar geração do Roadmap</h3>
        <button @click="$emit('close')" class="text-text-secondary hover:text-text-primary">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="flex-1 overflow-y-auto p-4">
        <div v-if="missingSkills.length > 0" class="mb-4 bg-yellow-50 border border-yellow-300 rounded p-3">
          <div class="flex items-start gap-2">
            <svg class="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-yellow-800">Habilidades não cobertas</p>
              <p class="text-xs text-yellow-700 mt-1">Os projetos selecionados requerem habilidades que nenhum colaborador selecionado possui:</p>
              <div class="flex flex-wrap gap-1 mt-2">
                <span v-for="skill in missingSkills" :key="skill" class="inline-block px-2 py-0.5 bg-yellow-200 text-yellow-800 rounded text-xs font-medium">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <slot></slot>
      </div>
      
      <div class="px-4 py-3 border-t flex justify-between items-center bg-gray-50">
        <div class="text-xs text-text-secondary">
          <slot name="footer-info"></slot>
        </div>
        <div class="flex gap-2">
          <button @click="$emit('close')" class="px-3 py-1.5 text-xs border border-gray-300 rounded hover:bg-gray-100">
            Cancelar
          </button>
          <button @click="$emit('execute')" :disabled="disabled" class="px-3 py-1.5 text-xs bg-primary-main text-white rounded hover:bg-primary-light disabled:opacity-50 disabled:cursor-not-allowed">
            Executar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SelectionModal',
  props: {
    missingSkills: { type: Array, default: () => [] },
    disabled: { type: Boolean, default: false }
  },
  emits: ['close', 'execute']
}
</script>
