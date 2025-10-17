<template>
  <div class="w-72 bg-gray-50 border-r border-gray-200 flex-shrink-0 overflow-y-auto">
    <div class="p-4 space-y-4">
      <AlgorithmParameters 
        :params="params"
        :loading="loading"
        @update:params="$emit('update:params', $event)"
        @execute="$emit('execute')"
        @toggle-comparison="$emit('toggle-comparison')"
      />
      <ComparisonParameters 
        v-if="showComparison"
        :ga-params="gaParams"
        :aco-params="acoParams"
        :loading="loading"
        @update:ga-params="$emit('update:gaParams', $event)"
        @update:aco-params="$emit('update:acoParams', $event)"
        @compare="$emit('compare')"
      />
    </div>
  </div>
</template>

<script>
import AlgorithmParameters from './AlgorithmParameters.vue'
import ComparisonParameters from './ComparisonParameters.vue'

export default {
  name: 'RoadmapSidebar',
  components: { AlgorithmParameters, ComparisonParameters },
  props: {
    projetosCount: { type: Number, default: 0 },
    colaboradoresCount: { type: Number, default: 0 },
    params: { type: Object, required: true },
    gaParams: { type: Object, required: true },
    acoParams: { type: Object, required: true },
    loading: { type: Boolean, default: false },
    showComparison: { type: Boolean, default: false }
  },
  emits: ['update:params', 'update:gaParams', 'update:acoParams', 'execute', 'toggle-comparison', 'compare']
}
</script>
