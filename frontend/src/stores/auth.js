import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '../router'
import { useToast } from 'vue-toastification'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)
  const toast = useToast()

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userRole = computed(() => user.value?.role || 'guest')
  const userName = computed(() => user.value?.name || '')
  const userEmail = computed(() => user.value?.email || '')
  const userCompany = computed(() => user.value?.company || null)

  // Actions
  async function login(credentials) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/login', credentials)
      
      if (response.data.access_token) {
        token.value = response.data.access_token
        localStorage.setItem('token', token.value)
        
        // Set authorization header for future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        
        // Get user profile
        await fetchUserProfile()
        
        // Redirect to dashboard or requested page
        const redirectPath = router.currentRoute.value.query.redirect || '/dashboard'
        router.push(redirectPath)
        
        toast.success('Login successful')
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
      toast.error(error.value)
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/register', userData)
      
      if (response.data.message) {
        toast.success('Registration successful. Please check your email for verification.')
        router.push('/login')
      }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
      toast.error(error.value)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      // Call logout endpoint to invalidate token on server
      await axios.post('/api/auth/logout')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of server response
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      
      // Redirect to login page
      router.push('/login')
      toast.info('You have been logged out')
    }
  }

  async function fetchUserProfile() {
    if (!token.value) return
    
    try {
      const response = await axios.get('/api/users/me')
      user.value = response.data
    } catch (err) {
      console.error('Error fetching user profile:', err)
      
      // If unauthorized, logout
      if (err.response?.status === 401) {
        logout()
      }
    }
  }

  async function forgotPassword(email) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/forgot-password', { email })
      toast.success('Password reset instructions sent to your email')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to process password reset request'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function resetPassword(token, newPassword) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/reset-password', { 
        token, 
        new_password: newPassword 
      })
      toast.success('Password has been reset successfully')
      router.push('/login')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to reset password'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(profileData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put('/api/users/me', profileData)
      user.value = response.data
      toast.success('Profile updated successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update profile'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function changePassword(passwordData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/auth/change-password', passwordData)
      toast.success('Password changed successfully')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to change password'
      toast.error(error.value)
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Initialize auth state
  function init() {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      fetchUserProfile()
    }
  }

  // Call init when store is created
  init()

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    isAdmin,
    userRole,
    userName,
    userEmail,
    userCompany,
    
    // Actions
    login,
    register,
    logout,
    fetchUserProfile,
    forgotPassword,
    resetPassword,
    updateProfile,
    changePassword
  }
})