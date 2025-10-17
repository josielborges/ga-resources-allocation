<template>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
    <input 
      :value="value" 
      @input="$emit('update', parseFloat($event.target.value))"
      type="range" 
      :min="min" 
      :max="max" 
      :step="step"
      class="form-slider"
    />
    <div class="flex justify-between text-sm text-text-secondary mt-1">
      <span>{{ min }}</span>
      <span class="font-medium">{{ value }}</span>
      <span>{{ max }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ParamSlider',
  props: {
    label: { type: String, required: true },
    value: { type: Number, required: true },
    min: { type: Number, required: true },
    max: { type: Number, required: true },
    step: { type: Number, default: 1 }
  },
  emits: ['update']
}
</script>
