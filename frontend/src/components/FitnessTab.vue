<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-base font-medium text-text-primary">Evolução da Fitness</h3>
      <div class="flex items-center gap-2 bg-green-50 px-3 py-1 rounded">
        <TrophyIcon class="w-4 h-4 text-green-600" />
        <span class="text-lg font-semibold text-green-700">{{ melhor.toFixed(2) }}</span>
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
    }
  },
  computed: {
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

