<template>
  <div class="company-management">
    <h1>Company Management</h1>
    
    <div class="actions-bar">
      <button @click="showCreateCompanyModal = true" class="btn-primary">Add New Company</button>
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search companies..." 
          @input="searchCompanies"
        />
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Loading companies...</p>
    </div>
    
    <div v-else class="companies-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Industry</th>
            <th>Properties</th>
            <th>Users</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.name }}</td>
            <td>{{ company.industry }}</td>
            <td>{{ company.properties_count || 0 }}</td>
            <td>{{ company.users_count || 0 }}</td>
            <td>
              <span :class="['status-badge', company.isActive ? 'active' : 'inactive']">
                {{ company.isActive ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editCompany(company)" class="btn-icon">Edit</button>
              <button @click="viewCompanyDetails(company.id)" class="btn-icon">Details</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// In a real implementation, we would have a companies store
// For now, we'll use mock data
const loading = ref(false)
const searchQuery = ref('')
const showCreateCompanyModal = ref(false)
const currentCompany = ref(null)

// Mock companies data
const companies = ref([
  {
    id: 1,
    name: 'Acme Real Estate',
    industry: 'Real Estate',
    properties_count: 120,
    users_count: 15,
    isActive: true
  },
  {
    id: 2,
    name: 'Globex Properties',
    industry: 'Property Management',
    properties_count: 85,
    users_count: 8,
    isActive: true
  },
  {
    id: 3,
    name: 'Initech Investments',
    industry: 'Investment',
    properties_count: 210,
    users_count: 22,
    isActive: true
  },
  {
    id: 4,
    name: 'Umbrella Holdings',
    industry: 'Real Estate Development',
    properties_count: 45,
    users_count: 5,
    isActive: false
  }
])

onMounted(() => {
  // Simulate loading
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
})

function searchCompanies() {
  // Implement search functionality
  console.log('Searching for:', searchQuery.value)
}

function editCompany(company) {
  currentCompany.value = company
  // Open edit modal or navigate to edit page
  console.log('Editing company:', company)
}

function viewCompanyDetails(companyId) {
  // Navigate to company details page
  console.log('Viewing company details:', companyId)
}
</script>

<style scoped>
.company-management {
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

.companies-table {
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

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>