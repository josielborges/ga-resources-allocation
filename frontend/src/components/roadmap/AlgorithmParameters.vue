<template>
  <div class="bg-white rounded-md shadow-sm p-4">
    <h3 class="text-base font-semibold text-gray-900 mb-4">Parâmetros do Algoritmo</h3>
    
    <form class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Algoritmo</label>
        <select :value="params.algorithm" @input="$emit('update:params', { ...params, algorithm: $event.target.value })" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main">
          <option value="ga">Algoritmo Genético</option>
          <option value="aco">Colônia de Formigas</option>
        </select>
      </div>
      
      <template v-if="params.algorithm === 'ga'">
        <ParamSlider label="População" :value="params.tam_pop" :min="10" :max="100" 
                     @update="$emit('update:params', { ...params, tam_pop: $event })" />
        <ParamSlider label="Gerações" :value="params.n_gen" :min="5" :max="1000" 
                     @update="$emit('update:params', { ...params, n_gen: $event })" />
        <ParamSlider label="Crossover" :value="params.pc" :min="0" :max="1" :step="0.1" 
                     @update="$emit('update:params', { ...params, pc: $event })" />
        <ParamSlider label="Mutação" :value="params.pm" :min="0" :max="1" :step="0.1" 
                     @update="$emit('update:params', { ...params, pm: $event })" />
      </template>
      
      <template v-else>
        <ParamSlider label="Número de Formigas" :value="params.tam_pop" :min="10" :max="50" 
                     @update="$emit('update:params', { ...params, tam_pop: $event })" />
        <ParamSlider label="Iterações Máximas" :value="params.n_gen" :min="5" :max="50" 
                     @update="$emit('update:params', { ...params, n_gen: $event })" />
        <ParamSlider label="Alpha (Feromônio)" :value="params.alpha" :min="0.1" :max="3" :step="0.1" 
                     @update="$emit('update:params', { ...params, alpha: $event })" />
        <ParamSlider label="Beta (Heurística)" :value="params.beta" :min="0.1" :max="5" :step="0.1" 
                     @update="$emit('update:params', { ...params, beta: $event })" />
        <ParamSlider label="Rho (Evaporação)" :value="params.rho" :min="0.1" :max="0.9" :step="0.1" 
                     @update="$emit('update:params', { ...params, rho: $event })" />
      </template>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Data de Referência</label>
        <input 
          :value="params.ref_date" 
          @input="$emit('update:params', { ...params, ref_date: $event.target.value })"
          type="date" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
        />
      </div>
      
      <div class="space-y-2 pt-4">
        <button 
          @click="$emit('execute')" 
          :disabled="loading" 
          class="bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
          type="button"
        >
          Executar {{ params.algorithm.toUpperCase() }}
        </button>
        
        <button 
          @click="$emit('toggle-comparison')" 
          class="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full hover:bg-green-700 transition-colors shadow-sm"
          type="button"
        >
          Configurar Comparação
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import ParamSlider from './ParamSlider.vue'

export default {
  name: 'AlgorithmParameters',
  components: { ParamSlider },
  props: {
    params: { type: Object, required: true },
    loading: { type: Boolean, default: false }
  },
  emits: ['update:params', 'execute', 'toggle-comparison']
}
</script>
