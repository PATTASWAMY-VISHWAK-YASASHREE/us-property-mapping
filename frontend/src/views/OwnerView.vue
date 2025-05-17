<template>
  <div class="owner-view">
    <div class="container mx-auto px-4 py-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold">Owner Details</h1>
        <div class="flex space-x-2">
          <button 
            @click="$router.go(-1)" 
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md flex items-center"
          >
            <span class="mr-1">←</span> Back
          </button>
          <button 
            v-if="currentOwner"
            @click="exportOwnerData" 
            class="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-md"
          >
            Export Data
          </button>
        </div>
      </div>
      
      <!-- Owner Analysis Component -->
      <OwnerAnalysis />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useWealthStore } from '../stores/wealth'
import OwnerAnalysis from '../components/wealth/OwnerAnalysis.vue'

const wealthStore = useWealthStore()
const currentOwner = computed(() => wealthStore.currentOwner)

function exportOwnerData() {
  if (!currentOwner.value) return
  
  // Prepare data for export
  const ownerData = {
    owner: currentOwner.value,
    properties: wealthStore.ownerProperties,
    wealthData: wealthStore.wealthData
  }
  
  // Convert to JSON string
  const jsonData = JSON.stringify(ownerData, null, 2)
  
  // Create a blob and download link
  const blob = new Blob([jsonData], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  
  // Create download link and trigger click
  const a = document.createElement('a')
  a.href = url
  a.download = `owner-${currentOwner.value.id}-data.json`
  document.body.appendChild(a)
  a.click()
  
  // Clean up
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.owner-view {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}
</style>