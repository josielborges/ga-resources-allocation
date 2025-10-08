<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" style="margin: 0; padding: 16px;">
    <div class="bg-white rounded-lg w-full max-w-sm overflow-hidden shadow-xl">
      <!-- Header -->
      <div class="flex items-center p-3 border-b border-gray-200">
        <div class="w-8 h-8 rounded-full bg-yellow-100 flex items-center justify-center mr-2">
          <svg class="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h3 class="text-base font-semibold text-gray-900">{{ title }}</h3>
      </div>
      
      <!-- Content -->
      <div class="p-3">
        <p class="text-sm text-gray-600">{{ message }}</p>
      </div>
      
      <!-- Footer -->
      <div class="flex justify-end p-3 border-t border-gray-200 bg-gray-50">
        <button 
          @click="close"
          class="px-3 py-1.5 bg-primary-main text-white rounded text-sm font-medium hover:bg-primary-light transition-colors"
        >
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Atenção'
    },
    message: {
      type: String,
      default: ''
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>
