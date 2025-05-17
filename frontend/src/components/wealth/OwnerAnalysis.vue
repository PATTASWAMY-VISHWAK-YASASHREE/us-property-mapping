<template>
  <div class="owner-analysis">
    <h2 class="text-2xl font-bold mb-6">Owner Analysis</h2>
    
    <!-- Owner Profile Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 class="text-xl font-semibold mb-4">Owner Profile</h3>
      <div v-if="loading" class="flex justify-center">
        <div class="spinner"></div>
      </div>
      <div v-else-if="!currentOwner" class="text-gray-500">
        Select an owner to view their profile
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div class="flex items-center mb-4">
            <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mr-4">
              <span class="text-2xl font-bold">{{ ownerInitials }}</span>
            </div>
            <div>
              <h4 class="text-lg font-semibold">{{ currentOwner.name }}</h4>
              <p class="text-gray-600">{{ currentOwner.type || 'Individual' }}</p>
            </div>
          </div>
          <div class="space-y-2">
            <p v-if="currentOwner.address"><span class="font-medium">Address:</span> {{ currentOwner.address }}</p>
            <p v-if="currentOwner.email"><span class="font-medium">Email:</span> {{ currentOwner.email }}</p>
            <p v-if="currentOwner.phone"><span class="font-medium">Phone:</span> {{ currentOwner.phone }}</p>
            <p v-if="currentOwner.taxId"><span class="font-medium">Tax ID:</span> {{ currentOwner.taxId }}</p>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded-lg">
          <h4 class="font-semibold mb-2">Financial Summary</h4>
          <div class="space-y-2">
            <p><span class="font-medium">Net Worth:</span> {{ formatCurrency(currentOwner.netWorth) }}</p>
            <p><span class="font-medium">Total Property Value:</span> {{ formatCurrency(totalPropertyValue) }}</p>
            <p><span class="font-medium">Properties Owned:</span> {{ ownerProperties.length }}</p>
            <p v-if="currentOwner.lastUpdated"><span class="font-medium">Last Updated:</span> {{ formatDate(currentOwner.lastUpdated) }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Wealth Data Visualization Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 class="text-xl font-semibold mb-4">Wealth Data Visualization</h3>
      <div v-if="loading" class="flex justify-center">
        <div class="spinner"></div>
      </div>
      <div v-else-if="!currentOwner" class="text-gray-500">
        Select an owner to view wealth data
      </div>
      <div v-else>
        <div class="flex mb-4 space-x-4">
          <button 
            v-for="period in ['1Y', '3Y', '5Y', 'All']" 
            :key="period"
            @click="changeTimeframe(period)"
            :class="[
              'px-3 py-1 rounded',
              selectedTimeframe === period ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
            ]"
          >
            {{ period }}
          </button>
        </div>
        
        <div class="h-64 mb-6">
          <!-- Wealth trend chart will be rendered here -->
          <div ref="wealthChartRef" class="w-full h-full"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-gray-50 p-4 rounded-lg">
            <h5 class="font-medium text-gray-600">Real Estate</h5>
            <p class="text-xl font-semibold">{{ formatCurrency(wealthBreakdown.realEstate) }}</p>
            <p class="text-sm text-gray-500">{{ calculatePercentage(wealthBreakdown.realEstate) }}% of total</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg">
            <h5 class="font-medium text-gray-600">Investments</h5>
            <p class="text-xl font-semibold">{{ formatCurrency(wealthBreakdown.investments) }}</p>
            <p class="text-sm text-gray-500">{{ calculatePercentage(wealthBreakdown.investments) }}% of total</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg">
            <h5 class="font-medium text-gray-600">Business Assets</h5>
            <p class="text-xl font-semibold">{{ formatCurrency(wealthBreakdown.businessAssets) }}</p>
            <p class="text-sm text-gray-500">{{ calculatePercentage(wealthBreakdown.businessAssets) }}% of total</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg">
            <h5 class="font-medium text-gray-600">Other Assets</h5>
            <p class="text-xl font-semibold">{{ formatCurrency(wealthBreakdown.otherAssets) }}</p>
            <p class="text-sm text-gray-500">{{ calculatePercentage(wealthBreakdown.otherAssets) }}% of total</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Property Portfolio Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 class="text-xl font-semibold mb-4">Property Portfolio</h3>
      <div v-if="loading" class="flex justify-center">
        <div class="spinner"></div>
      </div>
      <div v-else-if="!currentOwner || !ownerProperties.length" class="text-gray-500">
        No properties found for this owner
      </div>
      <div v-else>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Address</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acquisition Date</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="property in ownerProperties" :key="property.id">
                <td class="px-6 py-4 whitespace-nowrap">{{ property.address }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ property.type }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(property.value) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(property.acquisitionDate) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <router-link :to="`/property/${property.id}`" class="text-blue-600 hover:text-blue-900">View</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="mt-6">
          <h4 class="font-semibold mb-3">Portfolio Distribution</h4>
          <div class="h-64">
            <!-- Property distribution chart will be rendered here -->
            <div ref="portfolioChartRef" class="w-full h-full"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Relationship Mapping Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 class="text-xl font-semibold mb-4">Relationship Mapping</h3>
      <div v-if="loading" class="flex justify-center">
        <div class="spinner"></div>
      </div>
      <div v-else-if="!currentOwner" class="text-gray-500">
        Select an owner to view relationships
      </div>
      <div v-else>
        <div class="mb-4">
          <div class="flex justify-between items-center mb-2">
            <h4 class="font-semibold">Connected Entities</h4>
            <div class="flex space-x-2">
              <button 
                v-for="type in ['All', 'Business', 'Personal']" 
                :key="type"
                @click="filterRelationships(type)"
                :class="[
                  'px-3 py-1 text-sm rounded',
                  relationshipFilter === type ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
                ]"
              >
                {{ type }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="h-96 border border-gray-200 rounded-lg mb-4">
          <!-- Relationship network graph will be rendered here -->
          <div ref="relationshipGraphRef" class="w-full h-full"></div>
        </div>
        
        <div v-if="relatedEntities.length" class="mt-4">
          <h4 class="font-semibold mb-2">Related Entities</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="entity in relatedEntities" 
              :key="entity.id"
              class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h5 class="font-medium">{{ entity.name }}</h5>
                  <p class="text-sm text-gray-600">{{ entity.type }}</p>
                </div>
                <span class="text-xs bg-gray-200 px-2 py-1 rounded-full">{{ entity.relationshipType }}</span>
              </div>
              <p v-if="entity.description" class="text-sm mt-2">{{ entity.description }}</p>
              <div class="mt-2 flex justify-end">
                <button 
                  @click="viewEntityDetails(entity.id)"
                  class="text-sm text-blue-600 hover:text-blue-800"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useWealthStore } from '../../stores/wealth'
