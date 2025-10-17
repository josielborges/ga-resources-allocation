<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-base font-medium text-text-primary">Evolução da Fitness</h3>
      <div class="flex items-center gap-2 px-3 py-1 rounded" :class="totalViolacoes > 0 ? 'bg-red-50' : 'bg-green-50'">
        <svg v-if="totalViolacoes > 0" class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <TrophyIcon v-else class="w-4 h-4 text-green-600" />
        <span class="text-lg font-semibold" :class="totalViolacoes > 0 ? 'text-red-700' : 'text-green-700'">
          {{ totalViolacoes }} {{ totalViolacoes === 1 ? 'Violação' : 'Violações' }}
        </span>
      </div>
    </div>
    
    <div class="bg-white rounded-md shadow-sm p-4">
      <div class="h-[500px] w-full relative">
        <Line v-if="historico && historico.length > 0" :data="chartData" :options="chartOptions" />
        <div v-else class="flex items-center justify-center h-full text-text-secondary">
          <div class="text-center">
            <ChartBarIcon class="w-8 h-8 mx-auto mb-2 text-text-disabled" />
            <p class="text-sm">Nenhum dado disponível</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { ChartBarIcon, TrophyIcon } from '@heroicons/vue/24/outline'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'FitnessTab',
  components: { Line, ChartBarIcon, TrophyIcon },
  props: {
    historico: {
      type: Array,
      default: () => []
    },
    melhor: {
      type: Number,
      default: 0
    },
    ocorrencias: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    totalViolacoes() {
      const ignorar = ['gaps_projeto', 'makespan', 'resource_idle_time']
      return Object.keys(this.ocorrencias || {}).reduce((sum, key) => {
        if (!ignorar.includes(key) && this.ocorrencias[key]) {
          return sum + this.ocorrencias[key].length
        }
        return sum
      }, 0)
    },
    chartData() {
      if (!this.historico || this.historico.length === 0) {
        return { labels: [], datasets: [] }
      }
      
      return {
        labels: this.historico.map((_, i) => `Geração ${i + 1}`),
        datasets: [{
          label: 'Fitness',
          data: this.historico,
          borderColor: '#3ac47d',
          backgroundColor: 'rgba(58, 196, 125, 0.1)',
          tension: 0.1,
          fill: true
        }]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          x: { 
            title: { 
              display: true, 
              text: 'Gerações',
              font: { size: 14 }
            },
            grid: { display: false }
          },
          y: { 
            title: { 
              display: true, 
              text: 'Valor da Fitness',
              font: { size: 14 }
            },
            beginAtZero: false
          }
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false
        }
      }
    }
  }
}
</script>

