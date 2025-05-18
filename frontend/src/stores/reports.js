import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useReportsStore = defineStore('reports', () => {
  // State
  const reports = ref([])
  const currentReport = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()

  // Getters
  const userReports = computed(() => {
    return reports.value.filter(report => report.isUserGenerated)
  })

  const systemReports = computed(() => {
    return reports.value.filter(report => !report.isUserGenerated)
  })

  // Actions
  async function fetchReports(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/reports', { params })
      reports.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch reports'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchReportById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/reports/${id}`)
      currentReport.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || `Failed to fetch report with ID: ${id}`
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function createReport(reportData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/reports', reportData)
      reports.value.push(response.data)
      toast.success('Report created successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateReport(id, reportData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`/api/reports/${id}`, reportData)
      
      // Update the report in the reports array
      const index = reports.value.findIndex(report => report.id === id)
      if (index !== -1) {
        reports.value[index] = response.data
      }
      
      // Update current report if it's the one being edited
      if (currentReport.value && currentReport.value.id === id) {
        currentReport.value = response.data
      }
      
      toast.success('Report updated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function deleteReport(id) {
    loading.value = true
    error.value = null
    
    try {
      await axios.delete(`/api/reports/${id}`)
      
      // Remove the report from the reports array
      reports.value = reports.value.filter(report => report.id !== id)
      
      // Clear current report if it's the one being deleted
      if (currentReport.value && currentReport.value.id === id) {
        currentReport.value = null
      }
      
      toast.success('Report deleted successfully')
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function generateReport(reportType, parameters) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/reports/generate', {
        report_type: reportType,
        parameters
      })
      
      toast.success('Report generated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to generate report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function exportReport(id, format = 'pdf') {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/reports/${id}/export`, {
        params: { format },
        responseType: 'blob'
      })
      
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `report-${id}.${format}`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      toast.success(`Report exported as ${format.toUpperCase()}`)
    } catch (err) {
      error.value = 'Failed to export report'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    reports,
    currentReport,
    loading,
    error,
    
    // Getters
    userReports,
    systemReports,
    
    // Actions
    fetchReports,
    fetchReportById,
    createReport,
    updateReport,
    deleteReport,
    generateReport,
    exportReport
  }
})