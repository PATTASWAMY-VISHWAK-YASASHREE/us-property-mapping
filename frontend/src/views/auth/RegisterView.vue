<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Create Account</h1>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
      
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input 
            type="text" 
            id="name" 
            v-model="userData.name" 
            required 
            autocomplete="name"
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="userData.email" 
            required 
            autocomplete="email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="userData.password" 
            required 
            autocomplete="new-password"
          />
          <small>Password must be at least 8 characters long</small>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="userData.confirmPassword" 
            required 
            autocomplete="new-password"
          />
        </div>
        
        <div class="form-group">
          <label for="company">Company (Optional)</label>
          <input 
            type="text" 
            id="company" 
            v-model="userData.company" 
            autocomplete="organization"
          />
        </div>
        
        <div class="form-options">
          <label class="terms-checkbox">
            <input type="checkbox" v-model="userData.agreeTerms" required />
            <span>I agree to the <a href="#" @click.prevent="showTerms">Terms and Conditions</a></span>
          </label>
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="btn-primary" 
            :disabled="authStore.loading || !isFormValid"
          >
            {{ authStore.loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </div>
      </form>
      
      <div class="register-footer">
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const toast = useToast()

const userData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  company: '',
  agreeTerms: false
})

const isFormValid = computed(() => {
  return userData.value.name && 
         userData.value.email && 
         userData.value.password && 
         userData.value.password === userData.value.confirmPassword &&
         userData.value.password.length >= 8 &&
         userData.value.agreeTerms
})

function register() {
  if (!isFormValid.value) {
    if (userData.value.password !== userData.value.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }
    
    if (userData.value.password.length < 8) {
      toast.error('Password must be at least 8 characters long')
      return
    }
    
    toast.error('Please fill in all required fields')
    return
  }
  
  // Prepare data for API
  const registerData = {
    name: userData.value.name,
    email: userData.value.email,
    password: userData.value.password,
    company: userData.value.company || undefined
  }
  
  authStore.register(registerData)
}

function showTerms() {
  toast.info('Terms and Conditions would be displayed here')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.register-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 500px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

.register-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-group small {
  display: block;
  color: #666;
  margin-top: 5px;
}

.form-options {
  margin-bottom: 20px;
}

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
}

.terms-checkbox input {
  margin-right: 8px;
  margin-top: 4px;
}

.terms-checkbox a {
  color: #4CAF50;
  text-decoration: none;
}

.form-actions {
  margin-bottom: 20px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  color: #666;
}

.register-footer a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
}
</style>