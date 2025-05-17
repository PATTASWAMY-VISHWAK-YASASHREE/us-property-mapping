import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const usePropertyStore = defineStore('property', () => {
  // State
  const properties = ref([])
  const currentProperty = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const searchResults = ref([])
  const searchFilters = ref({
    propertyType: [],
    minValue: 0,
    maxValue: null,
    minBedrooms: null,
    maxBedrooms: null,
    minBathrooms: null,
    maxBathrooms: null,
    yearBuiltMin: null,
    yearBuiltMax: null,
    dataSources: ['county-records', 'tax-assessor', 'census'],
    sortBy: 'relevance'
  })
  const savedSearches = ref([])
  const recentlyViewed = ref([])
  const toast = useToast()

  // Getters
  const filteredProperties = computed(() => {
    return properties.value.filter(property => {
      // Apply filters
      if (searchFilters.value.propertyType.length > 0 && 
          !searchFilters.value.propertyType.includes(property.propertyType)) {
        return false
      }
      
      if (searchFilters.value.minValue && property.value < searchFilters.value.minValue) {
        return false
      }
      
      if (searchFilters.value.maxValue && property.value > searchFilters.value.maxValue) {
        return false
      }
      
      if (searchFilters.value.minBedrooms && property.bedrooms < searchFilters.value.minBedrooms) {
        return false
      }
      
      if (searchFilters.value.maxBedrooms && property.bedrooms > searchFilters.value.maxBedrooms) {
        return false
      }
      
      if (searchFilters.value.minBathrooms && property.bathrooms < searchFilters.value.minBathrooms) {
        return false
      }
      
      if (searchFilters.value.maxBathrooms && property.bathrooms > searchFilters.value.maxBathrooms) {
        return false
      }
      
      if (searchFilters.value.yearBuiltMin && property.yearBuilt < searchFilters.value.yearBuiltMin) {
        return false
      }
      
      if (searchFilters.value.yearBuiltMax && property.yearBuilt > searchFilters.value.yearBuiltMax) {
        return false
      }
      
      return true
    })
  })

  // Actions
  async function fetchProperties(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/properties', { params })
      properties.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch properties'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchPropertyById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/properties/${id}`)
      currentProperty.value = response.data
      
      // Add to recently viewed
      addToRecentlyViewed(response.data)
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || `Failed to fetch property with ID: ${id}`
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function searchProperties(query) {
    loading.value = true
    error.value = null
    searchResults.value = []
    
    try {
      const response = await axios.get('/api/properties/search', { 
        params: { 
          query,
          ...searchFilters.value
        } 
      })
      searchResults.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Search failed'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function searchByCoordinates(lat, lng, radius = 0.5) {
    loading.value = true
    error.value = null
    searchResults.value = []
    
    try {
      const response = await axios.get('/api/properties/search/coordinates', { 
        params: { 
          latitude: lat,
          longitude: lng,
          radius,
          ...searchFilters.value
        } 
      })
      searchResults.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Location search failed'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  function updateSearchFilters(filters) {
    searchFilters.value = { ...searchFilters.value, ...filters }
  }

  function resetSearchFilters() {
    searchFilters.value = {
      propertyType: [],
      minValue: 0,
      maxValue: null,
      minBedrooms: null,
      maxBedrooms: null,
      minBathrooms: null,
      maxBathrooms: null,
      yearBuiltMin: null,
      yearBuiltMax: null,
      dataSources: ['county-records', 'tax-assessor', 'census'],
      sortBy: 'relevance'
    }
  }

  async function saveSearch(searchName, searchQuery, filters) {
    try {
      const response = await axios.post('/api/saved-searches', {
        name: searchName,
        query: searchQuery,
        filters: filters || searchFilters.value
      })
      
      savedSearches.value.push(response.data)
      toast.success('Search saved successfully')
      return response.data
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to save search'
      toast.error(errorMsg)
      throw errorMsg
    }
  }

  async function fetchSavedSearches() {
    try {
      const response = await axios.get('/api/saved-searches')
      savedSearches.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch saved searches:', err)
      return []
    }
  }

  async function deleteSavedSearch(id) {
    try {
      await axios.delete(`/api/saved-searches/${id}`)
      savedSearches.value = savedSearches.value.filter(search => search.id !== id)
      toast.success('Search deleted successfully')
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to delete saved search'
      toast.error(errorMsg)
      throw errorMsg
    }
  }

  function addToRecentlyViewed(property) {
    // Remove if already exists
    recentlyViewed.value = recentlyViewed.value.filter(p => p.id !== property.id)
    
    // Add to beginning of array
    recentlyViewed.value.unshift(property)
    
    // Keep only the last 10 items
    if (recentlyViewed.value.length > 10) {
      recentlyViewed.value = recentlyViewed.value.slice(0, 10)
    }
    
    // Save to localStorage
    try {
      localStorage.setItem('recentlyViewedProperties', JSON.stringify(recentlyViewed.value))
    } catch (e) {
      console.error('Failed to save recently viewed properties to localStorage:', e)
    }
  }

  function loadRecentlyViewed() {
    try {
      const saved = localStorage.getItem('recentlyViewedProperties')
      if (saved) {
        recentlyViewed.value = JSON.parse(saved)
      }
    } catch (e) {
      console.error('Failed to load recently viewed properties from localStorage:', e)
    }
  }

  // Initialize recently viewed properties
  loadRecentlyViewed()

  return {
    // State
    properties,
    currentProperty,
    loading,
    error,
    searchResults,
    searchFilters,
    savedSearches,
    recentlyViewed,
    
    // Getters
    filteredProperties,
    
    // Actions
    fetchProperties,
    fetchPropertyById,
    searchProperties,
    searchByCoordinates,
    updateSearchFilters,
    resetSearchFilters,
    saveSearch,
    fetchSavedSearches,
    deleteSavedSearch,
    addToRecentlyViewed
  }
})