import { Chart, registerables } from 'chart.js'
import * as d3 from 'd3'

// Register Chart.js components
Chart.register(...registerables)

// Initialize stores and route
const wealthStore = useWealthStore()
const route = useRoute()

// Reactive references
const wealthChartRef = ref(null)
const portfolioChartRef = ref(null)
const relationshipGraphRef = ref(null)
const wealthChart = ref(null)
const portfolioChart = ref(null)
const selectedTimeframe = ref('1Y')
const relationshipFilter = ref('All')
const relatedEntities = ref([])
const wealthBreakdown = ref({
  realEstate: 0,
  investments: 0,
  businessAssets: 0,
  otherAssets: 0
})

// Computed properties
const currentOwner = computed(() => wealthStore.currentOwner)
const ownerProperties = computed(() => wealthStore.ownerProperties)
const totalPropertyValue = computed(() => wealthStore.totalPropertyValue)
const loading = computed(() => wealthStore.loading)

const ownerInitials = computed(() => {
  if (!currentOwner.value || !currentOwner.value.name) return ''
  
  return currentOwner.value.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
})

// Methods
function formatCurrency(value) {
  if (!value) return '$0'
  
  // Handle string values with currency symbols
  if (typeof value === 'string') {
    value = parseFloat(value.replace(/[^0-9.-]+/g, ''))
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function calculatePercentage(value) {
  const total = Object.values(wealthBreakdown.value).reduce((sum, val) => sum + val, 0)
  if (total === 0 || !value) return 0
  
  return Math.round((value / total) * 100)
}

async function changeTimeframe(period) {
  selectedTimeframe.value = period
  
  if (!currentOwner.value) return
  
  let timeframe
  switch (period) {
    case '1Y': timeframe = 'yearly'; break
    case '3Y': timeframe = '3years'; break
    case '5Y': timeframe = '5years'; break
    case 'All': timeframe = 'all'; break
    default: timeframe = 'yearly'
  }
  
  const trendsData = await wealthStore.fetchWealthTrends(currentOwner.value.id, timeframe)
  renderWealthChart(trendsData)
}

function renderWealthChart(trendsData) {
  if (!wealthChartRef.value) return
  
  // Destroy existing chart if it exists
  if (wealthChart.value) {
    wealthChart.value.destroy()
  }
  
  const ctx = wealthChartRef.value.getContext('2d')
  
  // Prepare data for chart
  const labels = trendsData.map(item => item.date)
  const netWorthData = trendsData.map(item => item.netWorth)
  const propertyValueData = trendsData.map(item => item.propertyValue)
  
  wealthChart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Net Worth',
          data: netWorthData,
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'Property Value',
          data: propertyValueData,
          borderColor: 'rgba(153, 102, 255, 1)',
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ${formatCurrency(context.raw)}`
            }
          }
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return formatCurrency(value)
            }
          }
        }
      }
    }
  })
}

function renderPortfolioChart() {
  if (!portfolioChartRef.value || !ownerProperties.value.length) return
  
  // Destroy existing chart if it exists
  if (portfolioChart.value) {
    portfolioChart.value.destroy()
  }
  
  const ctx = portfolioChartRef.value.getContext('2d')
  
  // Group properties by type and calculate total value for each type
  const propertyTypes = {}
  ownerProperties.value.forEach(property => {
    const type = property.type || 'Other'
    const value = parseFloat(property.value?.replace(/[^0-9.-]+/g, '') || 0)
    
    if (!propertyTypes[type]) {
      propertyTypes[type] = 0
    }
    propertyTypes[type] += value
  })
  
  // Prepare data for chart
  const labels = Object.keys(propertyTypes)
  const data = Object.values(propertyTypes)
  
  // Generate colors
  const backgroundColors = [
    'rgba(255, 99, 132, 0.6)',
    'rgba(54, 162, 235, 0.6)',
    'rgba(255, 206, 86, 0.6)',
    'rgba(75, 192, 192, 0.6)',
    'rgba(153, 102, 255, 0.6)',
    'rgba(255, 159, 64, 0.6)'
  ]
  
  portfolioChart.value = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: backgroundColors.slice(0, labels.length),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = Math.round((value / total) * 100)
              return `${context.label}: ${formatCurrency(value)} (${percentage}%)`
            }
          }
        },
        legend: {
          position: 'right'
        }
      }
    }
  })
}

async function filterRelationships(type) {
  relationshipFilter.value = type
  
  if (!currentOwner.value) return
  
  // Filter related entities based on type
  if (type !== 'All') {
    relatedEntities.value = relatedEntities.value.filter(entity => 
      entity.relationshipType.toLowerCase().includes(type.toLowerCase())
    )
  } else {
    // Reload all relationships
    await loadRelationships()
  }
  
  renderRelationshipGraph()
}

async function loadRelationships() {
  if (!currentOwner.value) return
  
  try {
    const data = await wealthStore.fetchRelatedOwners(currentOwner.value.id)
    relatedEntities.value = data
  } catch (error) {
    console.error('Failed to load relationships:', error)
    relatedEntities.value = []
  }
}

function renderRelationshipGraph() {
  if (!relationshipGraphRef.value || !currentOwner.value || !relatedEntities.value.length) return
  
  // Clear previous graph
  d3.select(relationshipGraphRef.value).selectAll('*').remove()
  
  const width = relationshipGraphRef.value.clientWidth
  const height = relationshipGraphRef.value.clientHeight
  
  // Create SVG
  const svg = d3.select(relationshipGraphRef.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
  
  // Prepare data for force-directed graph
  const nodes = [
    { id: currentOwner.value.id, name: currentOwner.value.name, type: 'central', group: 0 },
    ...relatedEntities.value.map((entity, i) => ({
      id: entity.id,
      name: entity.name,
      type: entity.type,
      group: entity.relationshipType === 'Business' ? 1 : 2
    }))
  ]
  
  const links = relatedEntities.value.map(entity => ({
    source: currentOwner.value.id,
    target: entity.id,
    type: entity.relationshipType
  }))
  
  // Create force simulation
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
  
  // Create links
  const link = svg.append('g')
    .selectAll('line')
    .data(links)
    .enter()
    .append('line')
    .attr('stroke-width', 2)
    .attr('stroke', d => d.type === 'Business' ? '#4299e1' : '#ed64a6')
  
  // Create nodes
  const node = svg.append('g')
    .selectAll('circle')
    .data(nodes)
    .enter()
    .append('circle')
    .attr('r', d => d.type === 'central' ? 15 : 10)
    .attr('fill', d => {
      if (d.type === 'central') return '#3182ce'
      return d.group === 1 ? '#4299e1' : '#ed64a6'
    })
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended)
    )
  
  // Add labels
  const label = svg.append('g')
    .selectAll('text')
    .data(nodes)
    .enter()
    .append('text')
    .text(d => d.name)
    .attr('font-size', 12)
    .attr('dx', 15)
    .attr('dy', 4)
  
  // Update positions on simulation tick
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
    
    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
    
    label
      .attr('x', d => d.x)
      .attr('y', d => d.y)
  })
  
  // Drag functions
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
  }
  
  function dragged(event) {
    event.subject.fx = event.x
    event.subject.fy = event.y
  }
  
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0)
    event.subject.fx = null
    event.subject.fy = null
  }
}

function viewEntityDetails(entityId) {
  // Navigate to the owner view for the selected entity
  if (entityId) {
    window.location.href = `/owner/${entityId}`
  }
}

async function loadOwnerData(ownerId) {
  if (!ownerId) return
  
  try {
    // Load owner data
    await wealthStore.fetchOwnerById(ownerId)
    
    // Load wealth data
    const wealthData = await wealthStore.fetchWealthData(ownerId)
    if (wealthData) {
      wealthBreakdown.value = {
        realEstate: wealthData.realEstate || 0,
        investments: wealthData.investments || 0,
        businessAssets: wealthData.businessAssets || 0,
        otherAssets: wealthData.otherAssets || 0
      }
    }
    
    // Load wealth trends
    const trendsData = await wealthStore.fetchWealthTrends(ownerId, 'yearly')
    renderWealthChart(trendsData)
    
    // Load relationships
    await loadRelationships()
    renderRelationshipGraph()
    
    // Render portfolio chart
    renderPortfolioChart()
  } catch (error) {
    console.error('Error loading owner data:', error)
  }
}

// Watch for route changes to load data for different owners
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      loadOwnerData(newId)
    }
  }
)

// Initialize component
onMounted(() => {
  const ownerId = route.params.id
  if (ownerId) {
    loadOwnerData(ownerId)
  }
})
</script>

<style scoped>
.owner-analysis {
  padding: 1rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #3182ce;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>