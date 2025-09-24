<template>
  <div class="dados-container">
    <div class="section">
      <h3><el-icon><Document /></el-icon> Projetos ({{ projetos.length }})</h3>
      
      <div v-if="projetos.length === 0" class="no-data">
        <el-empty description="Nenhum projeto carregado" />
      </div>
      
      <el-row v-else :gutter="20">
        <el-col :xs="24" :sm="12" :lg="8" v-for="projeto in projetos" :key="projeto.nome">
          <el-card class="project-card" shadow="hover">
            <template #header>
              <div class="project-header">
                <span class="project-name">{{ projeto.nome }}</span>
                <el-tag :color="projeto.color" size="small">{{ projeto.etapas.length }} etapas</el-tag>
              </div>
            </template>
            
            <el-table :data="projeto.etapas" size="small" :show-header="false">
              <el-table-column prop="nome" label="Etapa">
                <template #default="scope">
                  <div class="etapa-info">
                    <strong>{{ scope.row.nome }}</strong>
                    <div class="etapa-details">
                      <el-tag size="mini" type="info">{{ scope.row.duracao_dias }} dias</el-tag>
                      <el-tag size="mini" type="warning">{{ scope.row.cargo_necessario }}</el-tag>
                    </div>
                    <div class="habilidades">
                      <el-tag 
                        v-for="hab in scope.row.habilidades_necessarias" 
                        :key="hab" 
                        size="mini" 
                        effect="plain"
                      >
                        {{ hab }}
                      </el-tag>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="section">
      <h3><el-icon><User /></el-icon> Colaboradores ({{ colaboradores.length }})</h3>
      
      <div v-if="colaboradores.length === 0" class="no-data">
        <el-empty description="Nenhum colaborador carregado" />
      </div>
      
      <el-card v-else class="colaboradores-card">
        <el-table :data="colaboradores" size="small" stripe>
          <el-table-column prop="id" label="ID" width="60" align="center" />
          
          <el-table-column prop="nome" label="Nome" width="150">
            <template #default="scope">
              <div class="colaborador-name">
                <el-avatar :size="30" :src="`https://api.dicebear.com/7.x/initials/svg?seed=${scope.row.nome}`" />
                <span>{{ scope.row.nome }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="cargo" label="Cargo" width="120">
            <template #default="scope">
              <el-tag type="success" size="small">{{ scope.row.cargo }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="habilidades" label="Habilidades" min-width="200">
            <template #default="scope">
              <div class="habilidades-list">
                <el-tag 
                  v-for="hab in scope.row.habilidades" 
                  :key="hab" 
                  size="small" 
                  effect="plain"
                  style="margin: 2px"
                >
                  {{ hab }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="ausencias" label="Ausências" width="150">
            <template #default="scope">
              <div v-if="scope.row.ausencias.length > 0" class="ausencias-list">
                <el-popover placement="top" trigger="hover" width="200">
                  <template #reference>
                    <el-tag type="danger" size="small">
                      {{ scope.row.ausencias.length }} ausência(s)
                    </el-tag>
                  </template>
                  <div>
                    <div v-for="ausencia in scope.row.ausencias" :key="ausencia">
                      {{ ausencia }}
                    </div>
                  </div>
                </el-popover>
              </div>
              <el-tag v-else type="success" size="small">Disponível</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import { Document, User } from '@element-plus/icons-vue'

export default {
  name: 'DadosTab',
  components: {
    Document,
    User
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

<style scoped>
.dados-container {
  padding: 20px;
}

.section {
  margin-bottom: 40px;
}

h3 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.project-card {
  margin-bottom: 20px;
  height: 100%;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-name {
  font-weight: 600;
  color: #303133;
}

.etapa-info {
  padding: 8px 0;
}

.etapa-details {
  margin: 8px 0;
  display: flex;
  gap: 8px;
}

.habilidades {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.colaboradores-card {
  overflow-x: auto;
}

.colaborador-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.habilidades-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.ausencias-list {
  cursor: pointer;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  margin: 20px 0;
}

@media (max-width: 768px) {
  .dados-container {
    padding: 10px;
  }
  
  .project-card {
    margin-bottom: 15px;
  }
}
</style>