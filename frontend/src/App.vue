<template>
  <div class="h-screen bg-background-default font-sans overflow-hidden">
    <div class="flex h-full">
      <!-- Menu Lateral -->
      <div class="w-64 bg-gradient-to-b from-cyan-600 to-green-400 text-white overflow-y-auto flex flex-col">
        <div class="p-4 flex-1">
          <h2 class="text-lg font-semibold mb-6 cursor-pointer hover:text-white/90 transition-colors" @click="reloadApp">Roadmaps & Estimativas</h2>
          <nav class="space-y-6">
            <div v-for="section in menuSections" :key="section.title" class="space-y-1">
              <div class="text-xs font-semibold text-white text-opacity-60 uppercase tracking-wider px-3 mb-2">
                {{ section.title }}
              </div>
              <button 
                v-for="item in section.items" 
                :key="item.id"
                @click="activeModule = item.id"
                :class="[
                  'w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  activeModule === item.id 
                    ? 'bg-white bg-opacity-20 text-white shadow-md' 
                    : 'text-white hover:bg-white hover:bg-opacity-15'
                ]"
              >
                <component :is="item.icon" class="w-5 h-5" />
                {{ item.label }}
              </button>
            </div>
          </nav>
        </div>
      </div>

      <!-- Área do Roadmap com header estendido -->
      <div v-if="activeModule === 'roadmap'" class="flex-1 flex flex-col">
        <!-- Header estendido -->
        <div class="text-white px-6 py-4 shadow-sm flex-shrink-0 flex items-center justify-between" style="background: linear-gradient(to bottom, #0891B2, #0C94AD);">
          <h1 class="text-xl font-semibold">{{ getModuleTitle() }}</h1>
          <div class="flex items-center gap-3">
            <select 
              v-model="selectedTriboId" 
              @change="onTriboChange"
              class="px-3 py-1.5 border border-white border-opacity-30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-white bg-white bg-opacity-20 text-white"
            >
              <option :value="null" class="text-gray-900">Tribo</option>
              <option v-for="tribo in tribos" :key="tribo.id" :value="tribo.id" class="text-gray-900">
                {{ tribo.nome }}
              </option>
            </select>
            <SquadSelector v-model="selectedSquadId" :squads="filteredSquads" @update:modelValue="applySquadFilter" />
          </div>
        </div>
        
        <!-- Conteúdo do roadmap -->
        <div class="flex flex-1 overflow-hidden">
          <!-- Parâmetros Sidebar -->
          <div v-if="selectedSquadId" class="w-72 bg-gray-50 border-r border-gray-200 flex-shrink-0 overflow-y-auto">
            <div class="p-4 space-y-4">
            <div class="bg-white rounded-md shadow-sm p-4">
              <h3 class="text-base font-semibold text-gray-900 mb-4">Parâmetros do Algoritmo</h3>
              
              <form class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Algoritmo</label>
                  <select v-model="params.algorithm" class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main">
                    <option value="ga">Algoritmo Genético</option>
                    <option value="aco">Colônia de Formigas</option>
                  </select>
                </div>
                <!-- GA Parameters -->
                <template v-if="params.algorithm === 'ga'">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">População</label>
                    <input 
                      v-model="params.tam_pop" 
                      type="range" 
                      min="10" 
                      max="100" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>10</span>
                      <span class="font-medium">{{ params.tam_pop }}</span>
                      <span>100</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Gerações</label>
                    <input 
                      v-model="params.n_gen" 
                      type="range" 
                      min="5" 
                      max="1000" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>5</span>
                      <span class="font-medium">{{ params.n_gen }}</span>
                      <span>1000</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Crossover</label>
                    <input 
                      v-model="params.pc" 
                      type="range" 
                      min="0" 
                      max="1" 
                      step="0.1" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>0</span>
                      <span class="font-medium">{{ params.pc }}</span>
                      <span>1</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Mutação</label>
                    <input 
                      v-model="params.pm" 
                      type="range" 
                      min="0" 
                      max="1" 
                      step="0.1" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>0</span>
                      <span class="font-medium">{{ params.pm }}</span>
                      <span>1</span>
                    </div>
                  </div>
                </template>
                
                <!-- ACO Parameters -->
                <template v-else>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Número de Formigas</label>
                    <input 
                      v-model="params.tam_pop" 
                      type="range" 
                      min="10" 
                      max="50" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>10</span>
                      <span class="font-medium">{{ params.tam_pop }}</span>
                      <span>50</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Iterações Máximas</label>
                    <input 
                      v-model="params.n_gen" 
                      type="range" 
                      min="5" 
                      max="50" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>5</span>
                      <span class="font-medium">{{ params.n_gen }}</span>
                      <span>50</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Alpha (Feromônio)</label>
                    <input 
                      v-model="params.alpha" 
                      type="range" 
                      min="0.1" 
                      max="3" 
                      step="0.1" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>0.1</span>
                      <span class="font-medium">{{ params.alpha }}</span>
                      <span>3</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Beta (Heurística)</label>
                    <input 
                      v-model="params.beta" 
                      type="range" 
                      min="0.1" 
                      max="5" 
                      step="0.1" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>0.1</span>
                      <span class="font-medium">{{ params.beta }}</span>
                      <span>5</span>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Rho (Evaporação)</label>
                    <input 
                      v-model="params.rho" 
                      type="range" 
                      min="0.1" 
                      max="0.9" 
                      step="0.1" 
                      class="form-slider"
                    />
                    <div class="flex justify-between text-sm text-text-secondary mt-1">
                      <span>0.1</span>
                      <span class="font-medium">{{ params.rho }}</span>
                      <span>0.9</span>
                    </div>
                  </div>
                </template>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Data de Referência</label>
                  <input 
                    v-model="params.ref_date" 
                    type="date" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary-main"
                  />
                </div>
                
                <div class="border-t border-gray-200 pt-4 mt-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input 
                      v-model="customizeExecution" 
                      type="checkbox" 
                      class="w-4 h-4 text-primary-main rounded border-gray-300 focus:ring-primary-main"
                    />
                    <span class="text-sm font-medium text-gray-700">Personalizar execução</span>
                  </label>
                  <p class="text-xs text-gray-500 mt-1 ml-6">Selecione projetos e colaboradores específicos</p>
                </div>
                
                <div class="space-y-2 pt-2">
                  <button 
                    @click="prepareExecution" 
                    :disabled="loading" 
                    class="bg-primary-main text-white px-4 py-2 rounded-md text-sm font-medium w-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-light transition-colors shadow-sm"
                    type="button"
                  >
                    <span v-if="loading" class="flex items-center justify-center">
                      <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Executando...
                    </span>
                    <span v-else>Executar {{ params.algorithm.toUpperCase() }}</span>
                  </button>
                  
                  <button 
                    @click="showLoadModal = true" 
                    class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full hover:bg-blue-700 transition-colors shadow-sm"
                    type="button"
                  >
                    Carregar Resultado
                  </button>
                  
                  <button 
                    @click="showComparisonParams = !showComparisonParams" 
                    class="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full hover:bg-green-700 transition-colors shadow-sm"
                    type="button"
                  >
                    {{ showComparisonParams ? 'Ocultar' : 'Configurar' }} Comparação
                  </button>
                </div>
              </form>
            </div>
            
            <!-- Comparison Parameters -->
            <div v-if="showComparisonParams" class="bg-white rounded-md shadow-sm p-4">
              <h4 class="text-sm font-semibold text-gray-900 mb-3">Parâmetros para Comparação</h4>
                
              <!-- GA Parameters -->
              <div class="mb-4">
                <h5 class="text-xs font-semibold text-blue-600 mb-2 uppercase tracking-wide">Algoritmo Genético</h5>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">População</label>
                    <input v-model="gaParams.tam_pop" type="number" min="10" max="100" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Gerações</label>
                    <input v-model="gaParams.n_gen" type="number" min="10" max="500" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Crossover</label>
                    <input v-model="gaParams.pc" type="number" min="0" max="1" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Mutação</label>
                    <input v-model="gaParams.pm" type="number" min="0" max="1" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500">
                  </div>
                </div>
              </div>
                
              <!-- ACO Parameters -->
              <div class="mb-4">
                <h5 class="text-xs font-semibold text-green-600 mb-2 uppercase tracking-wide">Colônia de Formigas</h5>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Formigas</label>
                    <input v-model="acoParams.tam_pop" type="number" min="10" max="50" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Iterações</label>
                    <input v-model="acoParams.n_gen" type="number" min="5" max="50" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Alpha</label>
                    <input v-model="acoParams.alpha" type="number" min="0.1" max="3" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Beta</label>
                    <input v-model="acoParams.beta" type="number" min="0.1" max="5" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Rho</label>
                    <input v-model="acoParams.rho" type="number" min="0.1" max="0.9" step="0.1" class="w-full px-2 py-1.5 border border-gray-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-green-500">
                  </div>
                </div>
              </div>
                
              <button 
                @click="compararAlgoritmos" 
                :disabled="loading" 
                class="bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium w-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-purple-700 transition-colors shadow-sm"
                type="button"
              >
                  <span v-if="loading" class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Comparando...
                  </span>
                <span v-else>Executar Comparação</span>
              </button>
            </div>
            </div>
          </div>
          
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
            <div v-else-if="!resultado" class="mt-6 space-y-4">
              <div class="bg-semantic-info-light border border-semantic-info-main rounded-md p-3">
                <div class="flex items-center">
                  <svg class="w-4 h-4 text-semantic-info-main mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-semantic-info-main text-sm">Configure os parâmetros e execute o algoritmo</span>
                </div>
              </div>
              
              <div v-if="resultadosSalvos.length > 0">
                <h4 class="text-base font-semibold text-gray-900 mb-3">Últimas Execuções Salvas</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3">
                  <div 
                    v-for="resultado in resultadosSalvos.slice(0, 6)" 
                    :key="resultado.id" 
                    @click="carregarResultado(resultado.id)"
                    class="bg-white border rounded-lg p-4 hover:shadow-md transition-all cursor-pointer group"
                  >
                    <div class="flex items-start justify-between mb-2">
                      <h5 class="font-semibold text-gray-900 text-sm group-hover:text-primary-main transition-colors line-clamp-2">{{ resultado.nome }}</h5>
                      <span class="text-xs px-2 py-0.5 rounded flex-shrink-0 ml-2" :class="resultado.algoritmo === 'ga' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">{{ resultado.algoritmo.toUpperCase() }}</span>
                    </div>
                    <div class="text-xs text-gray-600 space-y-1">
                      <p><span class="font-medium">Fitness:</span> {{ resultado.melhor_fitness.toFixed(2) }}</p>
                      <p v-if="resultado.parametros?.projeto_ids" class="flex items-center gap-1">
                        <span class="font-medium">Projetos:</span> {{ resultado.parametros.projeto_ids.length }}
                      </p>
                      <p v-if="getRoadmapEndDate(resultado)">
                        <span class="font-medium">Término:</span> {{ getRoadmapEndDate(resultado) }}
                      </p>
                      <p><span class="font-medium">Salvo em:</span> {{ new Date(resultado.data_execucao).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
                    </div>
                  </div>
                </div>
                <button 
                  v-if="resultadosSalvos.length > 6"
                  @click="showLoadModal = true" 
                  class="mt-3 text-sm text-primary-main hover:underline"
                >
                  Ver todos ({{ resultadosSalvos.length }})
                </button>
              </div>
              
              <div class="bg-white rounded-md shadow-sm p-4">
                <h4 class="text-base font-semibold text-gray-900 mb-3">Dados do Sistema</h4>
                <div class="grid grid-cols-2 gap-3">
                  <div @click="showColaboradoresModal = true" class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-3 border border-blue-200 cursor-pointer hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-xs text-blue-600 font-medium mb-1">Colaboradores</p>
                        <p class="text-2xl font-bold text-blue-700">{{ colaboradores.length }}</p>
                      </div>
                      <svg class="w-8 h-8 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                      </svg>
                    </div>
                  </div>
                  <div @click="showProjetosModal = true" class="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-3 border border-green-200 cursor-pointer hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-xs text-green-600 font-medium mb-1">Projetos</p>
                        <p class="text-2xl font-bold text-green-700">{{ projetos.length }}</p>
                      </div>
                      <svg class="w-8 h-8 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                      </svg>
                    </div>
                  </div>
                  <div @click="showCargosModal = true" class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-3 border border-purple-200 cursor-pointer hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-xs text-purple-600 font-medium mb-1">Cargos</p>
                        <p class="text-2xl font-bold text-purple-700">{{ cargos.length }}</p>
                      </div>
                      <svg class="w-8 h-8 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"/>
                        <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z"/>
                      </svg>
                    </div>
                  </div>
                  <div @click="showHabilidadesModal = true" class="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-3 border border-orange-200 cursor-pointer hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-xs text-orange-600 font-medium mb-1">Habilidades</p>
                        <p class="text-2xl font-bold text-orange-700">{{ habilidades.length }}</p>
                      </div>
                      <svg class="w-8 h-8 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                    </div>
                  </div>
                </div>
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
        <!-- Header (outros módulos) -->
        <div class="text-white px-6 py-4 shadow-sm flex-shrink-0 flex items-center justify-between" style="background: linear-gradient(to bottom, #0891B2, #0C94AD);">
          <h1 class="text-xl font-semibold">{{ getModuleTitle() }}</h1>
          <div class="flex items-center gap-3">
            <select 
              v-model="selectedTriboId" 
              @change="onTriboChange"
              class="px-3 py-1.5 border border-white border-opacity-30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-white bg-white bg-opacity-20 text-white"
            >
              <option :value="null" class="text-gray-900">Tribo</option>
              <option v-for="tribo in tribos" :key="tribo.id" :value="tribo.id" class="text-gray-900">
                {{ tribo.nome }}
              </option>
            </select>
            <SquadSelector v-model="selectedSquadId" :squads="filteredSquads" @update:modelValue="applySquadFilter" />
          </div>
        </div>
        
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
            <div v-else class="h-full overflow-y-auto p-4">
              <ProjetosCrud :selectedSquadId="selectedSquadId" :allProjetos="allProjetos" @reload="carregarDados" />
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
              <ColaboradoresCrud :key="selectedSquadId" :selectedSquadId="selectedSquadId" :allColaboradores="allColaboradores" @reload="carregarDados" />
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

          <!-- Módulo Relatórios -->
          <div v-if="activeModule === 'relatorios'" class="h-full overflow-y-auto p-4">
            <div class="bg-white rounded-md shadow-sm p-6">
              <p class="text-text-secondary">Módulo de relatórios em desenvolvimento...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de Seleção -->
    <div v-if="showSelectionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showSelectionModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-5xl w-full mx-4 max-h-[90vh] flex flex-col">
        <div class="px-6 py-3 border-b flex justify-between items-center">
          <h3 class="text-base font-semibold text-text-primary">Personalizar Execução</h3>
          <button @click="showSelectionModal = false" class="text-text-secondary hover:text-text-primary">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4">
          <!-- Skill Coverage Warning -->
          <div v-if="missingSkills.length > 0" class="mb-4 bg-yellow-50 border border-yellow-300 rounded p-3">
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <div class="flex-1">
                <p class="text-sm font-medium text-yellow-800">Habilidades não cobertas</p>
                <p class="text-xs text-yellow-700 mt-1">Os projetos selecionados requerem habilidades que nenhum colaborador selecionado possui:</p>
                <div class="flex flex-wrap gap-1 mt-2">
                  <span v-for="skill in missingSkills" :key="skill" class="inline-block px-2 py-0.5 bg-yellow-200 text-yellow-800 rounded text-xs font-medium">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
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
                  v-for="projeto in projetos" 
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
            
            <!-- Colaboradores -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-text-primary">Colaboradores ({{ selectedCollaborators.length }}/{{ colaboradores.length }})</h4>
                <button @click="toggleAllCollaborators" class="text-xs text-primary-main hover:underline">
                  {{ selectedCollaborators.length === colaboradores.length ? 'Desmarcar' : 'Selecionar' }} todos
                </button>
              </div>
              <div class="space-y-1 max-h-[400px] overflow-y-auto border rounded p-2">
                <div 
                  v-for="colab in colaboradores" 
                  :key="colab.id" 
                  @click="toggleCollaborator(colab.id)"
                  class="flex items-center gap-2 cursor-pointer p-1.5 rounded transition-colors border"
                  :class="selectedCollaborators.includes(colab.id) ? 'bg-green-100 border-green-300' : 'hover:bg-gray-50 border-transparent'"
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
                        <div class="flex flex-wrap gap-1">
                          <span v-for="hab in member.habilidades" :key="hab.id" class="inline-block px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">
                            {{ hab.nome }}
                          </span>
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
                  <button @click="addSimulatedMember" class="w-full px-2 py-1 bg-purple-600 text-white rounded text-xs hover:bg-purple-700">Adicionar</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-4 py-3 border-t flex justify-between items-center bg-gray-50">
          <div class="text-xs text-text-secondary">
            {{ selectedProjects.length }} projeto(s), {{ selectedCollaborators.length + simulatedMembers.length }} colaborador(es)
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
              :disabled="selectedProjects.length === 0 || selectedCollaborators.length === 0"
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
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            <div 
              v-for="resultado in resultadosSalvos" 
              :key="resultado.id" 
              @click="carregarResultado(resultado.id)"
              class="bg-white border rounded-lg p-4 hover:shadow-lg transition-all group relative cursor-pointer h-[130px]"
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
              <div class="flex items-start justify-between mb-2 pr-6">
                <h5 class="font-semibold text-gray-900 text-sm line-clamp-2 flex-1">{{ resultado.nome }}</h5>
                <span class="text-xs px-2 py-0.5 rounded flex-shrink-0 ml-2" :class="resultado.algoritmo === 'ga' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">{{ resultado.algoritmo.toUpperCase() }}</span>
              </div>
              <div class="text-xs text-gray-600 space-y-1">
                <p><span class="font-medium">Fitness:</span> {{ resultado.melhor_fitness.toFixed(2) }}</p>
                <p v-if="resultado.parametros?.projeto_ids" class="flex items-center gap-1">
                  <span class="font-medium">Projetos:</span> {{ resultado.parametros.projeto_ids.length }}
                </p>
                <p v-if="getRoadmapEndDate(resultado)">
                  <span class="font-medium">Término:</span> {{ getRoadmapEndDate(resultado) }}
                </p>
                <p><span class="font-medium">Salvo em:</span> {{ new Date(resultado.data_execucao).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
              </div>
            </div>
          </div>
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
  </div>
</template>

<script>
import axios from 'axios'
import { CpuChipIcon, FolderIcon, UserGroupIcon, DocumentChartBarIcon, CogIcon, BriefcaseIcon, AcademicCapIcon } from '@heroicons/vue/24/outline'
import DadosTab from './components/DadosTab.vue'
import FitnessTab from './components/FitnessTab.vue'
import ConflitosTab from './components/ConflitosTab.vue'
import GanttTab from './components/GanttTab.vue'
import CalendarioTab from './components/CalendarioTab.vue'
import MapaAlocacaoTab from './components/MapaAlocacaoTab.vue'
import ProjetosCrud from './components/ProjetosCrud.vue'
import ColaboradoresCrud from './components/ColaboradoresCrud.vue'
import CargosHabilidadesCrud from './components/CargosHabilidadesCrud.vue'
import TribosSquadsCrud from './components/TribosSquadsCrud.vue'
import ConfirmModal from './components/ConfirmModal.vue'
import SquadSelector from './components/SquadSelector.vue'

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
    ConfirmModal,
    SquadSelector,
    CpuChipIcon,
    FolderIcon,
    UserGroupIcon,
    DocumentChartBarIcon,
    CogIcon,
    BriefcaseIcon,
    AcademicCapIcon
  },
  data() {
    return {
      activeModule: 'roadmap',
      customizeExecution: false,
      showSelectionModal: false,
      showSaveModal: false,
      showLoadModal: false,
      showConfirmDelete: false,
      showColaboradoresModal: false,
      showProjetosModal: false,
      showCargosModal: false,
      showHabilidadesModal: false,
      expandedProjects: {},
      resultadoToDelete: null,
      saveResultName: '',
      resultadosSalvos: [],
      selectedProjects: [],
      selectedCollaborators: [],
      simulatedMembers: [],
      newMember: { cargo_id: null, habilidade_names: [] },
      cargos: [],
      habilidades: [],
      params: {
        algorithm: 'ga',
        tam_pop: 50,
        n_gen: 200,
        pc: 0.7,
        pm: 0.3,
        alpha: 1.0,
        beta: 2.0,
        rho: 0.5,
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
      selectedTriboId: null,
      selectedSquadId: null,
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
            { id: 'cargos-habilidades', label: 'Cargos e Habilidades', icon: 'BriefcaseIcon' }
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
      comparacaoResultado: null
    }
  },
  computed: {
    filteredSquads() {
      if (!this.selectedTriboId) return this.squads
      return this.squads.filter(s => s.tribo_id === this.selectedTriboId)
    },
    allColaboradoresWithSimulated() {
      return [...this.colaboradores, ...this.simulatedMembers]
    },
    filteredHabilidadesForCargo() {
      if (!this.newMember.cargo_id) return []
      return this.habilidades.filter(h => h.cargo_id == this.newMember.cargo_id)
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
      
      // Get available skills from selected collaborators
      this.colaboradores
        .filter(c => this.selectedCollaborators.includes(c.id))
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
    async carregarDados() {
      try {
        console.log('Carregando dados...')
        const [colabRes, projRes, tribosRes, squadsRes] = await Promise.all([
          axios.get('/api/colaboradores'),
          axios.get('/api/projetos'),
          axios.get('/api/tribos'),
          axios.get('/api/squads')
        ])
        console.log('Colaboradores:', colabRes.data)
        console.log('Projetos:', projRes.data)
        this.allColaboradores = colabRes.data
        this.allProjetos = projRes.data
        this.tribos = tribosRes.data
        this.squads = squadsRes.data
        this.loadSavedFilters()
        console.log(`Carregados ${this.allColaboradores.length} colaboradores e ${this.allProjetos.length} projetos`)
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        console.error('Erro ao carregar dados:', error.message)
      }
    },
    applySquadFilter() {
      if (this.selectedSquadId) {
        this.colaboradores = this.allColaboradores.filter(c => c.squad?.id === this.selectedSquadId)
        this.projetos = this.allProjetos.filter(p => p.squad?.id === this.selectedSquadId)
        localStorage.setItem('selectedSquadId', this.selectedSquadId.toString())
      } else {
        this.colaboradores = this.allColaboradores
        this.projetos = this.allProjetos
        localStorage.removeItem('selectedSquadId')
      }
      this.resultado = null
      this.comparacaoResultado = null
      this.initializeSelections()
      this.carregarResultadosSalvos()
    },
    onTriboChange() {
      this.selectedSquadId = null
      localStorage.setItem('selectedTriboId', this.selectedTriboId?.toString() || '')
      localStorage.removeItem('selectedSquadId')
      this.applySquadFilter()
    },
    loadSavedFilters() {
      const savedTriboId = localStorage.getItem('selectedTriboId')
      const savedSquadId = localStorage.getItem('selectedSquadId')
      
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
        }
      }
      
      this.applySquadFilter()
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
      
      this.simulatedMembers.push({
        id: `sim_${Date.now()}`,
        nome: `${cargo.nome} Simulado ${cargoSimCount}`,
        cargo: cargo,
        habilidades: habilidades,
        simulated: true
      })
      
      this.newMember = { cargo_id: null, habilidade_names: [] }
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
    prepareExecution() {
      if (this.customizeExecution) {
        this.showSelectionModal = true
      } else {
        this.selectedProjects = this.projetos.map(p => p.id)
        this.selectedCollaborators = this.colaboradores.map(c => c.id)
        this.simulatedMembers = []
        this.executarAlgoritmo()
      }
    },
    async executarAlgoritmo() {
      this.showSelectionModal = false
      this.loading = true
      try {
        // Reload data to get latest collaborators
        await this.carregarDados()
        
        const endpoint = this.params.algorithm === 'aco' ? '/api/executar-aco' : '/api/executar-algoritmo'
        const payload = {
          ...this.params,
          projeto_ids: this.selectedProjects,
          colaborador_ids: this.selectedCollaborators,
          simulated_members: this.simulatedMembers.map(m => ({
            nome: m.nome,
            cargo_id: m.cargo.id,
            habilidade_names: m.habilidades.map(h => h.nome)
          }))
        }
        const response = await axios.post(endpoint, payload)
        this.resultado = response.data
        this.activeTab = 'gantt'
        console.log(`${this.params.algorithm.toUpperCase()} executado com sucesso!`)
      } catch (error) {
        console.error('Erro ao executar algoritmo')
      } finally {
        this.loading = false
      }
    },
    async compararAlgoritmos() {
      this.loading = true
      try {
        const comparisonParams = {
          ref_date: this.params.ref_date,
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
    async carregarResultadosSalvos() {
      try {
        const response = await axios.get('/api/resultados-salvos')
        let resultados = response.data
        if (this.selectedSquadId) {
          resultados = resultados.filter(r => r.squad_id === this.selectedSquadId)
        }
        this.resultadosSalvos = resultados
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
          saved_colaboradores: this.colaboradores.filter(c => this.selectedCollaborators.includes(c.id)),
          simulated_members: this.simulatedMembers.map(m => ({
            nome: m.nome,
            cargo_id: m.cargo.id,
            cargo: m.cargo,
            habilidade_names: m.habilidades.map(h => h.nome),
            habilidades: m.habilidades
          }))
        }
        
        await axios.post('/api/resultados-salvos', {
          nome: this.saveResultName,
          algoritmo: this.params.algorithm,
          melhor_fitness: this.resultado.melhor_fitness,
          roadmap_end_date: roadmapEndDate,
          squad_id: this.selectedSquadId,
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
        this.params = saved.parametros
        
        // Restore saved collaborators (including deleted ones)
        if (saved.parametros.saved_colaboradores) {
          this.colaboradores = saved.parametros.saved_colaboradores
        }
        
        // Restore simulated members if they exist
        if (saved.parametros.simulated_members && saved.parametros.simulated_members.length > 0) {
          this.simulatedMembers = saved.parametros.simulated_members.map((m, idx) => ({
            id: `sim_${Date.now()}_${idx}`,
            nome: m.nome,
            cargo: m.cargo || this.cargos.find(c => c.id === m.cargo_id),
            habilidades: m.habilidades || this.habilidades.filter(h => m.habilidade_names.includes(h.nome)),
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
        'relatorios': 'Relatórios e Análises'
      }
      return titles[this.activeModule] || 'Sistema de Alocação'
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