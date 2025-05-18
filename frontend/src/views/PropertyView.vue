<template>
  <div class="property-view">
    <div class="container mx-auto px-4 py-8">
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{{ error }}</p>
      </div>
      
      <div v-else-if="property">
        <!-- Property Header -->
        <div class="mb-8">
          <div class="flex flex-col md:flex-row md:justify-between md:items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ property.address }}</h1>
              <p class="text-lg text-gray-600">{{ property.city }}, {{ property.state }} {{ property.zip_code }}</p>
            </div>
            <div class="mt-4 md:mt-0">
              <button 
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                @click="toggleBookmark"
              >
                {{ isBookmarked ? 'Remove Bookmark' : 'Bookmark' }}
              </button>
              <button 
                class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"
                @click="printReport"
              >
                Print Report
              </button>
            </div>
          </div>
        </div>
        
        <!-- Property Detail Component -->
        <PropertyDetail 
          :property="property" 
          :loading="loadingDetails" 
          @refresh="fetchPropertyDetails" 
        />
        
        <!-- Tabs Navigation -->
        <div class="border-b border-gray-200 mt-8">
          <nav class="flex -mb-px">
            <button 
              @click="activeTab = 'ownership'" 
              :class="[
                'py-4 px-6 font-medium text-sm',
                activeTab === 'ownership' 
                  ? 'border-b-2 border-blue-500 text-blue-600' 
                  : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Ownership History
            </button>
            <button 
              @click="activeTab = 'transactions'" 
              :class="[
                'py-4 px-6 font-medium text-sm',
                activeTab === 'transactions' 
                  ? 'border-b-2 border-blue-500 text-blue-600' 
                  : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Transaction Records
            </button>
            <button 
              @click="activeTab = 'comparables'" 
              :class="[
                'py-4 px-6 font-medium text-sm',
                activeTab === 'comparables' 
                  ? 'border-b-2 border-blue-500 text-blue-600' 
                  : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Comparable Properties
            </button>
          </nav>
        </div>
        
        <!-- Tab Content -->
        <div class="py-6">
          <!-- Ownership History Tab -->
          <div v-if="activeTab === 'ownership'">
            <OwnershipHistory 
              :property-id="propertyId" 
              :loading="loadingOwnership" 
              :ownership-history="ownershipHistory" 
            />
          </div>
          
          <!-- Transaction Records Tab -->
          <div v-if="activeTab === 'transactions'">
            <TransactionRecords 
              :property-id="propertyId" 
              :loading="loadingTransactions" 
              :transactions="transactions" 
            />
          </div>
          
          <!-- Comparable Properties Tab -->
          <div v-if="activeTab === 'comparables'">
            <ComparableProperties 
              :property-id="propertyId" 
              :loading="loadingComparables" 
              :comparables="comparableProperties" 
            />
          </div>
        </div>
      </div>
      
      <div v-else class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
        <p>Property not found</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePropertyStore } from '@/stores/property'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import zillowService from '@/services/zillowService'

// Import components
import PropertyDetail from '@/components/property/PropertyDetail.vue'
import OwnershipHistory from '@/components/property/OwnershipHistory.vue'
import TransactionRecords from '@/components/property/TransactionRecords.vue'
import ComparableProperties from '@/components/property/ComparableProperties.vue'

const route = useRoute()
const propertyStore = usePropertyStore()
const toast = useToast()

// State
const propertyId = computed(() => route.params.id)
const property = computed(() => propertyStore.currentProperty)
const loading = ref(false)
const loadingDetails = ref(false)
const loadingOwnership = ref(false)
const loadingTransactions = ref(false)
const loadingComparables = ref(false)
const error = ref(null)
const activeTab = ref('ownership')
const isBookmarked = ref(false)

// Data for tabs
const ownershipHistory = ref([])
const transactions = ref([])
const comparableProperties = ref([])

// Fetch property data
const fetchProperty = async () => {
  loading.value = true
  error.value = null
  
  try {
    await propertyStore.fetchPropertyById(propertyId.value)
    checkBookmarkStatus()
  } catch (err) {
    error.value = err.toString()
    toast.error('Failed to load property details')
  } finally {
    loading.value = false
  }
}

