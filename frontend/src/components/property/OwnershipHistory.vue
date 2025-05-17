<template>
  <div class="ownership-history">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Ownership History</h2>
    
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="spinner"></div>
    </div>
    
    <div v-else-if="ownershipHistory && ownershipHistory.length > 0">
      <!-- Timeline View -->
      <div class="ownership-timeline mb-8">
        <div class="relative">
          <!-- Vertical line -->
          <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-blue-200"></div>
          
          <!-- Timeline items -->
          <div 
            v-for="(ownership, index) in ownershipHistory" 
            :key="index"
            class="relative pl-12 pb-8"
          >
            <!-- Timeline dot -->
            <div class="absolute left-0 top-1 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
              {{ index + 1 }}
            </div>
            
            <!-- Timeline content -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div class="flex flex-col md:flex-row md:justify-between md:items-center">
                <div>
                  <h3 class="text-lg font-semibold text-gray-800">{{ ownership.owner.name }}</h3>
                  <p class="text-gray-600">{{ ownership.owner.owner_type }}</p>
                </div>
                <div class="mt-2 md:mt-0">
                  <span class="inline-block bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded">
                    {{ formatOwnershipDates(ownership) }}
                  </span>
                </div>
              </div>
              
              <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-500">Ownership Percentage</p>
                  <p class="font-medium">{{ ownership.ownership_percentage }}%</p>
                </div>
                
                <div v-if="ownership.owner.address">
                  <p class="text-sm text-gray-500">Owner Address</p>
                  <p class="font-medium">{{ ownership.owner.address }}</p>
                </div>
              </div>
              
              <div class="mt-4" v-if="ownership.owner.wealth_data">
                <p class="text-sm text-gray-500 mb-1">Wealth Information</p>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="text-gray-600">Estimated Net Worth:</span>
                    <span class="font-medium ml-1">${{ formatCurrency(ownership.owner.wealth_data.estimated_net_worth) }}</span>
                  </div>
                  <div>
                    <span class="text-gray-600">Real Estate Assets:</span>
                    <span class="font-medium ml-1">${{ formatCurrency(ownership.owner.wealth_data.real_estate_assets) }}</span>
                  </div>
                </div>
              </div>
              
              <div class="mt-4 flex justify-end">
                <button 
                  @click="viewOwnerDetails(ownership.owner.id)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  View Owner Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Table View -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200">
          <thead>
            <tr>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Owner</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Type</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Ownership %</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Start Date</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">End Date</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Duration</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(ownership, index) in ownershipHistory" :key="`table-${index}`">
              <td class="py-3 px-4 text-sm">{{ ownership.owner.name }}</td>
              <td class="py-3 px-4 text-sm">{{ ownership.owner.owner_type }}</td>
              <td class="py-3 px-4 text-sm">{{ ownership.ownership_percentage }}%</td>
              <td class="py-3 px-4 text-sm">{{ formatDate(ownership.start_date) }}</td>
              <td class="py-3 px-4 text-sm">{{ formatDate(ownership.end_date) || 'Current' }}</td>
              <td class="py-3 px-4 text-sm">{{ calculateDuration(ownership) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else class="bg-gray-50 p-6 rounded-lg text-center">
      <p class="text-gray-500">No ownership history available for this property.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

defineProps({
  propertyId: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  ownershipHistory: {
    type: Array,
    default: () => []
  }
})

const router = useRouter()

// Format dates
const formatDate = (dateString) => {
  if (!dateString) return null
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

// Format ownership dates range
const formatOwnershipDates = (ownership) => {
  const startDate = formatDate(ownership.start_date)
  const endDate = ownership.end_date ? formatDate(ownership.end_date) : 'Present'
  
  return `${startDate} - ${endDate}`
}

// Calculate ownership duration
const calculateDuration = (ownership) => {
  const start = new Date(ownership.start_date)
  const end = ownership.end_date ? new Date(ownership.end_date) : new Date()
  
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  const years = Math.floor(diffDays / 365)
  const months = Math.floor((diffDays % 365) / 30)
  
  if (years > 0 && months > 0) {
    return `${years} year${years > 1 ? 's' : ''}, ${months} month${months > 1 ? 's' : ''}`
  } else if (years > 0) {
    return `${years} year${years > 1 ? 's' : ''}`
  } else if (months > 0) {
    return `${months} month${months > 1 ? 's' : ''}`
  } else {
    return `${diffDays} day${diffDays > 1 ? 's' : ''}`
  }
}

// Format currency values
const formatCurrency = (value) => {
  if (!value) return 'N/A'
  
  return new Intl.NumberFormat('en-US', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Navigate to owner details page
const viewOwnerDetails = (ownerId) => {
  router.push(`/owner/${ownerId}`)
}
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #4a6cf7;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>