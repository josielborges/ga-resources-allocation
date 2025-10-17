<template>
  <div class="space-y-3">
    <!-- Projetos -->
    <div class="bg-white rounded-md shadow-sm border border-gray-200">
      <div class="bg-blue-50 border-b border-blue-200 px-3 py-1.5">
        <h3 class="flex items-center gap-1.5 text-xs font-semibold text-blue-800">
          <DocumentIcon class="w-3.5 h-3.5" />
          Projetos ({{ projetos.length }})
        </h3>
      </div>
      
      <div v-if="projetos.length === 0" class="flex items-center justify-center h-32 text-gray-400 text-xs">
        <div class="text-center">
          <DocumentIcon class="w-8 h-8 mx-auto mb-2 text-gray-300" />
          <p>Nenhum projeto carregado</p>
        </div>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Projeto</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Etapa</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duração</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cargo</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Habilidades</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <template v-for="projeto in projetos" :key="projeto.nome">
              <tr v-for="(etapa, index) in projeto.etapas" :key="etapa.nome" class="hover:bg-gray-50">
                <td v-if="index === 0" :rowspan="projeto.etapas.length" class="px-3 py-1 text-sm font-medium border-r border-gray-200 bg-gray-50">
                  {{ projeto.nome }}
                </td>
                <td class="px-3 py-1 text-xs text-gray-700">{{ etapa.nome }}</td>
                <td class="px-3 py-1 text-xs">
                  <span class="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded font-medium">{{ etapa.duracao_dias }}d</span>
                </td>
                <td class="px-3 py-1 text-xs">
                  <span class="px-1.5 py-0.5 bg-orange-100 text-orange-700 text-xs rounded">{{ etapa.cargo_necessario?.nome || etapa.cargo_necessario }}</span>
                </td>
                <td class="px-3 py-1 text-xs">
                  <div class="flex flex-wrap gap-1">
                    <span 
                      v-for="hab in etapa.habilidades_necessarias" 
                      :key="hab.nome || hab" 
                      class="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                    >
                      {{ hab.nome || hab }}
                    </span>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Colaboradores -->
    <div class="bg-white rounded-md shadow-sm border border-gray-200">
      <div class="bg-green-50 border-b border-green-200 px-3 py-1.5">
        <h3 class="flex items-center gap-1.5 text-xs font-semibold text-green-800">
          <UserIcon class="w-3.5 h-3.5" />
          Colaboradores ({{ colaboradores.length }})
        </h3>
      </div>
      
      <div v-if="colaboradores.length === 0" class="flex items-center justify-center h-32 text-gray-400 text-xs">
        <div class="text-center">
          <UserIcon class="w-8 h-8 mx-auto mb-2 text-gray-300" />
          <p>Nenhum colaborador carregado</p>
        </div>
      </div>
      
      <div v-else>
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cargo</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Habilidades</th>
              <th class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="colaborador in colaboradores" :key="colaborador.id" class="hover:bg-gray-50">
              <td class="px-3 py-1 text-xs text-center text-gray-600">{{ colaborador.id }}</td>
              <td class="px-3 py-1 text-xs">
                <div class="flex items-center gap-1.5">
                  <img 
                    :src="`https://api.dicebear.com/7.x/initials/svg?seed=${colaborador.nome}`" 
                    :alt="colaborador.nome"
                    class="w-5 h-5 rounded-full"
                  />
                  <span class="font-medium text-gray-700">{{ colaborador.nome }}</span>
                </div>
              </td>
              <td class="px-3 py-1 text-xs">
                <span class="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded">{{ colaborador.cargo?.nome || colaborador.cargo }}</span>
              </td>
              <td class="px-3 py-1 text-xs">
                <div class="flex flex-wrap gap-1">
                  <span 
                    v-for="hab in colaborador.habilidades.slice(0, 3)" 
                    :key="hab.nome || hab" 
                    class="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                  >
                    {{ hab.nome || hab }}
                  </span>
                  <span v-if="colaborador.habilidades.length > 3" class="px-1.5 py-0.5 bg-gray-200 text-gray-500 text-xs rounded">
                    +{{ colaborador.habilidades.length - 3 }}
                  </span>
                </div>
              </td>
              <td class="px-3 py-1 text-xs">
                <div v-if="colaborador.ausencias.length > 0" class="relative group">
                  <span class="px-1.5 py-0.5 bg-red-100 text-red-700 text-xs rounded cursor-pointer">
                    {{ colaborador.ausencias.length }} ausência(s)
                  </span>
                  <div class="absolute z-10 invisible group-hover:visible bg-white border border-gray-200 rounded-md shadow-lg p-2 mt-1 min-w-32">
                    <div v-for="ausencia in colaborador.ausencias" :key="ausencia" class="text-xs text-gray-600">
                      {{ ausencia }}
                    </div>
                  </div>
                </div>
                <span v-else class="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded">Disponível</span>
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

