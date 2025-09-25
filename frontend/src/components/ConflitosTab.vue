<template>
  <div class="space-y-4">
    <div>
      <div class="bg-red-50 border-l-4 border-red-400 p-3 mb-3">
        <h3 class="text-lg font-semibold text-red-800 flex items-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          Resumo das Penalidades
        </h3>
      </div>
      <div class="bg-white rounded-md shadow-sm overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Motivo</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Valor</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in penalityData" :key="item.motivo" class="hover:bg-gray-50">
              <td class="px-3 py-1.5 text-sm">{{ item.motivo }}</td>
              <td class="px-3 py-1.5 text-sm font-semibold text-red-600">{{ item.valor }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-for="(ocorrencias, tipo) in ocorrencias" :key="tipo">
      <div v-if="ocorrencias.length > 0">
        <div class="bg-orange-50 border-l-4 border-orange-400 p-2 mb-3">
          <h4 class="text-base font-semibold text-orange-800 flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
            {{ translatePenalty(tipo) }}
          </h4>
        </div>
        <div class="bg-white rounded-md shadow-sm overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="(value, key) in ocorrencias[0]" :key="key" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                  {{ key }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in ocorrencias" :key="index" class="hover:bg-gray-50">
                <td v-for="(value, key) in item" :key="key" class="px-3 py-1.5 text-sm">
                  {{ value }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConflitosTab',
  props: {
    penalidades: Object,
    ocorrencias: Object
  },
  computed: {
    penalityData() {
      return Object.entries(this.penalidades).map(([key, value]) => ({
        motivo: this.translatePenalty(key),
        valor: value
      }))
    }
  },
  methods: {
    translatePenalty(key) {
      const translations = {
        'habilidades_incorretas': 'Habilidades Incorretas',
        'cargo_incorreto': 'Cargo Incorreto',
        'ausencias': 'Ausências',
        'sobreposicoes_colaborador': 'Sobreposições de Colaborador',
        'sobreposicoes_projeto': 'Sobreposições de Projeto',
        'makespan': 'Makespan'
      }
      return translations[key] || key
    }
  }
}
</script>