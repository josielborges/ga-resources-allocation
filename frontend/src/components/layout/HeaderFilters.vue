<template>
  <div class="text-white px-6 py-4 shadow-sm flex-shrink-0 flex items-center justify-between" 
       style="background: linear-gradient(to bottom, #0891B2, #0C94AD);">
    <h1 class="text-xl font-semibold">{{ title }}</h1>
    <div class="flex items-center gap-3">
      <select 
        :value="selectedTriboId" 
        @change="$emit('update:selectedTriboId', $event.target.value ? parseInt($event.target.value) : null); $emit('triboChange')"
        class="px-3 py-1.5 border border-white border-opacity-30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-white bg-white bg-opacity-20 text-white"
      >
        <option :value="null" selected class="text-gray-900">Tribo</option>
        <option v-for="tribo in tribos" :key="tribo.id" :value="tribo.id" class="text-gray-900">
          {{ tribo.nome }}
        </option>
      </select>
      <SquadSelector :modelValue="selectedSquadId" :squads="squads" @update:modelValue="$emit('update:selectedSquadId', $event); $emit('squadChange')" />
      <select 
        :value="selectedYear" 
        @change="$emit('update:selectedYear', $event.target.value ? parseInt($event.target.value) : null); $emit('yearChange')"
        class="px-3 py-1.5 border border-white border-opacity-30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-white bg-white bg-opacity-20 text-white"
      >
        <option :value="null" selected class="text-gray-900">Ano</option>
        <option v-for="year in availableYears" :key="year" :value="year" class="text-gray-900">
          {{ year }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import SquadSelector from '../common/SquadSelector.vue'

export default {
  name: 'HeaderFilters',
  components: { SquadSelector },
  props: {
    title: { type: String, required: true },
    selectedTriboId: { type: Number, default: null },
    selectedSquadId: { type: Number, default: null },
    selectedYear: { type: Number, default: null },
    tribos: { type: Array, default: () => [] },
    squads: { type: Array, default: () => [] },
    years: { type: Array, default: () => [] }
  },
  computed: {
    availableYears() {
      return this.years
    }
  },
  emits: ['update:selectedTriboId', 'update:selectedSquadId', 'update:selectedYear', 'triboChange', 'squadChange', 'yearChange']
}
</script>