// Fetch additional property details
const fetchPropertyDetails = async () => {
  loadingDetails.value = true;
  
  try {
    // Use our Zillow service to get property details
    if (property.value && property.value.address) {
      const response = await zillowService.getPropertyDetailsByAddress(property.value.address);
      console.log('Zillow property details:', response);
      // Update property with additional details if needed
    } else {
      // Fallback to API if we don't have an address
      await axios.get(`/api/properties/zillow/details/${property.value.id}`);
    }
  } catch (err) {
    toast.error('Failed to load additional property details');
  } finally {
    loadingDetails.value = false;
  }
}

// Fetch ownership history
const fetchOwnershipHistory = async () => {
  if (activeTab.value !== 'ownership') return
  
  loadingOwnership.value = true
  
  try {
    const response = await axios.get(`/api/properties/${propertyId.value}/ownership`)
    ownershipHistory.value = response.data
  } catch (err) {
    toast.error('Failed to load ownership history')
    ownershipHistory.value = []
  } finally {
    loadingOwnership.value = false
  }
}

// Fetch transaction records
const fetchTransactions = async () => {
  if (activeTab.value !== 'transactions') return
  
  loadingTransactions.value = true
  
  try {
    const response = await axios.get(`/api/properties/${propertyId.value}/transactions`)
    transactions.value = response.data
  } catch (err) {
    toast.error('Failed to load transaction records')
    transactions.value = []
  } finally {
    loadingTransactions.value = false
  }
}

// Fetch comparable properties
const fetchComparables = async () => {
  if (activeTab.value !== 'comparables') return;
  
  loadingComparables.value = true;
  
  try {
    // Use our Zillow service to get comparable properties if we have property details
    if (property.value && property.value.address) {
      const params = {
        address: property.value.address
      };
      
      if (property.value.zillow_id) {
        params.zpid = property.value.zillow_id;
      }
      
      const response = await zillowService.getSimilarProperties(params);
      console.log('Zillow comparable properties:', response);
      
      if (response && response.similar && response.similar.length > 0) {
        comparableProperties.value = response.similar;
      } else {
        // Fallback to API if Zillow direct call doesn't return results
        const apiResponse = await axios.get(`/api/properties/zillow/comps/${propertyId.value}`);
        comparableProperties.value = apiResponse.data.comparables || [];
      }
    } else {
      // Fallback to API if we don't have property details
      const response = await axios.get(`/api/properties/zillow/comps/${propertyId.value}`);
      comparableProperties.value = response.data.comparables || [];
    }
  } catch (err) {
    toast.error('Failed to load comparable properties');
    comparableProperties.value = [];
  } finally {
    loadingComparables.value = false;
  }
}

// Check if property is bookmarked
const checkBookmarkStatus = async () => {
  try {
    const response = await axios.get('/api/properties/bookmarked')
    isBookmarked.value = response.data.some(p => p.id === propertyId.value)
  } catch (err) {
    console.error('Failed to check bookmark status:', err)
  }
}

// Toggle bookmark status
const toggleBookmark = async () => {
  try {
    if (isBookmarked.value) {
      await axios.delete(`/api/properties/bookmark/${propertyId.value}`)
      toast.success('Property removed from bookmarks')
    } else {
      await axios.post('/api/properties/bookmark', {
        property_id: propertyId.value
      })
      toast.success('Property added to bookmarks')
    }
    isBookmarked.value = !isBookmarked.value
  } catch (err) {
    toast.error('Failed to update bookmark')
  }
}

// Print property report
const printReport = () => {
  window.print()
}

// Watch for tab changes to load data
watch(activeTab, (newTab) => {
  if (newTab === 'ownership') {
    fetchOwnershipHistory()
  } else if (newTab === 'transactions') {
    fetchTransactions()
  } else if (newTab === 'comparables') {
    fetchComparables()
  }
})

// Lifecycle hooks
onMounted(() => {
  fetchProperty()
})
</script>

<style scoped>
.property-view {
  min-height: calc(100vh - 64px);
}

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

@media print {
  .property-view {
    padding: 0;
  }
  
  button {
    display: none;
  }
}
</style>