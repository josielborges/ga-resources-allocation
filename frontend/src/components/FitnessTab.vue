<template>
  <div class="fitness-container">
    <h3>Evolução da Fitness</h3>
    <el-card class="chart-card">
      <div class="chart-wrapper">
        <Line v-if="historico && historico.length > 0" :data="chartData" :options="chartOptions" />
        <div v-else class="no-data">
          <el-empty description="Nenhum dado de fitness disponível" />
        </div>
      </div>
    </el-card>
    
    <el-card class="fitness-info">
      <el-statistic title="Melhor Fitness" :value="melhor" :precision="2" />
    </el-card>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
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
  components: { Line },
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
          borderColor: '#409EFF',
          backgroundColor: 'rgba(64, 158, 255, 0.1)',
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

<style scoped>
.fitness-container {
  padding: 20px;
}

.chart-card {
  margin: 20px 0;
  min-height: 450px;
}

.chart-wrapper {
  height: 400px;
  width: 100%;
  position: relative;
}

.fitness-info {
  margin-top: 20px;
  text-align: center;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

h3 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}
</style>