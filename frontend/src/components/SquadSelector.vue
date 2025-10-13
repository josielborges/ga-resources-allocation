<template>
  <div class="flex items-center gap-2">
    <label class="text-sm font-medium text-white">Squad:</label>
    <select 
      :value="modelValue" 
      @change="$emit('update:modelValue', $event.target.value ? parseInt($event.target.value) : null)"
      class="px-3 py-1.5 border border-white border-opacity-30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-white bg-white bg-opacity-20 text-white"
    >
      <option v-for="squad in squads" :key="squad.id" :value="squad.id" class="text-gray-900">
        {{ squad.nome }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'SquadSelector',
  props: {
    modelValue: {
      type: Number,
      default: null
    },
    squads: {
      type: Array,
      required: true
    }
  },
  emits: ['update:modelValue']
}
</script>
