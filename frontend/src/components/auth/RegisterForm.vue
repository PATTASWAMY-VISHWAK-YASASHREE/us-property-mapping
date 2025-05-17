<template>
  <div class="register-form">
    <h2>Create Account</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input 
          type="text" 
          id="firstName" 
          v-model="firstName" 
          required 
          placeholder="Enter your first name"
        />
      </div>
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input 
          type="text" 
          id="lastName" 
          v-model="lastName" 
          required 
          placeholder="Enter your last name"
        />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          required 
          placeholder="Enter your email"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          required 
          placeholder="Create a password"
        />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input 
          type="password" 
          id="confirmPassword" 
          v-model="confirmPassword" 
          required 
          placeholder="Confirm your password"
        />
      </div>
      <div class="form-group checkbox">
        <input type="checkbox" id="terms" v-model="termsAccepted" required />
        <label for="terms">I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/privacy" target="_blank">Privacy Policy</a></label>
      </div>
      <div class="form-actions">
        <button type="submit" :disabled="isLoading || !isFormValid">
          {{ isLoading ? 'Creating Account...' : 'Register' }}
        </button>
        <div class="login-link">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const termsAccepted = ref(false);
const error = ref('');
const isLoading = ref(false);

const isFormValid = computed(() => {
  return firstName.value && 
         lastName.value && 
         email.value && 
         password.value && 
         confirmPassword.value && 
         password.value === confirmPassword.value &&
         termsAccepted.value;
});

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match';
    return;
  }

  try {
    isLoading.value = true;
    error.value = '';
    
    await authStore.register({
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value
    });
    
    router.push('/verify-email');
  } catch (err) {
    error.value = err.message || 'Failed to register. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox input {
  width: auto;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.checkbox label {
  margin-bottom: 0;
  font-weight: normal;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 1.5rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4a6cf7;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3a5ce5;
}

button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.875rem;
}

.login-link a {
  color: #4a6cf7;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.error-message {
  color: #e53e3e;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
}

a {
  color: #4a6cf7;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>