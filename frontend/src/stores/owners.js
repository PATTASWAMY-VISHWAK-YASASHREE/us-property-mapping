import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useOwnersStore = defineStore('owners', () => {
  // State
  const owners = ref([])
  const currentOwner = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()

  // Getters
  const individualOwners = computed(() => {
    return owners.value.filter(owner => owner.type === 'individual')
  })

  const corporateOwners = computed(() => {
    return owners.value.filter(owner => owner.type === 'corporate')
  })

  const ownerProperties = computed(() => {
    if (!currentOwner.value) return []
    return currentOwner.value.properties || []
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

  async function createOwner(ownerData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/owners', ownerData)
      owners.value.push(response.data)
      toast.success('Owner created successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create owner'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateOwner(id, ownerData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`/api/owners/${id}`, ownerData)
      
      // Update the owner in the owners array
      const index = owners.value.findIndex(owner => owner.id === id)
      if (index !== -1) {
        owners.value[index] = response.data
      }
      
      // Update current owner if it's the one being edited
      if (currentOwner.value && currentOwner.value.id === id) {
        currentOwner.value = response.data
      }
      
      toast.success('Owner updated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update owner'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function deleteOwner(id) {
    loading.value = true
    error.value = null
    
    try {
      await axios.delete(`/api/owners/${id}`)
      
      // Remove the owner from the owners array
      owners.value = owners.value.filter(owner => owner.id !== id)
      
      // Clear current owner if it's the one being deleted
      if (currentOwner.value && currentOwner.value.id === id) {
        currentOwner.value = null
      }
      
      toast.success('Owner deleted successfully')
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete owner'
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

  async function fetchOwnerProperties(ownerId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/owners/${ownerId}/properties`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch owner properties'
      toast.error(error.value)
      throw error.value
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
    loading,
    error,
    
    // Getters
    individualOwners,
    corporateOwners,
    ownerProperties,
    
    // Actions
    fetchOwners,
    fetchOwnerById,
    createOwner,
    updateOwner,
    deleteOwner,
    searchOwners,
    fetchOwnerProperties,
    fetchRelatedOwners,
    compareOwners
  }
})