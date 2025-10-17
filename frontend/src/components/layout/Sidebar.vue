<template>
  <div class="w-64 bg-gradient-to-b from-cyan-600 to-green-400 text-white overflow-y-auto flex flex-col">
    <div class="p-4 flex-1">
      <h2 class="text-lg font-semibold mb-6 cursor-pointer hover:text-white/90 transition-colors" @click="$emit('reload')">
        Roadmaps & Estimativas
      </h2>
      <nav class="space-y-6">
        <div v-for="section in menuSections" :key="section.title" class="space-y-1">
          <div class="text-xs font-semibold text-white text-opacity-60 uppercase tracking-wider px-3 mb-2">
            {{ section.title }}
          </div>
          <button 
            v-for="item in section.items" 
            :key="item.id"
            @click="$emit('update:activeModule', item.id)"
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
</template>

<script>
import { CpuChipIcon, FolderIcon, UserGroupIcon, BriefcaseIcon, AcademicCapIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'Sidebar',
  components: { CpuChipIcon, FolderIcon, UserGroupIcon, BriefcaseIcon, AcademicCapIcon },
  props: {
    activeModule: { type: String, required: true }
  },
  emits: ['update:activeModule', 'reload'],
  data() {
    return {
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
      ]
    }
  }
}
</script>
