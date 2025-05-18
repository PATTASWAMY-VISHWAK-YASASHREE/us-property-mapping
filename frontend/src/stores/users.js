import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useAuthStore } from './auth'

export const useUsersStore = defineStore('users', () => {
  // State
  const users = ref([])
  const currentUser = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()
  const authStore = useAuthStore()

  // Getters
  const activeUsers = computed(() => {
    return users.value.filter(user => user.isActive)
  })

  const adminUsers = computed(() => {
    return users.value.filter(user => user.role === 'admin')
  })

  // Actions
  async function fetchUsers(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/users', { params })
      users.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch users'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchUserById(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`/api/users/${id}`)
      currentUser.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || `Failed to fetch user with ID: ${id}`
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function createUser(userData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/users', userData)
      users.value.push(response.data)
      toast.success('User created successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create user'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateUser(id, userData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`/api/users/${id}`, userData)
      
      // Update the user in the users array
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      
      // Update current user if it's the one being edited
      if (currentUser.value && currentUser.value.id === id) {
        currentUser.value = response.data
      }
      
      // Update auth store user if it's the current logged in user
      if (authStore.user && authStore.user.id === id) {
        authStore.user = response.data
      }
      
      toast.success('User updated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update user'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function deleteUser(id) {
    loading.value = true
    error.value = null
    
    try {
      await axios.delete(`/api/users/${id}`)
      
      // Remove the user from the users array
      users.value = users.value.filter(user => user.id !== id)
      
      // Clear current user if it's the one being deleted
      if (currentUser.value && currentUser.value.id === id) {
        currentUser.value = null
      }
      
      toast.success('User deleted successfully')
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete user'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateUserRole(id, role) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.patch(`/api/users/${id}/role`, { role })
      
      // Update the user in the users array
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      
      // Update current user if it's the one being edited
      if (currentUser.value && currentUser.value.id === id) {
        currentUser.value = response.data
      }
      
      toast.success(`User role updated to ${role}`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update user role'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function activateUser(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.patch(`/api/users/${id}/activate`)
      
      // Update the user in the users array
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      
      toast.success('User activated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to activate user'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function deactivateUser(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.patch(`/api/users/${id}/deactivate`)
      
      // Update the user in the users array
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      
      toast.success('User deactivated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to deactivate user'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    users,
    currentUser,
    loading,
    error,
    
    // Getters
    activeUsers,
    adminUsers,
    
    // Actions
    fetchUsers,
    fetchUserById,
    createUser,
    updateUser,
    deleteUser,
    updateUserRole,
    activateUser,
    deactivateUser
  }
})