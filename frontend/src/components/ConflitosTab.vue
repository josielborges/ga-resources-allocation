<template>
  <div>
    <h3>Resumo das Penalidades</h3>
    <el-table :data="penalityData" size="small" style="margin-bottom: 20px">
      <el-table-column prop="motivo" label="Motivo" />
      <el-table-column prop="valor" label="Valor" />
    </el-table>

    <div v-for="(ocorrencias, tipo) in ocorrencias" :key="tipo">
      <h4 v-if="ocorrencias.length > 0">{{ translatePenalty(tipo) }}</h4>
      <el-table v-if="ocorrencias.length > 0" :data="ocorrencias" size="small" style="margin-bottom: 20px">
        <el-table-column v-for="(value, key) in ocorrencias[0]" :key="key" :prop="key" :label="key" />
      </el-table>
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