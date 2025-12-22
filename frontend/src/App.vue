<template>
  <div class="h-screen bg-background-default font-sans overflow-hidden">
    <div class="flex h-full">
      <Sidebar :activeModule="activeModule" @update:activeModule="activeModule = $event" @reload="reloadApp" />

      <!-- Área do Roadmap com header estendido -->
      <div v-if="activeModule === 'roadmap'" class="flex-1 flex flex-col">
        <HeaderFilters 
          :title="getModuleTitle()"
          :tribos="tribos"
          :squads="filteredSquads"
          :years="availableYears"
          v-model:selectedTriboId="selectedTriboId"
          v-model:selectedSquadId="selectedSquadId"
          v-model:selectedYear="selectedYear"
          @triboChange="onTriboChange"
          @squadChange="applySquadFilter"
          @yearChange="applyYearFilter"
        />
        
        <!-- Conteúdo do roadmap -->
        <div class="flex flex-1 overflow-hidden">
          <!-- Conteúdo principal -->
          <div class="flex-1 p-4 overflow-y-auto">
            <div v-if="!selectedSquadId" class="flex items-center justify-center h-full">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Selecione um Squad</h3>
                <p class="text-gray-500">Por favor, selecione um squad no seletor acima para visualizar o roadmap</p>
              </div>
            </div>
            <div v-if="!selectedYear" class="flex items-center justify-center h-full">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Selecione o Ano do Roadmap</h3>
                <p class="text-gray-500">Por favor, selecione um ano no filtro acima para visualizar os projetos</p>
              </div>
            </div>
            <div v-else-if="!resultado" class="space-y-4 p-4">
              <!-- Top Row: Actions + Quick Stats -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <!-- Actions -->
                <div class="lg:col-span-2 bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500">
                  <h2 class="text-lg font-bold text-gray-900 mb-1">Gerador de Roadmap</h2>
                  <p class="text-xs text-gray-600 mb-3">Otimize a alocação usando GA ou ACO</p>
                  <div class="flex gap-2">
                    <button 
                      @click="showSelectionModal = true" 
                      :disabled="!selectedSquadId || !selectedYear"
                      class="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      <span>Executar</span>
                    </button>
                    <button 
                      @click="showComparisonModal = true" 
                      :disabled="!selectedSquadId || !selectedYear"
                      class="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <span>Comparar</span>
                    </button>
                    <button 
                      v-if="resultadosSalvos.length > 0"
                      @click="showLoadModal = true" 
                      class="bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition-all flex items-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span>Carregar ({{ resultadosSalvos.length }})</span>
                    </button>
                  </div>
                </div>
                
                <!-- Saved Results Summary -->
                <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-cyan-500">
                  <div class="flex items-center justify-between mb-2">
                    <h3 class="text-sm font-bold text-gray-900">Execuções Salvas</h3>
                    <svg class="w-5 h-5 text-cyan-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                      <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <p class="text-3xl font-bold text-gray-900">{{ resultadosSalvos.length }}</p>
                  <p class="text-xs text-gray-500 mt-1">Total de roadmaps</p>
                </div>
              </div>

              <!-- Stats Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <div @click="showColaboradoresModal = true" class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer p-3 border-l-4 border-blue-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Colaboradores</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ colaboradores.length }}</p>
                </div>
                
                <div @click="showProjetosModal = true" class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer p-3 border-l-4 border-green-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Projetos</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ projetos.length }}</p>
                </div>
                
                <div class="bg-white rounded-lg shadow-sm p-3 border-l-4 border-indigo-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Etapas</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ projetos.reduce((sum, p) => sum + (p.etapas?.length || 0), 0) }}</p>
                </div>
                
                <div @click="showCargosModal = true" class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer p-3 border-l-4 border-purple-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"/>
                      <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Cargos</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ cargos.length }}</p>
                </div>
                
                <div @click="showHabilidadesModal = true" class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer p-3 border-l-4 border-orange-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Habilidades</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ habilidades.length }}</p>
                </div>
                
                <div class="bg-white rounded-lg shadow-sm p-3 border-l-4 border-pink-500">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-5 h-5 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
                    </svg>
                    <p class="text-xs text-gray-600 font-medium">Transversais</p>
                  </div>
                  <p class="text-2xl font-bold text-gray-900">{{ transversais.length }}</p>
                </div>
              </div>

              <!-- Recent Executions -->
              <div v-if="resultadosSalvos.length > 0" class="bg-white rounded-xl shadow-md p-6">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                    <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                      <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
                    </svg>
                    Execuções Recentes
                  </h3>
                  <button 
                    @click="showLoadModal = true" 
                    class="text-sm text-purple-600 hover:text-purple-800 font-medium flex items-center gap-1"
                  >
                    Ver todos ({{ resultadosSalvos.length }})
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div 
                    v-for="resultado in resultadosSalvos.slice(0, 6)" 
                    :key="resultado.id" 
                    @click="carregarResultado(resultado.id)"
                    class="bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-200 rounded-lg p-4 hover:shadow-lg hover:border-purple-300 transition-all cursor-pointer group"
                  >
                    <div class="flex items-start justify-between mb-3">
                      <h5 class="font-semibold text-gray-900 text-sm group-hover:text-purple-600 transition-colors line-clamp-2 flex-1">{{ resultado.nome }}</h5>
                      <span class="text-xs px-2 py-1 rounded-full font-bold flex-shrink-0 ml-2" :class="resultado.algoritmo === 'ga' ? 'bg-blue-500 text-white' : 'bg-green-500 text-white'">{{ resultado.algoritmo.toUpperCase() }}</span>
                    </div>
                    <div class="space-y-2">
                      <div class="flex items-center justify-between text-xs">
                        <span class="text-gray-600">Fitness</span>
                        <span class="font-bold text-gray-900">{{ resultado.melhor_fitness.toFixed(2) }}</span>
                      </div>
                      <div v-if="resultado.parametros?.projeto_ids" class="flex items-center justify-between text-xs">
                        <span class="text-gray-600">Projetos</span>
                        <span class="font-bold text-gray-900">{{ resultado.parametros.projeto_ids.length }}</span>
                      </div>
                      <div v-if="getRoadmapEndDate(resultado)" class="flex items-center justify-between text-xs">
                        <span class="text-gray-600">Término</span>
                        <span class="font-bold text-gray-900">{{ getRoadmapEndDate(resultado) }}</span>
                      </div>
                      <div class="pt-2 border-t border-gray-300">
                        <p class="text-xs text-gray-500">{{ new Date(resultado.data_execucao).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Quick Info -->
              <div v-else class="bg-white rounded-xl shadow-md p-8 text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Nenhuma execução salva</h3>
                <p class="text-gray-500">Execute um algoritmo e salve o resultado para vê-lo aqui</p>
              </div>
            </div>

            <div v-if="resultado" class="bg-white rounded-md shadow-sm">
              <div class="border-b border-divider px-4">
                <div class="flex justify-between items-center">
                  <nav class="flex space-x-6">
                    <button 
                      v-for="tab in tabs" 
                      :key="tab.name"
                      @click="activeTab = tab.name"
                      :class="[
                        'py-3 px-1 border-b-2 font-medium text-sm transition-colors',
                        activeTab === tab.name 
                          ? 'border-primary-main text-primary-main' 
                          : 'border-transparent text-text-secondary hover:text-text-primary hover:border-gray-300'
                      ]"
                    >
                      {{ tab.label }}
                    </button>
                  </nav>
                  <button 
                    @click="showSaveModal = true" 
                    class="bg-green-600 text-white px-3 py-1.5 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
                  >
                    Salvar Resultado
                  </button>
                </div>
              </div>
              
              <div class="p-4">
                <DadosTab v-if="activeTab === 'dados'" :colaboradores="colaboradores" :projetos="projetos" />
                <FitnessTab v-if="activeTab === 'fitness'" :historico="resultado.historico_fitness" :melhor="resultado.melhor_fitness" :ocorrencias="resultado.ocorrencias_penalidades" />
                <ConflitosTab v-if="activeTab === 'conflitos'" :penalidades="resultado.penalidades" :ocorrencias="resultado.ocorrencias_penalidades" :ref-date="params.ref_date" />
                <GanttTab v-if="activeTab === 'gantt'" :tarefas="resultado.tarefas" :penalidades="resultado.penalidades" :ocorrencias="resultado.ocorrencias_penalidades" :projetos="projetos" :ref-date="params.ref_date" />
                <CalendarioTab v-if="activeTab === 'calendario'" :tarefas="resultado.tarefas" :projetos="projetos" />
                <MapaAlocacaoTab v-if="activeTab === 'mapa'" :tarefas="resultado.tarefas" :projetos="projetos" :colaboradores="allColaboradoresWithSimulated" />
                <div v-if="activeTab === 'comparacao'" class="space-y-4">
                  <div v-if="!comparacaoResultado" class="text-center py-8">
                    <p class="text-text-secondary">Use o botão "Comparar GA vs ACO" para ver a análise comparativa dos algoritmos.</p>
                  </div>
                  <div v-else>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 class="font-semibold text-blue-800 mb-2">Algoritmo Genético (GA)</h4>
                        <div class="space-y-1 text-sm">
                          <p><span class="font-medium">Melhor Fitness:</span> {{ comparacaoResultado.ga_stats.best_fitness.toFixed(2) }}</p>
                          <p><span class="font-medium">Fitness Médio:</span> {{ comparacaoResultado.ga_stats.avg_fitness.toFixed(2) }}</p>
                          <p><span class="font-medium">Tempo Médio:</span> {{ comparacaoResultado.ga_stats.avg_time.toFixed(2) }}s</p>
                          <p><span class="font-medium">Convergência:</span> {{ comparacaoResultado.ga_stats.avg_convergence.toFixed(0) }} gerações</p>
                        </div>
                      </div>
                      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                        <h4 class="font-semibold text-green-800 mb-2">Otimização por Colônia de Formigas (ACO)</h4>
                        <div class="space-y-1 text-sm">
                          <p><span class="font-medium">Melhor Fitness:</span> {{ comparacaoResultado.aco_stats.best_fitness.toFixed(2) }}</p>
                          <p><span class="font-medium">Fitness Médio:</span> {{ comparacaoResultado.aco_stats.avg_fitness.toFixed(2) }}</p>
                          <p><span class="font-medium">Tempo Médio:</span> {{ comparacaoResultado.aco_stats.avg_time.toFixed(2) }}s</p>
                          <p><span class="font-medium">Convergência:</span> {{ comparacaoResultado.aco_stats.avg_convergence.toFixed(0) }} iterações</p>
                        </div>
                      </div>
                    </div>
                    <div class="bg-white border rounded-lg p-4">
                      <h4 class="font-semibold mb-3">Análise Comparativa</h4>
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div class="text-center">
                          <p class="font-medium text-lg" :class="comparacaoResultado.comparison.winner === 'ACO' ? 'text-green-600' : 'text-blue-600'">
                            {{ comparacaoResultado.comparison.winner }}
                          </p>
                          <p class="text-text-secondary">Vencedor</p>
                        </div>
                        <div class="text-center">
                          <p class="font-medium text-lg" :class="comparacaoResultado.comparison.fitness_improvement > 0 ? 'text-green-600' : 'text-red-600'">
                            {{ comparacaoResultado.comparison.fitness_improvement.toFixed(1) }}%
                          </p>
                          <p class="text-text-secondary">Melhoria no Fitness</p>
                        </div>
                        <div class="text-center">
                          <p class="font-medium text-lg">
                            {{ comparacaoResultado.comparison.time_difference.toFixed(2) }}s
                          </p>
                          <p class="text-text-secondary">Diferença de Tempo</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content (outros módulos) -->
      <div v-else class="flex-1 flex flex-col">
        <HeaderFilters 
          :title="getModuleTitle()"
          :tribos="tribos"
          :squads="filteredSquads"
          :years="availableYears"
          v-model:selectedTriboId="selectedTriboId"
          v-model:selectedSquadId="selectedSquadId"
          v-model:selectedYear="selectedYear"
          @triboChange="onTriboChange"
          @squadChange="applySquadFilter"
          @yearChange="applyYearFilter"
        />
        
        <!-- Content -->
        <div class="flex-1 overflow-hidden">
          <!-- Módulo Projetos -->
          <div v-if="activeModule === 'projetos'" class="h-full">
            <div v-if="!selectedSquadId" class="flex items-center justify-center h-full">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Selecione um Squad</h3>
                <p class="text-gray-500">Por favor, selecione um squad no seletor acima para gerenciar projetos</p>
              </div>
            </div>
            <div v-if="!selectedYear" class="flex items-center justify-center h-full">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Selecione o Ano do Roadmap</h3>
                <p class="text-gray-500">Por favor, selecione um ano no filtro acima para visualizar os projetos</p>
              </div>
            </div>
            <div v-else class="h-full overflow-y-auto p-4">
              <ProjetosCrud :selectedSquadId="selectedSquadId" :selectedYear="selectedYear" :allProjetos="allProjetos" @reload="carregarDados" />
            </div>
          </div>

          <!-- Módulo Colaboradores -->
          <div v-if="activeModule === 'colaboradores'" class="h-full">
            <div v-if="!selectedSquadId" class="flex items-center justify-center h-full">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">Selecione um Squad</h3>
                <p class="text-gray-500">Por favor, selecione um squad no seletor acima para gerenciar colaboradores</p>
              </div>
            </div>
            <div v-else class="h-full overflow-y-auto p-4">
              <ColaboradoresCrud 
                :key="selectedSquadId" 
                :selectedSquadId="selectedSquadId" 
                :allColaboradores="allColaboradores" 
                :selectedYear="selectedYear"
                :yearStartDate="getYearStartDate()"
                :yearEndDate="getYearEndDate()"
                @reload="carregarDados" 
              />
            </div>
          </div>

          <!-- Módulo Cargos & Habilidades -->
          <div v-if="activeModule === 'cargos-habilidades'" class="h-full overflow-y-auto p-4">
            <CargosHabilidadesCrud />
          </div>

          <!-- Módulo Tribos & Squads -->
          <div v-if="activeModule === 'tribos-squads'" class="h-full overflow-y-auto p-4">
            <TribosSquadsCrud />
          </div>

          <!-- Módulo Períodos Roadmaps -->
          <div v-if="activeModule === 'periodos-roadmaps'" class="h-full overflow-y-auto p-4">
            <PeriodosRoadmapsCrud />
          </div>

          <!-- Módulo Relatórios -->
          <div v-if="activeModule === 'relatorios'" class="h-full overflow-y-auto p-4">
            <div class="bg-white rounded-md shadow-sm p-6">
              <p class="text-text-secondary">Módulo de relatórios em desenvolvimento...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Skill Coverage Warning (Right Side) -->
    <div v-if="showSelectionModal && missingSkills.length > 0" class="fixed top-20 right-4 z-[60] max-w-sm w-full">
      <div class="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-4 shadow-xl">
        <div class="flex items-start gap-3">
          <svg class="w-6 h-6 text-yellow-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          <div class="flex-1">
            <p class="text-sm font-semibold text-yellow-900">Habilidades não cobertas</p>
            <p class="text-xs text-yellow-800 mt-1">Os projetos selecionados requerem habilidades que nenhum colaborador selecionado possui:</p>
            <div class="flex flex-wrap gap-1 mt-2">
              <span v-for="skill in missingSkills" :key="skill" class="inline-block px-2 py-1 bg-yellow-200 text-yellow-900 rounded text-xs font-medium">
                {{ skill }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de Seleção -->
    <div v-if="showSelectionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showSelectionModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-5xl w-full mx-4 max-h-[90vh] flex flex-col">
        <div class="px-6 py-3 border-b flex justify-between items-center">
          <h3 class="text-base font-semibold text-text-primary">Executar geração do Roadmap</h3>
          <button @click="showSelectionModal = false" class="text-text-secondary hover:text-text-primary">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4">
          
          <!-- Algorithm Parameters -->
          <div class="mb-3 bg-gray-50 rounded-md p-3 border border-gray-200">
            <div class="flex items-center gap-3">
              <h4 class="text-xs font-semibold text-gray-700">Parâmetros:</h4>
              <select v-model="params.algorithm" class="px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-primary-main">
                <option value="cp">Constraint Programming</option>
                <option value="ga">Algoritmo Genético</option>
                <option value="aco">Colônia de Formigas</option>
              </select>
              <div class="flex items-center gap-2 flex-1">
                <span class="text-xs text-gray-600 cursor-help" :title="params.algorithm === 'ga' ? 'Número de soluções candidatas em cada geração' : params.algorithm === 'aco' ? 'Número de formigas explorando soluções' : 'Não aplicável para CP'">População:</span>
                <input v-model.number="params.tam_pop" type="range" :min="10" :max="params.algorithm === 'ga' ? 100 : 50" class="form-slider flex-1" :disabled="params.algorithm === 'cp'" />
                <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.algorithm === 'cp' ? 'N/A' : params.tam_pop }}</span>
              </div>
              <div class="flex items-center gap-2 flex-1">
                <span class="text-xs text-gray-600 cursor-help" :title="params.algorithm === 'ga' ? 'Número de ciclos evolutivos do algoritmo' : params.algorithm === 'aco' ? 'Número de ciclos de busca do algoritmo' : 'Tempo limite em segundos'">{{ params.algorithm === 'cp' ? 'Tempo Limite:' : params.algorithm === 'ga' ? 'Gerações:' : 'Iterações:' }}</span>
                <input v-if="params.algorithm === 'cp'" v-model.number="params.time_limit_seconds" type="range" :min="30" :max="600" class="form-slider flex-1" />
                <input v-else v-model.number="params.n_gen" type="range" :min="5" :max="params.algorithm === 'ga' ? 1000 : 50" class="form-slider flex-1" />
                <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.algorithm === 'cp' ? params.time_limit_seconds + 's' : params.n_gen }}</span>
              </div>
              <button 
                @click="showAdvancedParams = !showAdvancedParams"
                class="text-xs text-gray-500 hover:text-gray-700 transition-colors"
                title="Parâmetros Avançados"
              >
                <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-90': showAdvancedParams }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
            
            <div v-if="showAdvancedParams" class="pt-2 border-t border-gray-300">
              <div v-if="params.algorithm === 'ga'" class="flex items-center gap-3">
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-gray-600 cursor-help" title="Probabilidade de combinar genes de dois indivíduos">Crossover:</span>
                  <input v-model.number="params.pc" type="range" min="0" max="1" step="0.1" class="form-slider flex-1" />
                  <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.pc }}</span>
                </div>
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-gray-600 cursor-help" title="Probabilidade de alterar genes aleatoriamente">Mutação:</span>
                  <input v-model.number="params.pm" type="range" min="0" max="1" step="0.1" class="form-slider flex-1" />
                  <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.pm }}</span>
                </div>
              </div>
              <div v-else-if="params.algorithm === 'aco'" class="flex items-center gap-3">
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-gray-600 cursor-help" title="Influência do feromônio na escolha do caminho">Alpha:</span>
                  <input v-model.number="params.alpha" type="range" min="0.1" max="3" step="0.1" class="form-slider flex-1" />
                  <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.alpha }}</span>
                </div>
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-gray-600 cursor-help" title="Influência da heurística (distância) na escolha">Beta:</span>
                  <input v-model.number="params.beta" type="range" min="0.1" max="5" step="0.1" class="form-slider flex-1" />
                  <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.beta }}</span>
                </div>
                <div class="flex items-center gap-2 flex-1">
                  <span class="text-xs text-gray-600 cursor-help" title="Taxa de evaporação do feromônio">Rho:</span>
                  <input v-model.number="params.rho" type="range" min="0.1" max="0.9" step="0.1" class="form-slider flex-1" />
                  <span class="text-xs font-medium text-gray-700 w-8 text-right">{{ params.rho }}</span>
                </div>
              </div>
              <div v-else-if="params.algorithm === 'cp'" class="space-y-3">
                <div class="flex items-center gap-3">
                  <div class="flex items-center gap-2 flex-1">
                    <span class="text-xs text-gray-600 cursor-help" title="Peso da duração total do projeto na função objetivo">Peso Makespan:</span>
                    <input v-model.number="params.makespan_weight" type="range" min="100" max="500" step="10" class="form-slider flex-1" />
                    <span class="text-xs font-medium text-gray-700 w-12 text-right">{{ params.makespan_weight }}</span>
                  </div>
                  <div class="flex items-center gap-2 flex-1">
                    <span class="text-xs text-gray-600 cursor-help" title="Peso do balanceamento de carga entre colaboradores">Balanceamento:</span>
                    <input v-model.number="params.load_balancing_weight" type="range" min="10" max="100" step="5" class="form-slider flex-1" />
                    <span class="text-xs font-medium text-gray-700 w-12 text-right">{{ params.load_balancing_weight }}</span>
                  </div>
                </div>
                <div class="text-xs text-gray-500">
                  <p><strong>CP Otimizado:</strong> Foca em reduzir tempo total e distribuir trabalho equilibradamente. Maior peso = maior prioridade na otimização.</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Projetos -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-text-primary">Projetos ({{ selectedProjects.length }}/{{ projetos.length }})</h4>
                <button @click="toggleAllProjects" class="text-xs text-primary-main hover:underline">
                  {{ selectedProjects.length === projetos.length ? 'Desmarcar' : 'Selecionar' }} todos
                </button>
              </div>
              <div class="space-y-1 max-h-[400px] overflow-y-auto border rounded p-2">
                <div 
                  v-for="projeto in sortedProjetos" 
                  :key="projeto.id" 
                  @click="toggleProject(projeto.id)"
                  class="flex items-center gap-2 cursor-pointer p-1.5 rounded transition-colors border"
                  :class="selectedProjects.includes(projeto.id) ? 'bg-blue-100 border-blue-300' : 'hover:bg-gray-50 border-transparent'"
                >
                  <div class="flex items-center justify-center w-7 h-7 rounded flex-shrink-0" :style="{ backgroundColor: projeto.color || '#3B82F6' }">
                    <svg v-if="selectedProjects.includes(projeto.id)" class="w-3.5 h-3.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0 flex items-center justify-between gap-2">
                    <div class="font-medium text-xs truncate">{{ projeto.nome }}</div>
                    <span 
                      v-if="getProjectSkills(projeto).length > 0"
                      :title="getProjectSkills(projeto).join(', ')"
                      class="flex-shrink-0 inline-flex items-center justify-center w-5 h-5 bg-blue-100 hover:bg-blue-200 transition-colors cursor-help"
                      style="border-radius: 6px;"
                    >
                      <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Colaboradores Squad -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-text-primary">Squad ({{ selectedCollaborators.length }}/{{ colaboradores.length }})</h4>
                <button @click="toggleAllCollaborators" class="text-xs text-primary-main hover:underline">
                  {{ selectedCollaborators.length === colaboradores.length ? 'Desmarcar' : 'Selecionar' }} todos
                </button>
              </div>
              <div class="space-y-1 max-h-[400px] overflow-y-auto border rounded p-2">
                <div 
                  v-for="colab in sortedColaboradores" 
                  :key="colab.id" 
                  @click="toggleCollaborator(colab.id)"
                  class="flex items-center gap-2 cursor-pointer p-1.5 rounded transition-colors border"
                  :class="[
                    selectedCollaborators.includes(colab.id) ? 'bg-green-100 border-green-300' : 'hover:bg-gray-50 border-transparent',
                    hasMissingSkill(colab) && !selectedCollaborators.includes(colab.id) ? 'ring-2 ring-yellow-400' : ''
                  ]"
                >
                  <div class="flex items-center justify-center w-7 h-7 rounded flex-shrink-0 bg-gray-200">
                    <svg v-if="selectedCollaborators.includes(colab.id)" class="w-3.5 h-3.5 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-xs truncate mb-1">
                      {{ colab.nome }} <span class="text-text-secondary font-normal">({{ colab.cargo?.nome || colab.cargo }})</span>
                    </div>
                    <div v-if="getCollaboratorSkills(colab).length > 0" class="flex flex-wrap gap-1">
                      <span v-for="skill in getCollaboratorSkills(colab)" :key="skill" class="inline-block px-1.5 py-0.5 bg-green-100 text-green-700 rounded text-xs">
                        {{ skill }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Transversais -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-purple-600">Transversais ({{ selectedTransversais.length }}/{{ transversais.length }})</h4>
                <button @click="toggleAllTransversais" class="text-xs text-purple-600 hover:underline">
                  {{ selectedTransversais.length === transversais.length ? 'Desmarcar' : 'Selecionar' }} todos
                </button>
              </div>
              <div class="space-y-1 max-h-[400px] overflow-y-auto border rounded p-2">
                <div 
                  v-for="colab in sortedTransversais" 
                  :key="colab.id" 
                  @click="toggleTransversal(colab.id)"
                  class="flex items-center gap-2 cursor-pointer p-1.5 rounded transition-colors border"
                  :class="[
                    selectedTransversais.includes(colab.id) ? 'bg-purple-100 border-purple-300' : 'hover:bg-gray-50 border-transparent',
                    hasMissingSkill(colab) && !selectedTransversais.includes(colab.id) ? 'ring-2 ring-yellow-400' : ''
                  ]"
                >
                  <div class="flex items-center justify-center w-7 h-7 rounded flex-shrink-0 bg-purple-200">
                    <svg v-if="selectedTransversais.includes(colab.id)" class="w-3.5 h-3.5 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-xs truncate mb-1">
                      {{ colab.nome }} <span class="text-text-secondary font-normal">({{ colab.cargo?.nome || colab.cargo }})</span>
                    </div>
                    <div v-if="getCollaboratorSkills(colab).length > 0" class="flex flex-wrap gap-1">
                      <span v-for="skill in getCollaboratorSkills(colab)" :key="skill" class="inline-block px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">
                        {{ skill }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Simular Membros -->
            <div class="flex flex-col">
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-text-primary">Simular Membros ({{ simulatedMembers.length }})</h4>
              </div>
              <div class="border rounded p-2 flex flex-col" style="height: 400px;">
                <div class="flex-1 overflow-y-auto mb-2">
                  <div v-if="simulatedMembers.length > 0" class="space-y-1">
                    <div v-for="member in simulatedMembers" :key="member.id" class="flex items-center gap-2 bg-purple-50 p-1.5 rounded border border-purple-200">
                      <div class="flex-1 min-w-0">
                        <div class="font-medium text-xs truncate mb-1">
                          {{ member.nome }} <span class="text-text-secondary font-normal">({{ member.cargo.nome }})</span>
                        </div>
                        <div class="flex flex-wrap gap-1 mb-1">
                          <span v-for="hab in member.habilidades" :key="hab.id" class="inline-block px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">
                            {{ hab.nome }}
                          </span>
                        </div>
                        <div class="text-xs text-gray-600">
                          {{ formatDate(member.inicio) }} - {{ formatDate(member.termino) }}
                        </div>
                      </div>
                      <button @click="removeSimulatedMember(member.id)" class="text-red-600 hover:text-red-800 flex-shrink-0">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div v-else class="text-xs text-text-secondary text-center py-4">
                    Nenhum membro simulado
                  </div>
                </div>
                <div class="space-y-2 border-t pt-2">
                  <select v-model="newMember.cargo_id" class="w-full px-2 py-1 border rounded text-xs">
                    <option :value="null">Cargo</option>
                    <option v-for="cargo in cargos" :key="cargo.id" :value="cargo.id">{{ cargo.nome }}</option>
                  </select>
                  <div class="w-full min-h-[32px] border rounded px-2 py-1 flex flex-wrap gap-1 items-center">
                    <span 
                      v-for="hab in filteredHabilidadesForCargo" 
                      :key="hab.id"
                      @click="toggleSkill(hab.nome)"
                      class="text-xs px-2 py-0.5 rounded cursor-pointer transition-colors"
                      :class="newMember.habilidade_names.includes(hab.nome) ? 'bg-purple-100 text-purple-700 font-medium' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                    >
                      {{ hab.nome }}
                    </span>
                    <span v-if="!newMember.cargo_id" class="text-xs text-gray-400">Selecione um cargo</span>
                    <span v-else-if="filteredHabilidadesForCargo.length === 0" class="text-xs text-gray-400">Sem habilidades</span>
                  </div>
                  <div class="grid grid-cols-2 gap-1">
                    <input v-model="newMember.inicio" type="date" class="px-2 py-1 border rounded text-xs" placeholder="Início">
                    <input v-model="newMember.termino" type="date" class="px-2 py-1 border rounded text-xs" placeholder="Término">
                  </div>
                  <button @click="addSimulatedMember" class="w-full px-2 py-1 bg-purple-600 text-white rounded text-xs hover:bg-purple-700">Adicionar</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-4 py-3 border-t flex justify-between items-center bg-gray-50">
          <div class="text-xs text-text-secondary">
            {{ selectedProjects.length }} projeto(s), {{ selectedCollaborators.length + selectedTransversais.length + simulatedMembers.length }} colaborador(es)
            <span v-if="selectedTransversais.length > 0" class="text-purple-600">(+{{ selectedTransversais.length }} transversais)</span>
            <span v-if="simulatedMembers.length > 0" class="text-purple-600">(+{{ simulatedMembers.length }} simulados)</span>
          </div>
          <div class="flex gap-2">
            <button 
              @click="showSelectionModal = false" 
              class="px-3 py-1.5 text-xs border border-gray-300 rounded hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button 
              @click="executarAlgoritmo" 
              :disabled="selectedProjects.length === 0 || (selectedCollaborators.length === 0 && selectedTransversais.length === 0 && simulatedMembers.length === 0)"
              class="px-3 py-1.5 text-xs bg-primary-main text-white rounded hover:bg-primary-light disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Executar
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal Salvar Resultado -->
    <div v-if="showSaveModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showSaveModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">Salvar Resultado</h3>
        </div>
        <div class="p-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">Nome do Resultado</label>
          <input 
            v-model="saveResultName" 
            type="text" 
            placeholder="Ex: Roadmap Q1 2025" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-main"
            @keyup.enter="salvarResultado"
          />
        </div>
        <div class="px-6 py-4 border-t flex justify-end gap-2">
          <button 
            @click="showSaveModal = false" 
            class="px-4 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-100"
          >
            Cancelar
          </button>
          <button 
            @click="salvarResultado" 
            :disabled="!saveResultName.trim()"
            class="px-4 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Carregar Resultado -->
    <div v-if="showLoadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showLoadModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[85vh] flex flex-col">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h3 class="text-lg font-semibold">Resultados Salvos ({{ resultadosSalvos.length }})</h3>
          <button @click="showLoadModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div v-if="resultadosSalvos.length === 0" class="text-center py-8 text-gray-500">
            <svg class="w-16 h-16 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>Nenhum resultado salvo ainda</p>
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="resultado in resultadosSalvos" 
              :key="resultado.id" 
              @click="carregarResultado(resultado.id)"
              class="bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-200 rounded-lg p-4 hover:shadow-lg hover:border-purple-300 transition-all cursor-pointer group relative"
            >
              <button 
                @click.stop="confirmarDeletarResultado(resultado.id)" 
                class="absolute top-2 right-2 p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors opacity-0 group-hover:opacity-100"
                title="Deletar"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
              <div class="flex items-start justify-between mb-3 pr-6">
                <h5 class="font-semibold text-gray-900 text-sm group-hover:text-purple-600 transition-colors line-clamp-2 flex-1">{{ resultado.nome }}</h5>
                <span class="text-xs px-2 py-1 rounded-full font-bold flex-shrink-0 ml-2" :class="resultado.algoritmo === 'ga' ? 'bg-blue-500 text-white' : 'bg-green-500 text-white'">{{ resultado.algoritmo.toUpperCase() }}</span>
              </div>
              <div class="space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-gray-600">Fitness</span>
                  <span class="font-bold text-gray-900">{{ resultado.melhor_fitness.toFixed(2) }}</span>
                </div>
                <div v-if="resultado.parametros?.projeto_ids" class="flex items-center justify-between text-xs">
                  <span class="text-gray-600">Projetos</span>
                  <span class="font-bold text-gray-900">{{ resultado.parametros.projeto_ids.length }}</span>
                </div>
                <div v-if="getRoadmapEndDate(resultado)" class="flex items-center justify-between text-xs">
                  <span class="text-gray-600">Término</span>
                  <span class="font-bold text-gray-900">{{ getRoadmapEndDate(resultado) }}</span>
                </div>
                <div class="pt-2 border-t border-gray-300">
                  <p class="text-xs text-gray-500">{{ new Date(resultado.data_execucao).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Comparison Modal -->
    <div v-if="showComparisonModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showComparisonModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full mx-4">
        <div class="px-6 py-3 border-b flex justify-between items-center">
          <h3 class="text-base font-semibold text-text-primary">Comparar Algoritmos (GA vs ACO)</h3>
          <button @click="showComparisonModal = false" class="text-text-secondary hover:text-text-primary">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-2 gap-6">
            <!-- GA Parameters -->
            <div class="bg-blue-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-blue-900 mb-4">Algoritmo Genético (GA)</h4>
              <div class="space-y-4">
                <ParamSlider label="População" :value="gaParams.tam_pop" :min="10" :max="100" @update="gaParams.tam_pop = $event" />
                <ParamSlider label="Gerações" :value="gaParams.n_gen" :min="5" :max="1000" @update="gaParams.n_gen = $event" />
                <ParamSlider label="Crossover" :value="gaParams.pc" :min="0" :max="1" :step="0.1" @update="gaParams.pc = $event" />
                <ParamSlider label="Mutação" :value="gaParams.pm" :min="0" :max="1" :step="0.1" @update="gaParams.pm = $event" />
              </div>
            </div>
            
            <!-- ACO Parameters -->
            <div class="bg-green-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-green-900 mb-4">Colônia de Formigas (ACO)</h4>
              <div class="space-y-4">
                <ParamSlider label="Formigas" :value="acoParams.tam_pop" :min="10" :max="50" @update="acoParams.tam_pop = $event" />
                <ParamSlider label="Iterações" :value="acoParams.n_gen" :min="5" :max="50" @update="acoParams.n_gen = $event" />
                <ParamSlider label="Alpha (Feromônio)" :value="acoParams.alpha" :min="0.1" :max="3" :step="0.1" @update="acoParams.alpha = $event" />
                <ParamSlider label="Beta (Heurística)" :value="acoParams.beta" :min="0.1" :max="5" :step="0.1" @update="acoParams.beta = $event" />
                <ParamSlider label="Rho (Evaporação)" :value="acoParams.rho" :min="0.1" :max="0.9" :step="0.1" @update="acoParams.rho = $event" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-6 py-3 border-t flex justify-end gap-2 bg-gray-50">
          <button 
            @click="showComparisonModal = false" 
            class="px-4 py-2 text-sm border border-gray-300 rounded hover:bg-gray-100"
          >
            Cancelar
          </button>
          <button 
            @click="compararAlgoritmos" 
            class="px-4 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700"
          >
            Executar Comparação
          </button>
        </div>
      </div>
    </div>
    
    <!-- Confirm Delete Modal -->
    <ConfirmModal
      :show="showConfirmDelete"
      title="Confirmar exclusão"
      message="Tem certeza que deseja excluir este resultado salvo? Esta ação não pode ser desfeita."
      @confirm="deletarResultado"
      @cancel="cancelarDeletarResultado"
    />
    
    <!-- Colaboradores Modal -->
    <div v-if="showColaboradoresModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showColaboradoresModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-5xl w-full mx-4 max-h-[85vh] flex flex-col">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h3 class="text-lg font-semibold">Colaboradores ({{ colaboradores.length }})</h3>
          <button @click="showColaboradoresModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div v-for="colab in colaboradores" :key="colab.id" class="bg-gray-50 border rounded-lg p-3">
              <h4 class="font-semibold text-gray-900 text-sm mb-1">{{ colab.nome }}</h4>
              <div class="text-xs text-gray-600 space-y-0.5">
                <p>{{ colab.cargo?.nome || colab.cargo }}<span v-if="colab.squad"> • {{ colab.squad.nome }}</span></p>
                <div v-if="colab.habilidades?.length" class="flex flex-wrap gap-0.5 mt-1">
                  <span v-for="hab in colab.habilidades" :key="hab.id" class="px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">
                    {{ hab.nome || hab }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Projetos Modal -->
    <div v-if="showProjetosModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showProjetosModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[85vh] flex flex-col">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h3 class="text-lg font-semibold">Projetos ({{ projetos.length }})</h3>
          <button @click="showProjetosModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-2">
            <div v-for="projeto in projetos" :key="projeto.id" class="border rounded-lg overflow-hidden">
              <div 
                @click="expandedProjects[projeto.id] = !expandedProjects[projeto.id]"
                class="flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2 flex-1">
                  <div class="w-3 h-3 rounded flex-shrink-0" :style="{ backgroundColor: projeto.color || '#3B82F6' }"></div>
                  <h4 class="font-semibold text-gray-900 text-sm">{{ projeto.nome }}</h4>
                  <span class="text-xs text-gray-500">({{ projeto.etapas?.length || 0 }} etapas)</span>
                </div>
                <div class="flex items-center gap-2">
                  <span v-if="projeto.termino" class="text-xs text-gray-600">
                    {{ new Date(projeto.termino).toLocaleDateString('pt-BR') }}
                  </span>
                  <svg 
                    class="w-5 h-5 text-gray-500 transition-transform"
                    :class="{ 'rotate-180': expandedProjects[projeto.id] }"
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
              <div v-if="expandedProjects[projeto.id] && projeto.etapas?.length" class="p-3 bg-white border-t">
                <div class="space-y-2">
                  <div v-for="etapa in projeto.etapas" :key="etapa.id" class="bg-gray-50 border rounded p-2">
                    <div class="font-medium text-gray-800 text-sm mb-1">{{ etapa.nome }}</div>
                    <div class="text-xs text-gray-600 mb-1">
                      <span class="font-medium">Duração:</span> {{ etapa.duracao_dias }} dias • 
                      <span class="font-medium">Cargo:</span> {{ etapa.cargo_necessario?.nome || etapa.cargo_necessario || 'N/A' }}
                    </div>
                    <div v-if="etapa.habilidades_necessarias?.length" class="flex flex-wrap gap-1">
                      <span v-for="hab in etapa.habilidades_necessarias" :key="hab.id" class="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">
                        {{ hab.nome || hab }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Cargos Modal -->
    <div v-if="showCargosModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showCargosModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[85vh] flex flex-col">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h3 class="text-lg font-semibold">Cargos ({{ cargos.length }})</h3>
          <button @click="showCargosModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div v-for="cargo in cargos" :key="cargo.id" class="bg-purple-50 border border-purple-200 rounded-lg p-3">
              <h4 class="font-semibold text-purple-900">{{ cargo.nome }}</h4>
              <div v-if="habilidades.filter(h => h.cargo_id === cargo.id).length" class="mt-2">
                <p class="text-xs font-medium text-purple-700 mb-1">Habilidades associadas:</p>
                <div class="flex flex-wrap gap-1">
                  <span v-for="hab in habilidades.filter(h => h.cargo_id === cargo.id)" :key="hab.id" class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">
                    {{ hab.nome }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Habilidades Modal -->
    <div v-if="showHabilidadesModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showHabilidadesModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full mx-4 max-h-[85vh] flex flex-col">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h3 class="text-lg font-semibold">Habilidades ({{ habilidades.length }})</h3>
          <button @click="showHabilidadesModal = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div v-for="hab in habilidades" :key="hab.id" class="bg-orange-50 border border-orange-200 rounded-lg p-3">
              <h4 class="font-semibold text-orange-900 mb-1">{{ hab.nome }}</h4>
              <p class="text-xs text-orange-700">
                <span class="font-medium">Cargo:</span> {{ cargos.find(c => c.id === hab.cargo_id)?.nome || 'N/A' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <ProgressBar 
      :show="showProgress"
      :title="params.algorithm === 'ga' ? 'Executando Algoritmo Genético' : params.algorithm === 'aco' ? 'Executando Colônia de Formigas' : 'Executando Constraint Programming'"
      :current="progressData.current"
      :total="progressData.total"
      :percent="progressData.percent"
      :fitness="progressData.fitness"
      :loading="progressLoading"
    />
  </div>
</template>

<script>
import axios from 'axios'
import { CpuChipIcon, FolderIcon, UserGroupIcon, BriefcaseIcon, AcademicCapIcon } from '@heroicons/vue/24/outline'
import DadosTab from './components/tabs/DadosTab.vue'
import FitnessTab from './components/tabs/FitnessTab.vue'
import ConflitosTab from './components/tabs/ConflitosTab.vue'
import GanttTab from './components/tabs/GanttTab.vue'
import CalendarioTab from './components/tabs/CalendarioTab.vue'
import MapaAlocacaoTab from './components/tabs/MapaAlocacaoTab.vue'
import ProjetosCrud from './components/crud/ProjetosCrud.vue'
import ColaboradoresCrud from './components/crud/ColaboradoresCrud.vue'
import CargosHabilidadesCrud from './components/crud/CargosHabilidadesCrud.vue'
import TribosSquadsCrud from './components/crud/TribosSquadsCrud.vue'
import PeriodosRoadmapsCrud from './components/crud/PeriodosRoadmapsCrud.vue'
import ConfirmModal from './components/modals/ConfirmModal.vue'
import SelectionModal from './components/modals/SelectionModal.vue'
import SaveResultModal from './components/modals/SaveResultModal.vue'
import LoadResultModal from './components/modals/LoadResultModal.vue'
import SquadSelector from './components/common/SquadSelector.vue'
import ProgressBar from './components/common/ProgressBar.vue'
import Sidebar from './components/layout/Sidebar.vue'
import HeaderFilters from './components/layout/HeaderFilters.vue'
import EmptyState from './components/common/EmptyState.vue'
import ParamSlider from './components/roadmap/ParamSlider.vue'
import { useRoadmap } from './composables/useRoadmap'

export default {
  name: 'App',
  components: {
    DadosTab,
    FitnessTab,
    ConflitosTab,
    GanttTab,
    CalendarioTab,
    MapaAlocacaoTab,
    ProjetosCrud,
    ColaboradoresCrud,
    CargosHabilidadesCrud,
    TribosSquadsCrud,
    PeriodosRoadmapsCrud,
    ConfirmModal,
    SelectionModal,
    SaveResultModal,
    LoadResultModal,
    SquadSelector,
    ProgressBar,
    Sidebar,
    HeaderFilters,
    EmptyState,
    ParamSlider,
    CpuChipIcon,
    FolderIcon,
    UserGroupIcon,
    BriefcaseIcon,
    AcademicCapIcon
  },
  data() {
    return {
      activeModule: 'roadmap',
      showSelectionModal: false,
      showSaveModal: false,
      showLoadModal: false,
      showConfirmDelete: false,
      showColaboradoresModal: false,
      showProjetosModal: false,
      showCargosModal: false,
      showHabilidadesModal: false,
      showComparisonModal: false,
      showAdvancedParams: false,
      expandedProjects: {},
      resultadoToDelete: null,
      saveResultName: '',
      resultadosSalvos: [],
      selectedProjects: [],
      selectedCollaborators: [],
      selectedTransversais: [],
      simulatedMembers: [],
      executedColaboradores: [],
      newMember: { cargo_id: null, habilidade_names: [], inicio: '', termino: '' },
      cargos: [],
      habilidades: [],
      params: {
        algorithm: 'ga',
        tam_pop: 50,
        n_gen: 300,
        pc: 0.7,
        pm: 0.3,
        alpha: 1.0,
        beta: 2.0,
        rho: 0.5,
        time_limit_seconds: 600,  // Increased for CP
        makespan_weight: 200,     // Increased focus on makespan
        load_balancing_weight: 50, // New parameter for load balancing
        ref_date: '2025-01-01'
      },
      gaParams: {
        tam_pop: 50,
        n_gen: 500,
        pc: 0.8,
        pm: 0.2
      },
      acoParams: {
        tam_pop: 50,
        n_gen: 15,
        alpha: 1.0,
        beta: 2.0,
        rho: 0.5
      },
      showComparisonParams: false,
      loading: false,
      activeTab: 'dados',
      resultado: null,
      colaboradores: [],
      allColaboradores: [],
      projetos: [],
      allProjetos: [],
      tribos: [],
      squads: [],
      periodosRoadmaps: [],
      selectedTriboId: null,
      selectedSquadId: null,
      selectedYear: null,
      menuSections: [
        {
          title: 'Squad',
          items: [
            { id: 'roadmap', label: 'Gerador de Roadmap', icon: 'CpuChipIcon' },
            { id: 'projetos', label: 'Projetos', icon: 'FolderIcon' },
            { id: 'colaboradores', label: 'Colaboradores', icon: 'UserGroupIcon' }
          ]
        },
        {
          title: 'Geral',
          items: [
            { id: 'tribos-squads', label: 'Tribos e Squads', icon: 'UserGroupIcon' },
            { id: 'cargos-habilidades', label: 'Cargos e Habilidades', icon: 'BriefcaseIcon' },
            { id: 'periodos-roadmaps', label: 'Períodos de Roadmaps', icon: 'AcademicCapIcon' }
          ]
        }
      ],
      tabs: [
        { name: 'dados', label: 'Dados' },
        { name: 'fitness', label: 'Fitness' },
        { name: 'conflitos', label: 'Conflitos' },
        { name: 'gantt', label: 'Gantt' },
        { name: 'calendario', label: 'Calendário' },
        { name: 'mapa', label: 'Mapa de Alocação' },
        { name: 'comparacao', label: 'Comparação' }
      ],
      comparacaoResultado: null,
      showProgress: false,
      progressData: { current: 0, total: 100, percent: 0, fitness: 0 },
      progressLoading: false
    }
  },
  computed: {
    filteredSquads() {
      if (!this.selectedTriboId) return this.squads
      return this.squads.filter(s => s.tribo_id === this.selectedTriboId)
    },
    availableYears() {
      return this.periodosRoadmaps.map(p => p.ano).sort((a, b) => b - a)
    },
    allColaboradoresWithSimulated() {
      if (this.executedColaboradores.length > 0) {
        return [...this.executedColaboradores, ...this.simulatedMembers]
      }
      const selectedSquadMembers = this.colaboradores.filter(c => this.selectedCollaborators.includes(c.id))
      const selectedTransversalMembers = this.transversais.filter(c => this.selectedTransversais.includes(c.id))
      return [...selectedSquadMembers, ...selectedTransversalMembers, ...this.simulatedMembers]
    },
    filteredHabilidadesForCargo() {
      if (!this.newMember.cargo_id) return []
      return this.habilidades.filter(h => h.cargo_id == this.newMember.cargo_id)
    },
    transversais() {
      return this.allColaboradores.filter(c => c.transversal)
    },
    sortedProjetos() {
      return [...this.projetos].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    sortedColaboradores() {
      return [...this.colaboradores].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    sortedTransversais() {
      return [...this.transversais].sort((a, b) => a.nome.localeCompare(b.nome))
    },
    missingSkills() {
      const requiredSkills = new Set()
      const availableSkills = new Set()
      
      // Get required skills from selected projects
      this.projetos
        .filter(p => this.selectedProjects.includes(p.id))
        .forEach(proj => {
          proj.etapas?.forEach(etapa => {
            etapa.habilidades_necessarias?.forEach(hab => {
              const skillName = hab.nome || hab
              requiredSkills.add(skillName)
            })
          })
        })
      
      // Get available skills from selected squad collaborators
      this.colaboradores
        .filter(c => this.selectedCollaborators.includes(c.id))
        .forEach(colab => {
          colab.habilidades?.forEach(hab => {
            const skillName = hab.nome || hab
            availableSkills.add(skillName)
          })
        })
      
      // Get available skills from selected transversal collaborators
      this.transversais
        .filter(c => this.selectedTransversais.includes(c.id))
        .forEach(colab => {
          colab.habilidades?.forEach(hab => {
            const skillName = hab.nome || hab
            availableSkills.add(skillName)
          })
        })
      
      // Find missing skills
      const missing = []
      requiredSkills.forEach(skill => {
        if (!availableSkills.has(skill)) {
          missing.push(skill)
        }
      })
      
      return missing.sort()
    }
  },
  async mounted() {
    await this.carregarDados()
    await this.carregarCargosHabilidades()
    await this.carregarResultadosSalvos()
    this.initializeSelections()
  },
  watch: {
    colaboradores() {
      this.initializeSelections()
    },
    projetos() {
      this.initializeSelections()
    },
    selectedYear() {
      // Update default dates for new member form when year changes
      if (!this.newMember.inicio && !this.newMember.termino) {
        this.newMember.inicio = this.getYearStartDate()
        this.newMember.termino = this.getYearEndDate()
      }
    },
    showSelectionModal(newVal) {
      // Set default dates when modal opens
      if (newVal && !this.newMember.inicio && !this.newMember.termino) {
        this.newMember.inicio = this.getYearStartDate()
        this.newMember.termino = this.getYearEndDate()
      }
    }
  },

  methods: {
    initializeSelections() {
      if (this.colaboradores.length > 0 && this.selectedCollaborators.length === 0) {
        this.selectedCollaborators = this.colaboradores.map(c => c.id)
      }
      if (this.projetos.length > 0 && this.selectedProjects.length === 0) {
        this.selectedProjects = this.projetos.map(p => p.id)
      }
      // Transversais are NOT selected by default
      this.selectedTransversais = []
    },
    toggleProject(id) {
      const index = this.selectedProjects.indexOf(id)
      if (index > -1) {
        this.selectedProjects.splice(index, 1)
      } else {
        this.selectedProjects.push(id)
      }
    },
    toggleCollaborator(id) {
      const index = this.selectedCollaborators.indexOf(id)
      if (index > -1) {
        this.selectedCollaborators.splice(index, 1)
      } else {
        this.selectedCollaborators.push(id)
      }
    },
    toggleAllProjects() {
      if (this.selectedProjects.length === this.projetos.length) {
        this.selectedProjects = []
      } else {
        this.selectedProjects = this.projetos.map(p => p.id)
      }
    },
    toggleAllCollaborators() {
      if (this.selectedCollaborators.length === this.colaboradores.length) {
        this.selectedCollaborators = []
      } else {
        this.selectedCollaborators = this.colaboradores.map(c => c.id)
      }
    },
    toggleTransversal(id) {
      const index = this.selectedTransversais.indexOf(id)
      if (index > -1) {
        this.selectedTransversais.splice(index, 1)
      } else {
        this.selectedTransversais.push(id)
      }
    },
    toggleAllTransversais() {
      if (this.selectedTransversais.length === this.transversais.length) {
        this.selectedTransversais = []
      } else {
        this.selectedTransversais = this.transversais.map(c => c.id)
      }
    },
    async carregarDados() {
      try {
        console.log('Carregando dados...')
        const [colabRes, projRes, tribosRes, squadsRes, periodosRes] = await Promise.all([
          axios.get('/api/colaboradores'),
          axios.get('/api/projetos'),
          axios.get('/api/tribos'),
          axios.get('/api/squads'),
          axios.get('/api/periodos-roadmaps')
        ])
        console.log('Colaboradores:', colabRes.data)
        console.log('Projetos:', projRes.data)
        this.allColaboradores = colabRes.data
        this.allProjetos = projRes.data
        this.tribos = tribosRes.data
        this.squads = squadsRes.data
        this.periodosRoadmaps = periodosRes.data
        this.loadSavedFilters()
        console.log(`Carregados ${this.allColaboradores.length} colaboradores e ${this.allProjetos.length} projetos`)
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        console.error('Erro ao carregar dados:', error.message)
      }
    },
    applySquadFilter() {
      this.selectedYear = null
      localStorage.removeItem('selectedYear')
      if (this.selectedSquadId) {
        localStorage.setItem('selectedSquadId', this.selectedSquadId.toString())
      } else {
        localStorage.removeItem('selectedSquadId')
      }
      this.applyFilters()
    },
    applyYearFilter() {
      if (this.selectedYear) {
        localStorage.setItem('selectedYear', this.selectedYear.toString())
      } else {
        localStorage.removeItem('selectedYear')
      }
      this.applyFilters()
    },
    applyFilters() {
      let filteredColaboradores = this.allColaboradores
      let filteredProjetos = []
      
      if (this.selectedSquadId) {
        filteredColaboradores = filteredColaboradores.filter(c => c.squad?.id === this.selectedSquadId && !c.transversal)
        filteredProjetos = this.allProjetos.filter(p => p.squad?.id === this.selectedSquadId)
        localStorage.setItem('selectedSquadId', this.selectedSquadId.toString())
      } else {
        filteredColaboradores = filteredColaboradores.filter(c => !c.transversal)
        filteredProjetos = this.allProjetos
        localStorage.removeItem('selectedSquadId')
      }
      
      if (this.selectedYear !== null) {
        filteredProjetos = filteredProjetos.filter(p => p.ano === this.selectedYear)
      } else {
        filteredProjetos = []
      }
      
      this.colaboradores = filteredColaboradores
      this.projetos = filteredProjetos
      this.resultado = null
      this.comparacaoResultado = null
      this.initializeSelections()
      this.carregarResultadosSalvos()
    },
    onTriboChange() {
      this.selectedSquadId = null
      this.selectedYear = null
      localStorage.setItem('selectedTriboId', this.selectedTriboId?.toString() || '')
      localStorage.removeItem('selectedSquadId')
      localStorage.removeItem('selectedYear')
      this.applyFilters()
    },
    loadSavedFilters() {
      const savedTriboId = localStorage.getItem('selectedTriboId')
      const savedSquadId = localStorage.getItem('selectedSquadId')
      const savedYear = localStorage.getItem('selectedYear')
      
      if (savedTriboId && this.tribos.length > 0) {
        const triboId = parseInt(savedTriboId)
        if (this.tribos.some(t => t.id === triboId)) {
          this.selectedTriboId = triboId
        }
      }
      
      if (savedSquadId && this.squads.length > 0) {
        const squadId = parseInt(savedSquadId)
        if (this.squads.some(s => s.id === squadId)) {
          this.selectedSquadId = squadId
          
          if (savedYear) {
            const year = parseInt(savedYear)
            if (this.periodosRoadmaps.some(p => p.ano === year)) {
              this.selectedYear = year
            }
          }
        }
      }
      
      this.applyFilters()
    },
    async carregarCargosHabilidades() {
      try {
        const [cargosRes, habilidadesRes] = await Promise.all([
          axios.get('/api/cargos'),
          axios.get('/api/habilidades')
        ])
        this.cargos = cargosRes.data
        this.habilidades = habilidadesRes.data
      } catch (error) {
        console.error('Erro ao carregar cargos e habilidades:', error)
      }
    },
    addSimulatedMember() {
      if (!this.newMember.cargo_id || this.newMember.habilidade_names.length === 0) return
      
      const cargo = this.cargos.find(c => c.id === this.newMember.cargo_id)
      const habilidades = this.habilidades.filter(h => this.newMember.habilidade_names.includes(h.nome))
      const cargoSimCount = this.simulatedMembers.filter(m => m.cargo.id === cargo.id).length + 1
      
      // Use provided dates or default to year period
      const inicio = this.newMember.inicio || this.getYearStartDate()
      const termino = this.newMember.termino || this.getYearEndDate()
      
      this.simulatedMembers.push({
        id: `sim_${Date.now()}`,
        nome: `${cargo.nome} Simulado ${cargoSimCount}`,
        cargo: cargo,
        habilidades: habilidades,
        inicio: inicio,
        termino: termino,
        simulated: true
      })
      
      // Reset form but keep default dates
      const defaultInicio = this.getYearStartDate()
      const defaultTermino = this.getYearEndDate()
      this.newMember = { cargo_id: null, habilidade_names: [], inicio: defaultInicio, termino: defaultTermino }
    },
    removeSimulatedMember(id) {
      const index = this.simulatedMembers.findIndex(m => m.id === id)
      if (index > -1) {
        this.simulatedMembers.splice(index, 1)
      }
    },
    toggleSkill(skillName) {
      const index = this.newMember.habilidade_names.indexOf(skillName)
      if (index > -1) {
        this.newMember.habilidade_names.splice(index, 1)
      } else {
        this.newMember.habilidade_names.push(skillName)
      }
    },
    executarAlgoritmoDirectly() {
      this.selectedProjects = this.projetos.map(p => p.id)
      this.selectedCollaborators = this.colaboradores.map(c => c.id)
      this.selectedTransversais = []
      this.simulatedMembers = []
      this.executarAlgoritmo()
    },
    async executarAlgoritmo() {
      this.showSelectionModal = false
      this.loading = true
      this.showProgress = true
      this.progressData = { current: 0, total: 1, percent: 0, fitness: 0 }
      
      // Capture selected members BEFORE any data operations
      const selectedSquadMembers = this.colaboradores.filter(c => this.selectedCollaborators.includes(c.id))
      const selectedTransversalMembers = this.allColaboradores.filter(c => this.selectedTransversais.includes(c.id))
      
      try {
        const colaborador_ids = [...selectedSquadMembers.map(c => c.id), ...selectedTransversalMembers.map(c => c.id)]
        const payload = {
          ...this.params,
          ref_date: this.getYearStartDate() || this.params.ref_date,
          projeto_ids: this.selectedProjects,
          colaborador_ids: colaborador_ids,
          simulated_members: this.simulatedMembers.map(m => ({
            nome: m.nome,
            cargo_id: m.cargo.id,
            habilidade_names: m.habilidades.map(h => h.nome),
            inicio: m.inicio || null,
            termino: m.termino || null
          }))
        }
        
        console.log('Payload:', JSON.stringify(payload, null, 2))
        
        // Use streaming endpoint for GA, ACO, and CP
        let streamEndpoint, regularEndpoint
        if (this.params.algorithm === 'ga') {
          streamEndpoint = '/api/executar-algoritmo-stream'
          regularEndpoint = '/api/executar-algoritmo'
        } else if (this.params.algorithm === 'aco') {
          streamEndpoint = '/api/executar-aco-stream'
          regularEndpoint = '/api/executar-aco'
        } else if (this.params.algorithm === 'cp') {
          streamEndpoint = '/api/executar-cp-stream'
          regularEndpoint = '/api/executar-cp'
        }
        
        const response = await fetch(streamEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''
        
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = JSON.parse(line.slice(6))
              
              if (data.error) {
                console.error('Erro no stream:', data.error)
                alert('Erro ao executar algoritmo: ' + data.error)
                this.showProgress = false
                this.loading = false
                return
              }
              
              if (data.type === 'progress') {
                this.progressData.current = data.generation
                this.progressData.total = data.total_generations
                this.progressData.fitness = data.best_fitness
              } else if (data.type === 'complete') {
                // Show loading state
                this.progressLoading = true
                // Get full result from regular endpoint
                const finalResponse = await axios.post(regularEndpoint, payload)
                this.resultado = finalResponse.data
                // Store executed collaborators for display (use captured members from before reload)
                this.executedColaboradores = [...selectedSquadMembers, ...selectedTransversalMembers]
                this.showProgress = false
                this.progressLoading = false
                this.loading = false
                this.activeTab = 'gantt'
                console.log(`${this.params.algorithm.toUpperCase()} executado com sucesso!`)
                return
              }
            }
          }
        }
      } catch (error) {
        console.error('Erro ao executar algoritmo:', error)
        alert('Erro ao executar algoritmo: ' + error.message)
        this.showProgress = false
        this.loading = false
      }
    },
    async compararAlgoritmos() {
      this.showComparisonModal = false
      this.loading = true
      try {
        const comparisonParams = {
          ref_date: this.getYearStartDate() || this.params.ref_date,
          ga_params: this.gaParams,
          aco_params: this.acoParams
        }
        const response = await axios.post('/api/comparar-algoritmos', comparisonParams)
        this.comparacaoResultado = response.data
        this.activeTab = 'comparacao'
        console.log('Comparação executada com sucesso!')
      } catch (error) {
        console.error('Erro ao comparar algoritmos')
      } finally {
        this.loading = false
      }
    },
    getProjectSkills(projeto) {
      const skills = new Set()
      projeto.etapas?.forEach(etapa => {
        etapa.habilidades_necessarias?.forEach(hab => {
          const skillName = hab.nome || hab
          skills.add(skillName)
        })
      })
      return Array.from(skills).sort()
    },
    getCollaboratorSkills(colab) {
      const skills = colab.habilidades?.map(hab => hab.nome || hab) || []
      return skills.sort()
    },
    hasMissingSkill(colab) {
      const colabSkills = new Set(colab.habilidades?.map(h => h.nome || h) || [])
      return this.missingSkills.some(skill => colabSkills.has(skill))
    },
    async carregarResultadosSalvos() {
      try {
        const params = {}
        if (this.selectedSquadId) params.squad_id = this.selectedSquadId
        if (this.selectedYear) params.ano = this.selectedYear
        const response = await axios.get('/api/resultados-salvos', { params })
        this.resultadosSalvos = response.data
      } catch (error) {
        console.error('Erro ao carregar resultados salvos:', error)
      }
    },
    async salvarResultado() {
      if (!this.saveResultName.trim()) return
      try {
        // Get end date from tasks
        let roadmapEndDate = null
        if (this.resultado?.tarefas?.length) {
          const tarefaFinal = this.resultado.tarefas.reduce((latest, t) => 
            t.fim_dias > latest.fim_dias ? t : latest, this.resultado.tarefas[0])
          if (tarefaFinal?.data_fim) {
            const [dia, mes, ano] = tarefaFinal.data_fim.split('/')
            roadmapEndDate = `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
          }
        }
        
        const paramsToSave = {
          ...this.params,
          roadmap_end_date: roadmapEndDate,
          saved_colaboradores: this.executedColaboradores,
          simulated_members: this.simulatedMembers.map(m => ({
            nome: m.nome,
            cargo_id: m.cargo.id,
            cargo: m.cargo,
            habilidade_names: m.habilidades.map(h => h.nome),
            habilidades: m.habilidades,
            inicio: m.inicio,
            termino: m.termino
          }))
        }
        
        await axios.post('/api/resultados-salvos', {
          nome: this.saveResultName,
          algoritmo: this.params.algorithm,
          melhor_fitness: this.resultado.melhor_fitness,
          roadmap_end_date: roadmapEndDate,
          squad_id: this.selectedSquadId,
          ano: this.selectedYear,
          tarefas: this.resultado.tarefas,
          historico_fitness: this.resultado.historico_fitness,
          penalidades: this.resultado.penalidades,
          ocorrencias_penalidades: this.resultado.ocorrencias_penalidades,
          parametros: paramsToSave
        })
        this.showSaveModal = false
        this.saveResultName = ''
        await this.carregarResultadosSalvos()
        console.log('Resultado salvo com sucesso!')
      } catch (error) {
        console.error('Erro ao salvar resultado:', error)
      }
    },
    async carregarResultado(id) {
      try {
        const response = await axios.get(`/api/resultados-salvos/${id}`)
        const saved = response.data
        this.resultado = {
          tarefas: saved.tarefas,
          melhor_fitness: saved.melhor_fitness,
          historico_fitness: saved.historico_fitness,
          penalidades: saved.penalidades,
          ocorrencias_penalidades: saved.ocorrencias_penalidades
        }
        this.params = { ...this.params, ...saved.parametros }
        
        // Restore saved collaborators (including deleted ones)
        if (saved.parametros.saved_colaboradores) {
          this.executedColaboradores = saved.parametros.saved_colaboradores
          console.log('Loaded executedColaboradores:', this.executedColaboradores.length)
        }
        
        // Ensure projetos are loaded for the saved result
        if (saved.parametros.projeto_ids && saved.parametros.projeto_ids.length > 0) {
          const projectIds = saved.parametros.projeto_ids
          this.projetos = this.allProjetos.filter(p => projectIds.includes(p.id))
        }
        
        // Restore simulated members if they exist
        if (saved.parametros.simulated_members && saved.parametros.simulated_members.length > 0) {
          this.simulatedMembers = saved.parametros.simulated_members.map((m, idx) => ({
            id: `sim_${Date.now()}_${idx}`,
            nome: m.nome,
            cargo: m.cargo || this.cargos.find(c => c.id === m.cargo_id),
            habilidades: m.habilidades || this.habilidades.filter(h => m.habilidade_names.includes(h.nome)),
            inicio: m.inicio,
            termino: m.termino,
            simulated: true
          }))
        } else {
          this.simulatedMembers = []
        }
        
        this.showLoadModal = false
        this.activeTab = 'gantt'
        console.log('Resultado carregado com sucesso!')
      } catch (error) {
        console.error('Erro ao carregar resultado:', error)
      }
    },
    confirmarDeletarResultado(id) {
      this.resultadoToDelete = id
      this.showConfirmDelete = true
    },
    async deletarResultado() {
      try {
        await axios.delete(`/api/resultados-salvos/${this.resultadoToDelete}`)
        await this.carregarResultadosSalvos()
        this.showConfirmDelete = false
        this.resultadoToDelete = null
        console.log('Resultado deletado com sucesso!')
      } catch (error) {
        console.error('Erro ao deletar resultado:', error)
      }
    },
    cancelarDeletarResultado() {
      this.showConfirmDelete = false
      this.resultadoToDelete = null
    },
    getRoadmapEndDate(resultado) {
      try {
        if (resultado?.roadmap_end_date) {
          const [year, month, day] = resultado.roadmap_end_date.split('-').map(Number)
          const date = new Date(year, month - 1, day)
          return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
        }
        return null
      } catch (e) {
        return null
      }
    },
    reloadApp() {
      window.location.reload()
    },
    getModuleTitle() {
      const titles = {
        'roadmap': 'Gerador de Roadmap',
        'estimativa': 'Gerador de Estimativa',
        'projetos': 'Gerenciamento de Projetos',
        'colaboradores': 'Gerenciamento de Colaboradores',
        'cargos-habilidades': 'Gerenciamento de Cargos & Habilidades',
        'tribos-squads': 'Gerenciamento de Tribos & Squads',
        'relatorios': 'Relatórios e Análises',
        'periodos-roadmaps' : 'Períodos de Roadmaps'
      }
      return titles[this.activeModule] || 'Sistema de Alocação'
    },
    getYearStartDate() {
      if (!this.selectedYear) return null
      const periodo = this.periodosRoadmaps.find(p => p.ano === this.selectedYear)
      return periodo?.inicio || null
    },
    getYearEndDate() {
      if (!this.selectedYear) return null
      const periodo = this.periodosRoadmaps.find(p => p.ano === this.selectedYear)
      return periodo?.termino || null
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A'
      const date = new Date(dateStr + 'T00:00:00')
      return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
    }
  }
}
</script>

<style>
.form-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #0891B2 0%, #0C94AD 100%);
  outline: none;
  cursor: pointer;
}

.form-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ffffff;
  border: 2px solid #0891B2;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ffffff;
  border: 2px solid #0891B2;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Scrollbar Styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #0891B2, #0C94AD);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #0e7490, #0a7c96);
}

@media (max-width: 768px) {
  .flex {
    flex-direction: column;
  }
  
  .w-64, .w-72 {
    width: 100% !important;
    height: auto;
  }
}
</style>