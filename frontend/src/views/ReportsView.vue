<template>
  <div class="reports-container">
    <h1>Reports</h1>
    
    <div class="reports-tabs">
      <button 
        :class="{ active: activeTab === 'my-reports' }" 
        @click="activeTab = 'my-reports'"
      >
        My Reports
      </button>
      <button 
        :class="{ active: activeTab === 'system-reports' }" 
        @click="activeTab = 'system-reports'"
      >
        System Reports
      </button>
      <button 
        :class="{ active: activeTab === 'generate' }" 
        @click="activeTab = 'generate'"
      >
        Generate Report
      </button>
    </div>
    
    <div class="tab-content">
      <!-- My Reports Tab -->
      <div v-if="activeTab === 'my-reports'" class="my-reports">
        <div v-if="loading" class="loading">
          <p>Loading your reports...</p>
        </div>
        
        <div v-else-if="userReports.length === 0" class="no-reports">
          <p>You haven't created any reports yet.</p>
          <button @click="activeTab = 'generate'" class="btn-primary">Create Your First Report</button>
        </div>
        
        <div v-else class="reports-list">
          <div 
            v-for="report in userReports" 
            :key="report.id" 
            class="report-card"
          >
            <div class="report-header">
              <h3>{{ report.title }}</h3>
              <span class="report-date">{{ formatDate(report.created_at) }}</span>
            </div>
            <p class="report-description">{{ report.description }}</p>
            <div class="report-actions">
              <button @click="viewReport(report.id)" class="btn-secondary">View</button>
              <button @click="exportReport(report.id)" class="btn-secondary">Export</button>
              <button @click="deleteReport(report.id)" class="btn-danger">Delete</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- System Reports Tab -->
      <div v-if="activeTab === 'system-reports'" class="system-reports">
        <div v-if="loading" class="loading">
          <p>Loading system reports...</p>
        </div>
        
        <div v-else-if="systemReports.length === 0" class="no-reports">
          <p>No system reports available.</p>
        </div>
        
        <div v-else class="reports-list">
          <div 
            v-for="report in systemReports" 
            :key="report.id" 
            class="report-card"
          >
            <div class="report-header">
              <h3>{{ report.title }}</h3>
              <span class="report-date">{{ formatDate(report.created_at) }}</span>
            </div>
            <p class="report-description">{{ report.description }}</p>
            <div class="report-actions">
              <button @click="viewReport(report.id)" class="btn-secondary">View</button>
              <button @click="exportReport(report.id)" class="btn-secondary">Export</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Generate Report Tab -->
      <div v-if="activeTab === 'generate'" class="generate-report">
        <h2>Generate New Report</h2>
        
        <div class="report-form">
          <div class="form-group">
            <label for="reportType">Report Type</label>
            <select id="reportType" v-model="newReport.type">
              <option value="property-analysis">Property Analysis</option>
              <option value="owner-portfolio">Owner Portfolio</option>
              <option value="market-trends">Market Trends</option>
              <option value="wealth-distribution">Wealth Distribution</option>
              <option value="custom">Custom Report</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="reportTitle">Report Title</label>
            <input type="text" id="reportTitle" v-model="newReport.title" placeholder="Enter report title" />
          </div>
          
          <div class="form-group">
            <label for="reportDescription">Description</label>
            <textarea id="reportDescription" v-model="newReport.description" placeholder="Enter report description"></textarea>
          </div>
          
          <div class="form-actions">
            <button @click="generateReport" class="btn-primary" :disabled="loading">
              {{ loading ? 'Generating...' : 'Generate Report' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useReportsStore } from '../stores/reports'

const reportsStore = useReportsStore()
const activeTab = ref('my-reports')
const loading = computed(() => reportsStore.loading)
const error = computed(() => reportsStore.error)

const userReports = computed(() => reportsStore.userReports)
const systemReports = computed(() => reportsStore.systemReports)

const newReport = ref({
  type: 'property-analysis',
  title: '',
  description: '',
  parameters: {}
})

onMounted(() => {
  // Fetch reports when component is mounted
  reportsStore.fetchReports()
})

function viewReport(id) {
  reportsStore.fetchReportById(id)
    .then(report => {
      // Handle viewing the report
      console.log('Viewing report:', report)
    })
}

function exportReport(id) {
  reportsStore.exportReport(id, 'pdf')
}

function deleteReport(id) {
  if (confirm('Are you sure you want to delete this report?')) {
    reportsStore.deleteReport(id)
  }
}

function generateReport() {
  const reportData = {
    title: newReport.value.title,
    description: newReport.value.description,
    report_type: newReport.value.type,
    parameters: newReport.value.parameters
  }
  
  reportsStore.createReport(reportData)
    .then(() => {
      // Reset form and switch to my reports tab
      newReport.value = {
        type: 'property-analysis',
        title: '',
        description: '',
        parameters: {}
      }
      activeTab.value = 'my-reports'
    })
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<style scoped>
.reports-container {
  padding: 20px;
}

.reports-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.reports-tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 3px solid transparent;
}

.reports-tabs button.active {
  border-bottom-color: #4CAF50;
  font-weight: bold;
}

.report-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fff;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.report-header h3 {
  margin: 0;
}

.report-date {
  color: #666;
  font-size: 14px;
}

.report-description {
  margin-bottom: 15px;
  color: #333;
}

.report-actions {
  display: flex;
  gap: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group textarea {
  min-height: 100px;
}

.form-actions {
  margin-top: 20px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-danger {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.loading, .no-reports {
  text-align: center;
  padding: 40px 0;
}
</style>