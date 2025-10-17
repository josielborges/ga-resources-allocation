<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
      <div class="px-6 py-4 border-b">
        <h3 class="text-lg font-semibold">Salvar Resultado</h3>
      </div>
      <div class="p-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Nome do Resultado</label>
        <input 
          :value="name" 
          @input="$emit('update:name', $event.target.value)"
          type="text" 
          placeholder="Ex: Roadmap Q1 2025" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-main"
          @keyup.enter="$emit('save')"
        />
      </div>
      <div class="px-6 py-4 border-t flex justify-end gap-2">
        <button @click="$emit('close')" class="px-4 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-100">
          Cancelar
        </button>
        <button @click="$emit('save')" :disabled="!name.trim()" class="px-4 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">
          Salvar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SaveResultModal',
  props: {
    name: { type: String, default: '' }
  },
  emits: ['close', 'save', 'update:name']
}
</script>
