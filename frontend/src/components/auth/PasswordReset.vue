<template>
  <div class="password-reset">
    <div v-if="!token">
      <!-- Request Password Reset Form -->
      <h2>Reset Your Password</h2>
      <p class="description">Enter your email address and we'll send you a link to reset your password.</p>
      
      <form @submit.prevent="requestReset" v-if="!requestSent">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="Enter your email"
          />
        </div>
        <div class="form-actions">
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? 'Sending...' : 'Send Reset Link' }}
          </button>
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
      
      <div v-else class="success-message">
        <div class="success-icon">✓</div>
        <h3>Reset Link Sent</h3>
        <p>We've sent a password reset link to <strong>{{ email }}</strong>. Please check your email and follow the instructions to reset your password.</p>
        <p class="note">If you don't see the email in your inbox, please check your spam folder.</p>
        <button @click="resetForm" class="btn-secondary">
          Send Another Link
        </button>
      </div>
    </div>
    
    <div v-else>
      <!-- Set New Password Form -->
      <h2>Create New Password</h2>
      <p class="description">Please enter your new password below.</p>
      
      <form @submit.prevent="setNewPassword" v-if="!resetComplete">
        <div class="form-group">
          <label for="password">New Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="Enter new password"
          />
          <div class="password-strength" v-if="password">
            <div class="strength-meter">
              <div 
                class="strength-value" 
                :style="{ width: `${passwordStrength.score * 25}%` }"
                :class="passwordStrength.className"
              ></div>
            </div>
            <span class="strength-text" :class="passwordStrength.className">
              {{ passwordStrength.text }}
            </span>
          </div>
          <ul class="password-requirements">
            <li :class="{ met: hasMinLength }">At least 8 characters</li>
            <li :class="{ met: hasUpperCase }">At least one uppercase letter</li>
            <li :class="{ met: hasLowerCase }">At least one lowercase letter</li>
            <li :class="{ met: hasNumber }">At least one number</li>
            <li :class="{ met: hasSpecialChar }">At least one special character</li>
          </ul>
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm New Password</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required 
            placeholder="Confirm new password"
          />
          <div v-if="passwordMismatch" class="password-mismatch">
            Passwords do not match
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" :disabled="isLoading || !isPasswordValid || passwordMismatch">
            {{ isLoading ? 'Updating...' : 'Update Password' }}
          </button>
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
      
      <div v-else class="success-message">
        <div class="success-icon">✓</div>
        <h3>Password Updated Successfully</h3>
        <p>Your password has been updated. You can now log in with your new password.</p>
        <button @click="goToLogin" class="btn-primary">
          Go to Login
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Form state
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const isLoading = ref(false);
const requestSent = ref(false);
const resetComplete = ref(false);
const token = ref('');

// Password validation
const hasMinLength = computed(() => password.value.length >= 8);
const hasUpperCase = computed(() => /[A-Z]/.test(password.value));
const hasLowerCase = computed(() => /[a-z]/.test(password.value));
const hasNumber = computed(() => /[0-9]/.test(password.value));
const hasSpecialChar = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(password.value));

const isPasswordValid = computed(() => 
  hasMinLength.value && 
  hasUpperCase.value && 
  hasLowerCase.value && 
  hasNumber.value && 
  hasSpecialChar.value
);

const passwordMismatch = computed(() => 
  confirmPassword.value && password.value !== confirmPassword.value
);

const passwordStrength = computed(() => {
  if (!password.value) {
    return { score: 0, text: '', className: '' };
  }
  
  let score = 0;
  if (hasMinLength.value) score++;
  if (hasUpperCase.value) score++;
  if (hasLowerCase.value) score++;
  if (hasNumber.value) score++;
  if (hasSpecialChar.value) score++;
  
  const strengthMap = {
    0: { text: 'Very Weak', className: 'very-weak' },
    1: { text: 'Weak', className: 'weak' },
    2: { text: 'Fair', className: 'fair' },
    3: { text: 'Good', className: 'good' },
    4: { text: 'Strong', className: 'strong' },
    5: { text: 'Very Strong', className: 'very-strong' }
  };
  
  return { 
    score, 
    text: strengthMap[score].text, 
    className: strengthMap[score].className 
  };
});

onMounted(() => {
  // Check if there's a token in the URL
  if (route.query.token) {
    token.value = route.query.token;
    // In a real app, you would validate the token here
  }
});

// Request password reset
const requestReset = async () => {
  try {
    isLoading.value = true;
    error.value = '';
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // In a real app, you would call your API here
    // await requestPasswordReset(email.value);
    
    requestSent.value = true;
  } catch (err) {
    error.value = err.message || 'Failed to send reset link. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Set new password
const setNewPassword = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match';
    return;
  }
  
  if (!isPasswordValid.value) {
    error.value = 'Please ensure your password meets all requirements';
    return;
  }
  
  try {
    isLoading.value = true;
    error.value = '';
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // In a real app, you would call your API here
    // await resetPassword({ token: token.value, password: password.value });
    
    resetComplete.value = true;
  } catch (err) {
    error.value = err.message || 'Failed to reset password. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Reset the form to request another link
const resetForm = () => {
  email.value = '';
  requestSent.value = false;
  error.value = '';
};

// Navigate to login page
const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.password-reset {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

.description {
  text-align: center;
  margin-bottom: 2rem;
  color: #666;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 2rem;
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

.btn-secondary {
  background-color: #718096;
}

.btn-secondary:hover {
  background-color: #4a5568;
}

.error-message {
  color: #e53e3e;
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fed7d7;
  border-radius: 4px;
  text-align: center;
}

.success-message {
  text-align: center;
}

.success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background-color: #48bb78;
  color: white;
  font-size: 2rem;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
}

.note {
  font-size: 0.875rem;
  color: #718096;
  margin: 1rem 0;
}

.password-strength {
  margin-top: 0.5rem;
}

.strength-meter {
  height: 4px;
  background-color: #edf2f7;
  border-radius: 2px;
  margin-bottom: 0.25rem;
}

.strength-value {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s;
}

.strength-text {
  font-size: 0.75rem;
}

.very-weak { background-color: #e53e3e; color: #e53e3e; }
.weak { background-color: #ed8936; color: #ed8936; }
.fair { background-color: #ecc94b; color: #ecc94b; }
.good { background-color: #48bb78; color: #48bb78; }
.strong { background-color: #38a169; color: #38a169; }
.very-strong { background-color: #2f855a; color: #2f855a; }

.password-requirements {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
  font-size: 0.875rem;
  color: #718096;
}

.password-requirements li {
  margin-bottom: 0.25rem;
  position: relative;
  padding-left: 1.5rem;
}

.password-requirements li:before {
  content: "✕";
  position: absolute;
  left: 0;
  color: #e53e3e;
}

.password-requirements li.met:before {
  content: "✓";
  color: #48bb78;
}

.password-mismatch {
  color: #e53e3e;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>