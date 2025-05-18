<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <h1>Forgot Password</h1>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
      
      <div v-if="emailSent" class="success-message">
        <p>Password reset instructions have been sent to your email.</p>
        <p>Please check your inbox and follow the instructions to reset your password.</p>
        <div class="form-actions">
          <router-link to="/login" class="btn-primary">Return to Login</router-link>
        </div>
      </div>
      
      <form v-else @submit.prevent="resetPassword" class="forgot-password-form">
        <p class="form-description">
          Enter your email address and we'll send you instructions to reset your password.
        </p>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            autocomplete="email"
          />
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="btn-primary" 
            :disabled="authStore.loading"
          >
            {{ authStore.loading ? 'Sending...' : 'Send Reset Instructions' }}
          </button>
        </div>
      </form>
      
      <div class="forgot-password-footer">
        <p>Remember your password? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const email = ref('')
const emailSent = ref(false)

function resetPassword() {
  authStore.forgotPassword(email.value)
    .then(() => {
      emailSent.value = true
    })
    .catch(() => {
      // Error is handled by the store and displayed via authStore.error
    })
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.forgot-password-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

.form-description {
  text-align: center;
  color: #666;
  margin-bottom: 20px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

.forgot-password-form {
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
  display: block;
  text-align: center;
  text-decoration: none;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.forgot-password-footer {
  text-align: center;
  color: #666;
}

.forgot-password-footer a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
}
</style>