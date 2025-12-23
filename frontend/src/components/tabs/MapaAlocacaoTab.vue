<template>
  <div class="space-y-3">
    <div class="bg-white rounded-md shadow-sm border border-gray-200">
      <div class="bg-purple-50 border-b border-purple-200 px-3 py-1.5 flex justify-between items-center">
        <h3 class="flex items-center gap-1.5 text-xs font-semibold text-purple-800">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 6a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 100 4v2a2 2 0 01-2 2H4a2 2 0 01-2-2v-2a2 2 0 100-4V6z"></path>
          </svg>
          Mapa de Alocação por Mês
        </h3>
        <div class="text-xs text-purple-700">
          {{ colaboradoresUnicos.length }} colab. • 12 meses • {{ tarefas.length }} tarefas
        </div>
      </div>
      
      <div style="max-height: 60vh; overflow-y: auto;">
        <table class="w-full">
          <thead class="bg-gray-50 sticky top-0">
            <tr>
              <th class="px-2 py-1.5 text-left text-xs font-medium text-gray-500 uppercase bg-gray-50 border-r" style="width: 150px; max-width: 150px;">
                Colaborador
              </th>
              <th 
                v-for="mes in mesesDoAno" 
                :key="mes.numero"
                class="px-1 py-1.5 text-center text-xs font-medium text-gray-500 uppercase border-l"
                style="width: 70px;"
              >
                {{ mes.nome.substring(0, 3) }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="colaborador in colaboradoresUnicos" :key="colaborador" class="hover:bg-gray-50 border-b border-gray-100">
              <td class="px-2 py-1.5 text-xs font-medium text-gray-900 bg-white border-r truncate" style="width: 150px; max-width: 150px;" :title="colaborador">
                {{ colaborador }}
              </td>
              <td 
                v-for="mes in mesesDoAno" 
                :key="mes.numero"
                class="px-0.5 py-1.5 border-l border-gray-100 relative"
                style="width: 70px; height: 40px;"
              >
                <div class="relative w-full h-full">
                  <!-- Background base -->
                  <div class="absolute w-full h-6 bg-gray-100 rounded top-0"></div>
                  
                  <!-- Tarefas (bottom layer) -->
                  <div 
                    v-for="alocacao in getAlocacoesMes(colaborador, mes.numero)" 
                    :key="alocacao.id"
                    class="absolute h-6 rounded top-0"
                    :style="{
                      left: alocacao.left + '%',
                      width: alocacao.width + '%',
                      backgroundColor: alocacao.cor,
                      zIndex: 1,
                      opacity: 0.9
                    }"
                    :title="alocacao.tooltip"
                  >
                  </div>
                  
                  <!-- Férias (middle layer - visible over tasks) -->
                  <div 
                    v-for="ferias in getFeriasMes(colaborador, mes.numero)" 
                    :key="ferias.id"
                    class="absolute h-6 rounded top-0"
                    :style="{
                      left: ferias.left + '%',
                      width: ferias.width + '%',
                      backgroundColor: '#FEE2E2',
                      backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 3px, #DC2626 3px, #DC2626 4px)',
                      zIndex: 2,
                      border: '2px solid #DC2626',
                      opacity: 0.95
                    }"
                    :title="ferias.tooltip"
                  >
                  </div>
                  
                  <!-- Ausências (top layer - small markers) -->
                  <div 
                    v-for="ausencia in getAusenciasMes(colaborador, mes.numero)" 
                    :key="ausencia.id"
                    class="absolute w-1 h-6 top-0"
                    :style="{
                      left: ausencia.left + '%',
                      backgroundColor: '#1F2937',
                      backgroundImage: 'radial-gradient(circle, #FFFFFF 25%, transparent 25%), radial-gradient(circle, #FFFFFF 25%, transparent 25%)',
                      backgroundSize: '4px 4px',
                      backgroundPosition: '0 0, 2px 2px',
                      zIndex: 3
                    }"
                    :title="ausencia.tooltip"
                  >
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Legenda -->
      <div class="bg-gray-50 border-t border-gray-200 p-2">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Legenda de Projetos -->
          <div>
            <h4 class="text-xs font-medium text-gray-900 mb-1.5">Projetos</h4>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-1">
              <div 
                v-for="projeto in projetosLegenda" 
                :key="projeto.nome"
                class="flex items-center space-x-1"
              >
                <div 
                  class="w-2.5 h-2.5 rounded"
                  :style="{ backgroundColor: projeto.color }"
                ></div>
                <span class="text-xs text-gray-700 truncate">{{ projeto.nome }}</span>
              </div>
            </div>
          </div>
          
          <!-- Legenda de Disponibilidade -->
          <div>
            <h4 class="text-xs font-medium text-gray-900 mb-1.5">Disponibilidade</h4>
            <div class="space-y-1">
              <div class="flex items-center space-x-2">
                <div 
                  class="w-4 h-2.5 rounded border-2" 
                  style="
                    background-color: #FEE2E2;
                    background-image: repeating-linear-gradient(45deg, transparent, transparent 3px, #DC2626 3px, #DC2626 4px);
                    border-color: #DC2626;
                  "
                ></div>
                <span class="text-xs text-gray-700">🏖️ Férias</span>
              </div>
              <div class="flex items-center space-x-2">
                <div 
                  class="w-1 h-2.5" 
                  style="
                    background-color: #1F2937;
                    background-image: radial-gradient(circle, #FFFFFF 25%, transparent 25%), radial-gradient(circle, #FFFFFF 25%, transparent 25%);
                    background-size: 4px 4px;
                    background-position: 0 0, 2px 2px;
                  "
                ></div>
                <span class="text-xs text-gray-700">🚫 Ausências</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-4 h-2.5 rounded bg-gray-100"></div>
                <span class="text-xs text-gray-700">⚪ Disponível</span>
              </div>
            </div>
          </div>
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
    
    getFeriasMes(colaborador, numeroMes) {
      // Get vacation data from any task of this collaborator (they all have the same vacation info)
      const tarefasColaborador = this.tarefas.filter(t => t.colaborador === colaborador)
      if (tarefasColaborador.length === 0) return []
      
      // Use the first task to get vacation info (all tasks have the same collaborator vacation data)
      const primeiraTask = tarefasColaborador[0]
      if (!primeiraTask || !primeiraTask.ferias || primeiraTask.ferias.length === 0) {
        return []
      }
      
      const feriasArray = []
      
      primeiraTask.ferias.forEach((ferias, index) => {
        const dataInicio = this.parseData(ferias.data_inicio)
        const dataFim = this.parseData(ferias.data_fim)
        
        const mesInicio = dataInicio.getMonth() + 1
        const mesFim = dataFim.getMonth() + 1
        
        // Simple check: if vacation overlaps with this month
        if (numeroMes >= mesInicio && numeroMes <= mesFim) {
          const diasNoMes = new Date(dataInicio.getFullYear(), numeroMes, 0).getDate()
          
          let diaInicioMes, diaFimMes
          
          if (numeroMes === mesInicio && numeroMes === mesFim) {
            // Vacation starts and ends in the same month
            diaInicioMes = dataInicio.getDate()
            diaFimMes = dataFim.getDate()
          } else if (numeroMes === mesInicio) {
            // Vacation starts in this month
            diaInicioMes = dataInicio.getDate()
            diaFimMes = diasNoMes
          } else if (numeroMes === mesFim) {
            // Vacation ends in this month
            diaInicioMes = 1
            diaFimMes = dataFim.getDate()
          } else {
            // Vacation spans the entire month
            diaInicioMes = 1
            diaFimMes = diasNoMes
          }
          
          const left = ((diaInicioMes - 1) / diasNoMes) * 100
          const width = ((diaFimMes - diaInicioMes + 1) / diasNoMes) * 100
          
          feriasArray.push({
            id: `ferias-${colaborador}-${index}-${numeroMes}`,
            left: Math.max(0, left),
            width: Math.min(100 - left, width),
            tooltip: `🏖️ Férias: ${ferias.data_inicio} - ${ferias.data_fim} (${ferias.duracao_dias} dias)`
          })
        }
      })
      
      return feriasArray
    },
    
    getAusenciasMes(colaborador, numeroMes) {
      // Get absence data from any task of this collaborator (they all have the same absence info)
      const tarefasColaborador = this.tarefas.filter(t => t.colaborador === colaborador)
      if (tarefasColaborador.length === 0) return []
      
      // Use the first task to get absence info (all tasks have the same collaborator absence data)
      const primeiraTask = tarefasColaborador[0]
      if (!primeiraTask || !primeiraTask.ausencias || primeiraTask.ausencias.length === 0) return []
      
      const ausenciasArray = []
      
      primeiraTask.ausencias.forEach((ausencia, index) => {
        const dataAusencia = this.parseData(ausencia.data)
        const mesAusencia = dataAusencia.getMonth() + 1
        
        if (numeroMes === mesAusencia) {
          const diasNoMes = new Date(dataAusencia.getFullYear(), numeroMes, 0).getDate()
          const diaAusencia = dataAusencia.getDate()
          const left = ((diaAusencia - 1) / diasNoMes) * 100
          
          ausenciasArray.push({
            id: `ausencia-${colaborador}-${index}-${numeroMes}`,
            left: Math.max(0, left),
            tooltip: `🚫 Ausência: ${ausencia.data}`
          })
        }
      })
      
      return ausenciasArray
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