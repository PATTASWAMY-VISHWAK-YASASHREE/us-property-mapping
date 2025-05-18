<template>
  <div class="user-management">
    <h1>User Management</h1>
    
    <div class="actions-bar">
      <button @click="showCreateUserModal = true" class="btn-primary">Add New User</button>
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search users..." 
          @input="searchUsers"
        />
      </div>
    </div>
    
    <div v-if="usersStore.loading" class="loading">
      <p>Loading users...</p>
    </div>
    
    <div v-else class="users-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in usersStore.users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span :class="['status-badge', user.isActive ? 'active' : 'inactive']">
                {{ user.isActive ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editUser(user)" class="btn-icon">Edit</button>
              <button 
                v-if="user.isActive" 
                @click="deactivateUser(user.id)" 
                class="btn-icon danger"
              >
                Deactivate
              </button>
              <button 
                v-else 
                @click="activateUser(user.id)" 
                class="btn-icon success"
              >
                Activate
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUsersStore } from '../../stores/users'

const usersStore = useUsersStore()
const searchQuery = ref('')
const showCreateUserModal = ref(false)
const currentUser = ref(null)

onMounted(() => {
  usersStore.fetchUsers()
})

function searchUsers() {
  // Implement search functionality
  console.log('Searching for:', searchQuery.value)
}

function editUser(user) {
  currentUser.value = user
  // Open edit modal or navigate to edit page
  console.log('Editing user:', user)
}

function activateUser(userId) {
  usersStore.activateUser(userId)
}

function deactivateUser(userId) {
  usersStore.deactivateUser(userId)
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-box input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 250px;
}

.users-table {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-badge.inactive {
  background-color: #ffebee;
  color: #c62828;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-icon {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-icon.danger {
  background-color: #ffebee;
  border-color: #ffcdd2;
  color: #c62828;
}

.btn-icon.success {
  background-color: #e8f5e9;
  border-color: #c8e6c9;
  color: #2e7d32;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>