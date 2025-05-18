<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    
    <div class="profile-tabs">
      <button 
        :class="{ active: activeTab === 'profile' }" 
        @click="activeTab = 'profile'"
      >
        Profile Information
      </button>
      <button 
        :class="{ active: activeTab === 'security' }" 
        @click="activeTab = 'security'"
      >
        Security Settings
      </button>
      <button 
        :class="{ active: activeTab === 'activity' }" 
        @click="activeTab = 'activity'"
      >
        Recent Activity
      </button>
    </div>
    
    <div class="tab-content">
      <!-- Profile Information Tab -->
      <div v-if="activeTab === 'profile'" class="profile-info">
        <div v-if="loading" class="loading">
          <p>Loading profile information...</p>
        </div>
        
        <div v-else class="profile-form">
          <div class="form-group">
            <label for="name">Full Name</label>
            <input type="text" id="name" v-model="profileData.name" />
          </div>
          
          <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" v-model="profileData.email" disabled />
            <small>Email address cannot be changed</small>
          </div>
          
          <div class="form-group">
            <label for="phone">Phone Number</label>
            <input type="tel" id="phone" v-model="profileData.phone" />
          </div>
          
          <div class="form-group">
            <label for="company">Company</label>
            <input type="text" id="company" v-model="profileData.company" />
          </div>
          
          <div class="form-group">
            <label for="jobTitle">Job Title</label>
            <input type="text" id="jobTitle" v-model="profileData.jobTitle" />
          </div>
          
          <div class="form-actions">
            <button @click="updateProfile" class="btn-primary" :disabled="loading">
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Security Settings Tab -->
      <div v-if="activeTab === 'security'" class="security-settings">
        <h2>Change Password</h2>
        
        <div class="password-form">
          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input type="password" id="currentPassword" v-model="passwordData.currentPassword" />
          </div>
          
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input type="password" id="newPassword" v-model="passwordData.newPassword" />
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <input type="password" id="confirmPassword" v-model="passwordData.confirmPassword" />
          </div>
          
          <div class="form-actions">
            <button @click="changePassword" class="btn-primary" :disabled="loading || !passwordsValid">
              {{ loading ? 'Changing...' : 'Change Password' }}
            </button>
          </div>
          
          <div v-if="passwordError" class="error-message">
            {{ passwordError }}
          </div>
        </div>
        
        <div class="security-options">
          <h2>Security Options</h2>
          
          <div class="option-item">
            <div class="option-label">
              <h3>Two-Factor Authentication</h3>
              <p>Add an extra layer of security to your account</p>
            </div>
            <div class="option-control">
              <button class="btn-secondary">Setup 2FA</button>
            </div>
          </div>
          
          <div class="option-item">
            <div class="option-label">
              <h3>Login Sessions</h3>
              <p>Manage your active login sessions</p>
            </div>
            <div class="option-control">
              <button class="btn-secondary">View Sessions</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Recent Activity Tab -->
      <div v-if="activeTab === 'activity'" class="activity-log">
        <h2>Your Recent Activity</h2>
        
        <div v-if="loading" class="loading">
          <p>Loading activity...</p>
        </div>
        
        <div v-else-if="activityLog.length === 0" class="no-activity">
          <p>No recent activity to display.</p>
        </div>
        
        <div v-else class="activity-list">
          <div v-for="(activity, index) in activityLog" :key="index" class="activity-item">
            <div class="activity-icon" :class="activity.type">
              <i class="icon"></i>
            </div>
            <div class="activity-details">
              <p class="activity-description">{{ activity.description }}</p>
              <p class="activity-time">{{ formatDate(activity.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useUsersStore } from '../stores/users'

const authStore = useAuthStore()
const usersStore = useUsersStore()

const activeTab = ref('profile')
const loading = computed(() => authStore.loading || usersStore.loading)
const error = computed(() => authStore.error || usersStore.error)

const profileData = ref({
  name: '',
  email: '',
  phone: '',
  company: '',
  jobTitle: ''
})

const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordError = ref('')
const activityLog = ref([])

const passwordsValid = computed(() => {
  if (!passwordData.value.currentPassword || 
      !passwordData.value.newPassword || 
      !passwordData.value.confirmPassword) {
    return false
  }
  
  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    passwordError.value = 'New passwords do not match'
    return false
  }
  
  if (passwordData.value.newPassword.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return false
  }
  
  passwordError.value = ''
  return true
})

onMounted(() => {
  // Load user profile data
  if (authStore.user) {
    profileData.value = {
      name: authStore.user.name || '',
      email: authStore.user.email || '',
      phone: authStore.user.phone || '',
      company: authStore.user.company || '',
      jobTitle: authStore.user.job_title || ''
    }
  } else {
    // Fetch user profile if not already loaded
    authStore.fetchUserProfile()
      .then(user => {
        if (user) {
          profileData.value = {
            name: user.name || '',
            email: user.email || '',
            phone: user.phone || '',
            company: user.company || '',
            jobTitle: user.job_title || ''
          }
        }
      })
  }
  
  // Load activity log (mock data for now)
  fetchActivityLog()
})

function updateProfile() {
  authStore.updateProfile({
    name: profileData.value.name,
    phone: profileData.value.phone,
    company: profileData.value.company,
    job_title: profileData.value.jobTitle
  })
}

function changePassword() {
  if (!passwordsValid.value) return
  
  authStore.changePassword({
    current_password: passwordData.value.currentPassword,
    new_password: passwordData.value.newPassword
  })
    .then(() => {
      // Reset password fields
      passwordData.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    })
}

function fetchActivityLog() {
  // Mock activity data - in a real app, this would come from an API
  activityLog.value = [
    {
      type: 'login',
      description: 'Logged in from Chrome on Windows',
      timestamp: new Date(Date.now() - 1000 * 60 * 5) // 5 minutes ago
    },
    {
      type: 'search',
      description: 'Searched for "luxury properties in Miami"',
      timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
    },
    {
      type: 'view',
      description: 'Viewed property at 123 Ocean Drive',
      timestamp: new Date(Date.now() - 1000 * 60 * 45) // 45 minutes ago
    },
    {
      type: 'report',
      description: 'Generated market trends report',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
    },
    {
      type: 'login',
      description: 'Logged in from Safari on macOS',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24) // 1 day ago
    }
  ]
}

function formatDate(date) {
  if (!date) return ''
  
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffMins < 60) {
    return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  } else if (diffHours < 24) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  } else if (diffDays < 7) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  } else {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.profile-tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 3px solid transparent;
}

.profile-tabs button.active {
  border-bottom-color: #4CAF50;
  font-weight: bold;
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

.form-actions {
  margin-top: 30px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.error-message {
  color: #f44336;
  margin-top: 10px;
}

.security-options {
  margin-top: 40px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.option-label h3 {
  margin: 0 0 5px 0;
}

.option-label p {
  margin: 0;
  color: #666;
}

.activity-list {
  margin-top: 20px;
}

.activity-item {
  display: flex;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.activity-icon.login {
  background-color: #2196F3;
}

.activity-icon.search {
  background-color: #FF9800;
}

.activity-icon.view {
  background-color: #9C27B0;
}

.activity-icon.report {
  background-color: #4CAF50;
}

.activity-details {
  flex: 1;
}

.activity-description {
  margin: 0 0 5px 0;
}

.activity-time {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.loading, .no-activity {
  text-align: center;
  padding: 40px 0;
  color: #666;
}
</style>