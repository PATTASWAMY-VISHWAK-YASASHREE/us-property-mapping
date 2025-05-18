<template>
  <div class="admin-container">
    <h1>Admin Dashboard</h1>
    
    <div class="stats-cards">
      <div class="stat-card">
        <h3>Users</h3>
        <div class="stat-value">{{ adminStore.userCount }}</div>
        <div class="stat-link">
          <router-link to="/admin/users">Manage Users</router-link>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>Properties</h3>
        <div class="stat-value">{{ adminStore.propertyCount }}</div>
        <div class="stat-link">
          <router-link to="/admin/properties">Manage Properties</router-link>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>Owners</h3>
        <div class="stat-value">{{ adminStore.ownerCount }}</div>
        <div class="stat-link">
          <router-link to="/admin/owners">Manage Owners</router-link>
        </div>
      </div>
      
      <div class="stat-card">
        <h3>Searches</h3>
        <div class="stat-value">{{ adminStore.searchCount }}</div>
        <div class="stat-link">
          <router-link to="/admin/search-analytics">View Analytics</router-link>
        </div>
      </div>
    </div>
    
    <div class="admin-sections">
      <div class="admin-section">
        <h2>Recent Activity</h2>
        <div v-if="adminStore.loading" class="loading">
          <p>Loading activity logs...</p>
        </div>
        <div v-else class="activity-table">
          <table>
            <thead>
              <tr>
                <th>User</th>
                <th>Action</th>
                <th>Resource</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(activity, index) in adminStore.recentActivity" :key="index">
                <td>{{ activity.user_email || activity.user_id }}</td>
                <td>{{ activity.action }}</td>
                <td>{{ activity.resource_type }}: {{ activity.resource_id }}</td>
                <td>{{ formatDate(activity.timestamp) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="view-all">
            <button @click="viewAllActivity" class="btn-secondary">View All Activity</button>
          </div>
        </div>
      </div>
      
      <div class="admin-section">
        <h2>System Maintenance</h2>
        <div class="maintenance-actions">
          <div class="maintenance-card">
            <h3>Database Maintenance</h3>
            <p>Run optimization routines on the database</p>
            <button @click="runDatabaseMaintenance" class="btn-primary" :disabled="adminStore.loading">
              {{ adminStore.loading ? 'Running...' : 'Run Maintenance' }}
            </button>
          </div>
          
          <div class="maintenance-card">
            <h3>Clear Cache</h3>
            <p>Clear application cache to refresh data</p>
            <button @click="clearCache" class="btn-primary" :disabled="adminStore.loading">
              {{ adminStore.loading ? 'Clearing...' : 'Clear Cache' }}
            </button>
          </div>
          
          <div class="maintenance-card">
            <h3>System Report</h3>
            <p>Generate a comprehensive system report</p>
            <button @click="generateSystemReport" class="btn-primary" :disabled="adminStore.loading">
              {{ adminStore.loading ? 'Generating...' : 'Generate Report' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="admin-section">
      <h2>API Usage</h2>
      <div class="api-usage-controls">
        <div class="timeframe-selector">
          <label>Timeframe:</label>
          <select v-model="apiTimeframe">
            <option value="hourly">Hourly</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
      </div>
      <div class="api-usage-chart">
        <!-- Chart would go here in a real implementation -->
        <div class="chart-placeholder">
          <p>API Usage Chart ({{ apiTimeframe }})</p>
          <div class="mock-chart">
            <div class="chart-bar" v-for="(value, index) in mockChartData" :key="index" :style="{ height: value + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'

const router = useRouter()
const adminStore = useAdminStore()

const apiTimeframe = ref('daily')
const mockChartData = ref([25, 40, 30, 50, 65, 45, 35, 55, 70, 60])

onMounted(() => {
  // Fetch admin dashboard data
  adminStore.fetchSystemStats()
  adminStore.fetchActivityLogs({ limit: 10 })
})

function viewAllActivity() {
  router.push('/admin/activity-logs')
}

function runDatabaseMaintenance() {
  adminStore.runDatabaseMaintenance()
    .then(() => {
      // Refresh stats after maintenance
      adminStore.fetchSystemStats()
    })
}

function clearCache() {
  adminStore.clearCache()
}

function generateSystemReport() {
  adminStore.generateSystemReport()
    .then(report => {
      // Handle the generated report
      console.log('System report generated:', report)
    })
}

function formatDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<style scoped>
.admin-container {
  padding: 20px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  margin-top: 0;
  color: #666;
  font-size: 16px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin: 10px 0;
  color: #2c3e50;
}

.stat-link {
  margin-top: 10px;
}

.stat-link a {
  color: #4CAF50;
  text-decoration: none;
}

.admin-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.admin-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
}

.activity-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.view-all {
  margin-top: 15px;
  text-align: center;
}

.maintenance-actions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.maintenance-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #eee;
}

.maintenance-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.maintenance-card p {
  margin-bottom: 15px;
  color: #666;
}

.api-usage-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

.timeframe-selector {
  display: flex;
  align-items: center;
}

.timeframe-selector label {
  margin-right: 10px;
}

.chart-placeholder {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  height: 300px;
  display: flex;
  flex-direction: column;
}

.mock-chart {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  margin-top: 20px;
}

.chart-bar {
  width: 30px;
  background-color: #4CAF50;
  border-radius: 4px 4px 0 0;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>