import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useWealthStore = defineStore('wealth', () => {
  // State
  const owners = ref([])
  const currentOwner = ref(null)
  const wealthData = ref([])
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()

  // Getters
  const wealthyOwners = computed(() => {
    return owners.value.filter(owner => {
      const netWorth = parseFloat(owner.netWorth?.replace(/[^0-9.-]+/g, '') || 0)
      return netWorth >= 1000000 // $1M or more
    }).sort((a, b) => {
      const aWorth = parseFloat(a.netWorth?.replace(/[^0-9.-]+/g, '') || 0)
      const bWorth = parseFloat(b.netWorth?.replace(/[^0-9.-]+/g, '') || 0)
      return bWorth - aWorth // Sort by net worth descending
    })
  })

  const ownerProperties = computed(() => {
    if (!currentOwner.value) return []
    return currentOwner.value.properties || []
  })

  const totalPropertyValue = computed(() => {
    if (!ownerProperties.value.length) return 0
    
    return ownerProperties.value.reduce((total, property) => {
      const value = parseFloat(property.value?.replace(/[^0-9.-]+/g, '') || 0)
      return total + value
    }, 0)
  })

  // Actions
  async function fetchOwners(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/owners', { params })
      owners.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch owners'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchOwnerById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/owners/${id}`)
      currentOwner.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || `Failed to fetch owner with ID: ${id}`
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function searchOwners(query) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/owners/search', { params: { query } })
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Owner search failed'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchWealthData(ownerId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/wealth-data/${ownerId}`)
      wealthData.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch wealth data'
      console.error(error.value)
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchWealthTrends(ownerId, timeframe = 'yearly') {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/wealth-data/${ownerId}/trends`, {
        params: { timeframe }
      })
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch wealth trends'
      console.error(error.value)
      return []
    } finally {
      loading.value = false
    }
  }

  async function fetchRelatedOwners(ownerId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/owners/${ownerId}/related`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch related owners'
      console.error(error.value)
      return []
    } finally {
      loading.value = false
    }
  }

  async function compareOwners(ownerIds) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/owners/compare', { owner_ids: ownerIds })
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to compare owners'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    owners,
    currentOwner,
    wealthData,
    loading,
    error,
    
    // Getters
    wealthyOwners,
    ownerProperties,
    totalPropertyValue,
    
    // Actions
    fetchOwners,
    fetchOwnerById,
    searchOwners,
    fetchWealthData,
    fetchWealthTrends,
    fetchRelatedOwners,
    compareOwners
  }
})