<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="credentials.email" 
            required 
            autocomplete="email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password" 
            required 
            autocomplete="current-password"
          />
        </div>
        
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="credentials.remember" />
            <span>Remember me</span>
          </label>
          
          <router-link to="/forgot-password" class="forgot-password">
            Forgot password?
          </router-link>
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="btn-primary" 
            :disabled="authStore.loading"
          >
            {{ authStore.loading ? 'Logging in...' : 'Login' }}
          </button>
        </div>
      </form>
      
      <div class="login-footer">
        <p>Don't have an account? <router-link to="/register">Register</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

const credentials = ref({
  email: '',
  password: '',
  remember: false
})

function login() {
  authStore.login(credentials.value)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
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

.login-form {
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.remember-me input {
  margin-right: 5px;
}

.forgot-password {
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

.login-footer {
  text-align: center;
  color: #666;
}

.login-footer a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
}
</style>