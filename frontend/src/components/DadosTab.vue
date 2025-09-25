<template>
  <div class="space-y-6">
    <!-- Projetos -->
    <div>
      <h3 class="flex items-center gap-2 text-base font-medium text-text-primary mb-3">
        <DocumentIcon class="w-4 h-4" />
        Projetos ({{ projetos.length }})
      </h3>
      
      <div v-if="projetos.length === 0" class="flex items-center justify-center h-48 text-text-secondary">
        <div class="text-center">
          <DocumentIcon class="w-12 h-12 mx-auto mb-4 text-text-disabled" />
          <p>Nenhum projeto carregado</p>
        </div>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="projeto in projetos" :key="projeto.nome" class="bg-white rounded-md shadow-sm p-3 hover:shadow-md transition-shadow">
          <div class="flex justify-between items-center mb-3">
            <span class="font-medium text-sm">{{ projeto.nome }}</span>
            <span class="badge badge-info text-xs">{{ projeto.etapas.length }}</span>
          </div>
          
          <div class="space-y-2">
            <div v-for="etapa in projeto.etapas" :key="etapa.nome" class="border-b border-gray-100 pb-2 last:border-b-0">
              <h4 class="font-medium text-text-primary text-sm mb-1">{{ etapa.nome }}</h4>
              <div class="flex flex-wrap gap-1 mb-1">
                <span class="px-1.5 py-0.5 bg-blue-100 text-blue-700 text-xs rounded">{{ etapa.duracao_dias }}d</span>
                <span class="px-1.5 py-0.5 bg-orange-100 text-orange-700 text-xs rounded">{{ etapa.cargo_necessario }}</span>
              </div>
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="hab in etapa.habilidades_necessarias" 
                  :key="hab" 
                  class="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                >
                  {{ hab }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Colaboradores -->
    <div>
      <h3 class="flex items-center gap-2 text-base font-medium text-text-primary mb-3">
        <UserIcon class="w-4 h-4" />
        Colaboradores ({{ colaboradores.length }})
      </h3>
      
      <div v-if="colaboradores.length === 0" class="flex items-center justify-center h-48 text-text-secondary">
        <div class="text-center">
          <UserIcon class="w-12 h-12 mx-auto mb-4 text-text-disabled" />
          <p>Nenhum colaborador carregado</p>
        </div>
      </div>
      
      <div v-else class="bg-white rounded-md shadow-sm overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Cargo</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Habilidades</th>
              <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="colaborador in colaboradores" :key="colaborador.id" class="hover:bg-gray-50">
              <td class="px-3 py-2 text-sm text-center">{{ colaborador.id }}</td>
              <td class="px-3 py-2 text-sm">
                <div class="flex items-center gap-2">
                  <img 
                    :src="`https://api.dicebear.com/7.x/initials/svg?seed=${colaborador.nome}`" 
                    :alt="colaborador.nome"
                    class="w-6 h-6 rounded-full"
                  />
                  <span class="font-medium">{{ colaborador.nome }}</span>
                </div>
              </td>
              <td class="px-3 py-2 text-sm">
                <span class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">{{ colaborador.cargo }}</span>
              </td>
              <td class="px-3 py-2 text-sm">
                <div class="flex flex-wrap gap-1">
                  <span 
                    v-for="hab in colaborador.habilidades.slice(0, 3)" 
                    :key="hab" 
                    class="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                  >
                    {{ hab }}
                  </span>
                  <span v-if="colaborador.habilidades.length > 3" class="px-1.5 py-0.5 bg-gray-200 text-gray-500 text-xs rounded">
                    +{{ colaborador.habilidades.length - 3 }}
                  </span>
                </div>
              </td>
              <td class="px-3 py-2 text-sm">
                <div v-if="colaborador.ausencias.length > 0" class="relative group">
                  <span class="px-2 py-1 bg-red-100 text-red-700 text-xs rounded cursor-pointer">
                    {{ colaborador.ausencias.length }} ausência(s)
                  </span>
                  <div class="absolute z-10 invisible group-hover:visible bg-white border border-gray-200 rounded-md shadow-lg p-2 mt-1 min-w-32">
                    <div v-for="ausencia in colaborador.ausencias" :key="ausencia" class="text-xs text-gray-600">
                      {{ ausencia }}
                    </div>
                  </div>
                </div>
                <span v-else class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Disponível</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { DocumentIcon, UserIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'DadosTab',
  components: {
    DocumentIcon,
    UserIcon
  },
  props: {
    colaboradores: {
      type: Array,
      default: () => []
    },
    projetos: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    console.log('DadosTab - Colaboradores recebidos:', this.colaboradores)
    console.log('DadosTab - Projetos recebidos:', this.projetos)
  },
  watch: {
    colaboradores(newVal) {
      console.log('DadosTab - Colaboradores atualizados:', newVal)
    },
    projetos(newVal) {
      console.log('DadosTab - Projetos atualizados:', newVal)
    }
  }
}
</script>

