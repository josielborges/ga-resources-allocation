<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" style="margin: 0; padding: 16px;">
    <div class="bg-white rounded-lg w-full max-w-md overflow-hidden shadow-xl">
      <!-- Header -->
      <div class="flex items-center p-4 border-b border-gray-200">
        <div class="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center mr-3">
          <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      </div>
      
      <!-- Content -->
      <div class="p-4">
        <p class="text-gray-600 leading-relaxed">{{ message }}</p>
      </div>
      
      <!-- Footer -->
      <div class="flex justify-end p-4 border-t border-gray-200 bg-gray-50">
        <button 
          @click="close"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium transition-colors"
        >
          Entendi
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Aviso'
    },
    message: {
      type: String,
      default: 'Mensagem de notificação'
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>