<template>
  <div class="space-y-3">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-text-primary">Mapa de Alocação dos Colaboradores por Mês</h3>
      <div class="text-sm text-text-secondary">
        {{ colaboradoresUnicos.length }} colaboradores • 12 meses • {{ tarefas.length }} tarefas
      </div>
    </div>
    
    <div class="bg-white rounded-md border" style="max-height: 70vh; overflow-y: auto;">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-2 py-2 text-left text-xs font-medium text-gray-500 uppercase bg-gray-50 border-r" style="width: 180px; max-width: 180px;">
              Colaborador
            </th>
            <th 
              v-for="mes in mesesDoAno" 
              :key="mes.numero"
              class="px-1 py-2 text-center text-xs font-medium text-gray-500 uppercase border-l"
              style="width: 80px;"
            >
              {{ mes.nome.substring(0, 3) }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr v-for="colaborador in colaboradoresUnicos" :key="colaborador" class="hover:bg-gray-50 border-b border-gray-100">
            <td class="px-2 py-2 text-sm font-medium text-gray-900 bg-white border-r truncate" style="width: 180px; max-width: 180px;" :title="colaborador">
              {{ colaborador }}
            </td>
            <td 
              v-for="mes in mesesDoAno" 
              :key="mes.numero"
              class="px-0.5 py-2 border-l border-gray-100 relative"
              style="width: 80px; height: 40px;"
            >
              <div class="relative w-full h-6 bg-gray-100 rounded">
                <div 
                  v-for="alocacao in getAlocacoesMes(colaborador, mes.numero)" 
                  :key="alocacao.id"
                  class="absolute h-6 rounded"
                  :style="{
                    left: alocacao.left + '%',
                    width: alocacao.width + '%',
                    backgroundColor: alocacao.cor
                  }"
                  :title="alocacao.tooltip"
                >
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Legenda -->
    <div class="bg-gray-50 rounded-md p-3">
      <h4 class="text-sm font-medium text-gray-900 mb-2">Legenda de Projetos</h4>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-1">
        <div 
          v-for="projeto in projetosLegenda" 
          :key="projeto.nome"
          class="flex items-center space-x-1.5"
        >
          <div 
            class="w-3 h-3 rounded"
            :style="{ backgroundColor: projeto.color }"
          ></div>
          <span class="text-xs text-gray-700 truncate">{{ projeto.nome }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapaAlocacaoTab',
  props: {
    tarefas: {
      type: Array,
      required: true
    },
    projetos: {
      type: Array,
      required: true
    },
    colaboradores: {
      type: Array,
      required: true
    }
  },
  computed: {
    colaboradoresUnicos() {
      return this.colaboradores.map(c => c.nome).sort()
    },
    

    
    projetosLegenda() {
      const projetosUnicos = [...new Set(this.tarefas.map(t => t.projeto))]
      return projetosUnicos.map(nomeProjeto => {
        const projeto = this.projetos.find(p => p.nome === nomeProjeto)
        return {
          nome: nomeProjeto,
          color: projeto?.color || this.getProjectColor(nomeProjeto)
        }
      })
    },
    
    mesesDoAno() {
      return [
        { numero: 1, nome: 'Janeiro' },
        { numero: 2, nome: 'Fevereiro' },
        { numero: 3, nome: 'Março' },
        { numero: 4, nome: 'Abril' },
        { numero: 5, nome: 'Maio' },
        { numero: 6, nome: 'Junho' },
        { numero: 7, nome: 'Julho' },
        { numero: 8, nome: 'Agosto' },
        { numero: 9, nome: 'Setembro' },
        { numero: 10, nome: 'Outubro' },
        { numero: 11, nome: 'Novembro' },
        { numero: 12, nome: 'Dezembro' }
      ]
    }
  },
  methods: {
    parseData(dataStr) {
      const [dia, mes, ano] = dataStr.split('/')
      return new Date(ano, mes - 1, dia)
    },
    
    getAlocacoesMes(colaborador, numeroMes) {
      const tarefasColaborador = this.tarefas.filter(t => t.colaborador === colaborador)
      const alocacoes = []
      
      tarefasColaborador.forEach((tarefa, index) => {
        const dataInicio = this.parseData(tarefa.data_inicio)
        const dataFim = this.parseData(tarefa.data_fim)
        
        const mesInicio = dataInicio.getMonth() + 1
        const mesFim = dataFim.getMonth() + 1
        
        if (numeroMes >= mesInicio && numeroMes <= mesFim) {
          const diasNoMes = new Date(dataInicio.getFullYear(), numeroMes, 0).getDate()
          
          let diaInicioMes, diaFimMes
          
          if (numeroMes === mesInicio && numeroMes === mesFim) {
            // Tarefa começa e termina no mesmo mês
            diaInicioMes = dataInicio.getDate()
            diaFimMes = dataFim.getDate()
          } else if (numeroMes === mesInicio) {
            // Tarefa começa neste mês
            diaInicioMes = dataInicio.getDate()
            diaFimMes = diasNoMes
          } else if (numeroMes === mesFim) {
            // Tarefa termina neste mês
            diaInicioMes = 1
            diaFimMes = dataFim.getDate()
          } else {
            // Tarefa ocupa o mês inteiro
            diaInicioMes = 1
            diaFimMes = diasNoMes
          }
          
          const left = ((diaInicioMes - 1) / diasNoMes) * 100
          const width = ((diaFimMes - diaInicioMes + 1) / diasNoMes) * 100
          
          const projeto = this.projetos.find(p => p.nome === tarefa.projeto)
          
          alocacoes.push({
            id: `${tarefa.projeto}-${index}`,
            left: Math.max(0, left),
            width: Math.min(100 - left, width),
            cor: projeto?.color || this.getProjectColor(tarefa.projeto),
            tooltip: `${tarefa.projeto} - ${tarefa.nome_tarefa} (${tarefa.data_inicio} - ${tarefa.data_fim})`
          })
        }
      })
      
      return alocacoes
    },
    
    getProjectColor(projeto) {
      const colors = ['#3f6ad8', '#3ac47d', '#f7b924', '#d92550', '#16aaff', '#9C27B0', '#FF9800']
      const projects = [...new Set(this.tarefas.map(t => t.projeto))]
      const colorMap = {}
      projects.forEach((project, index) => {
        colorMap[project] = colors[index % colors.length]
      })
      return colorMap[projeto] || '#3f6ad8'
    },
    
    getSiglaProjeto(nomeProjeto) {
      return nomeProjeto
        .split(' ')
        .map(palavra => palavra.charAt(0).toUpperCase())
        .join('')
        .substring(0, 3)
    }
  }
}
</script>