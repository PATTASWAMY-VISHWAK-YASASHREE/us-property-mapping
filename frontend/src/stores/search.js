import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useSearchStore = defineStore('search', () => {
  // State
  const searchResults = ref({
    properties: [],
    owners: [],
    companies: []
  })
  const searchHistory = ref([])
  const loading = ref(false)
  const error = ref(null)
  const searchFilters = ref({
    types: ['properties', 'owners', 'companies'],
    minValue: null,
    maxValue: null,
    sortBy: 'relevance',
    sortOrder: 'desc',
    limit: 50
  })
  const toast = useToast()

  // Getters
  const hasResults = computed(() => {
    return searchResults.value.properties.length > 0 || 
           searchResults.value.owners.length > 0 || 
           searchResults.value.companies.length > 0
  })

  const totalResults = computed(() => {
    return searchResults.value.properties.length + 
           searchResults.value.owners.length + 
           searchResults.value.companies.length
  })

  // Actions
  async function search(query, filters = {}) {
    loading.value = true
    error.value = null
    
    // Merge provided filters with default filters
    const mergedFilters = { ...searchFilters.value, ...filters }
    
    try {
      const response = await axios.get('/api/search', { 
        params: { 
          query,
          ...mergedFilters
        } 
      })
      
      searchResults.value = response.data
      
      // Add to search history
      addToSearchHistory(query, mergedFilters)
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Search failed'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function advancedSearch(searchParams) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/search/advanced', searchParams)
      searchResults.value = response.data
      
      // Add to search history
      addToSearchHistory(searchParams.query || 'Advanced Search', searchParams)
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Advanced search failed'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function searchByLocation(location) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/search/location', { 
        params: { 
          location,
          ...searchFilters.value
        } 
      })
      
      searchResults.value = response.data
      
      // Add to search history
      addToSearchHistory(`Location: ${location}`, searchFilters.value)
      
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
      types: ['properties', 'owners', 'companies'],
      minValue: null,
      maxValue: null,
      sortBy: 'relevance',
      sortOrder: 'desc',
      limit: 50
    }
  }

  function addToSearchHistory(query, filters) {
    // Create a search history entry
    const historyEntry = {
      id: Date.now(),
      query,
      filters: { ...filters },
      timestamp: new Date().toISOString()
    }
    
    // Add to beginning of array
    searchHistory.value.unshift(historyEntry)
    
    // Keep only the last 20 searches
    if (searchHistory.value.length > 20) {
      searchHistory.value = searchHistory.value.slice(0, 20)
    }
    
    // Save to localStorage
    try {
      localStorage.setItem('searchHistory', JSON.stringify(searchHistory.value))
    } catch (e) {
      console.error('Failed to save search history to localStorage:', e)
    }
  }

  function loadSearchHistory() {
    try {
      const saved = localStorage.getItem('searchHistory')
      if (saved) {
        searchHistory.value = JSON.parse(saved)
      }
    } catch (e) {
      console.error('Failed to load search history from localStorage:', e)
    }
  }

  function clearSearchHistory() {
    searchHistory.value = []
    try {
      localStorage.removeItem('searchHistory')
    } catch (e) {
      console.error('Failed to clear search history from localStorage:', e)
    }
  }

  // Initialize search history
  loadSearchHistory()

  return {
    // State
    searchResults,
    searchHistory,
    loading,
    error,
    searchFilters,
    
    // Getters
    hasResults,
    totalResults,
    
    // Actions
    search,
    advancedSearch,
    searchByLocation,
    updateSearchFilters,
    resetSearchFilters,
    addToSearchHistory,
    clearSearchHistory
  }
})