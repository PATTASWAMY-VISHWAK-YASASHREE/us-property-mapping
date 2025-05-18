import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useAdminStore = defineStore('admin', () => {
  // State
  const systemStats = ref({})
  const activityLogs = ref([])
  const systemSettings = ref({})
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()

  // Getters
  const userCount = computed(() => systemStats.value.userCount || 0)
  const propertyCount = computed(() => systemStats.value.propertyCount || 0)
  const ownerCount = computed(() => systemStats.value.ownerCount || 0)
  const searchCount = computed(() => systemStats.value.searchCount || 0)
  const recentActivity = computed(() => activityLogs.value.slice(0, 10))

  // Actions
  async function fetchSystemStats() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/stats')
      systemStats.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch system statistics'
      console.error(error.value)
      return {}
    } finally {
      loading.value = false
    }
  }

  async function fetchActivityLogs(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/activity-logs', { params })
      activityLogs.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch activity logs'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchSystemSettings() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/settings')
      systemSettings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch system settings'
      console.error(error.value)
      return {}
    } finally {
      loading.value = false
    }
  }

  async function updateSystemSettings(settings) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put('/api/admin/settings', settings)
      systemSettings.value = response.data
      toast.success('System settings updated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update system settings'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function runDatabaseMaintenance() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/admin/maintenance/database')
      toast.success('Database maintenance completed successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to run database maintenance'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function clearCache() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/admin/maintenance/clear-cache')
      toast.success('Cache cleared successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to clear cache'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function generateSystemReport() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/admin/reports/system')
      toast.success('System report generated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to generate system report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchApiUsageStats(timeframe = 'daily') {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/stats/api-usage', {
        params: { timeframe }
      })
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch API usage statistics'
      console.error(error.value)
      return []
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    systemStats,
    activityLogs,
    systemSettings,
    loading,
    error,
    
    // Getters
    userCount,
    propertyCount,
    ownerCount,
    searchCount,
    recentActivity,
    
    // Actions
    fetchSystemStats,
    fetchActivityLogs,
    fetchSystemSettings,
    updateSystemSettings,
    runDatabaseMaintenance,
    clearCache,
    generateSystemReport,
    fetchApiUsageStats
  }
})