<template>
  <div class="transaction-records">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Transaction Records</h2>
    
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="spinner"></div>
    </div>
    
    <div v-else-if="transactions && transactions.length > 0">
      <!-- Transaction Summary -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Transaction Summary</h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Total Transactions:</span>
              <span class="font-medium">{{ transactions.length }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">First Transaction:</span>
              <span class="font-medium">{{ formatDate(firstTransactionDate) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Last Transaction:</span>
              <span class="font-medium">{{ formatDate(lastTransactionDate) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Average Price:</span>
              <span class="font-medium">${{ formatCurrency(averageTransactionAmount) }}</span>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Price History</h3>
          <div class="h-40 flex items-center justify-center">
            <!-- Price history chart would go here -->
            <span class="text-gray-500">Price history chart</span>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Transaction Types</h3>
          <div class="space-y-2">
            <div v-for="(count, type) in transactionTypeCount" :key="type" class="flex justify-between">
              <span class="text-gray-600">{{ formatTransactionType(type) }}:</span>
              <span class="font-medium">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Transaction Timeline -->
      <div class="mb-8">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Transaction Timeline</h3>
        
        <div class="relative">
          <!-- Vertical line -->
          <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-blue-200"></div>
          
          <!-- Timeline items -->
          <div 
            v-for="(transaction, index) in sortedTransactions" 
            :key="index"
            class="relative pl-12 pb-8"
          >
            <!-- Timeline dot -->
            <div 
              class="absolute left-0 top-1 w-8 h-8 rounded-full flex items-center justify-center text-white"
              :class="getTransactionTypeColor(transaction.transaction_type)"
            >
              <span class="text-xs">{{ getTransactionTypeIcon(transaction.transaction_type) }}</span>
            </div>
            
            <!-- Timeline content -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div class="flex flex-col md:flex-row md:justify-between md:items-center">
                <div>
                  <h4 class="text-lg font-semibold text-gray-800">
                    {{ formatTransactionType(transaction.transaction_type) }}
                  </h4>
                  <p class="text-gray-600">{{ formatDate(transaction.transaction_date) }}</p>
                </div>
                <div class="mt-2 md:mt-0">
                  <span class="inline-block bg-green-100 text-green-800 text-lg font-medium px-2.5 py-0.5 rounded">
                    ${{ formatCurrency(transaction.amount) }}
                  </span>
                </div>
              </div>
              
              <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="transaction.seller">
                  <p class="text-sm text-gray-500">Seller</p>
                  <p class="font-medium">{{ transaction.seller.name }}</p>
                </div>
                
                <div v-if="transaction.buyer">
                  <p class="text-sm text-gray-500">Buyer</p>
                  <p class="font-medium">{{ transaction.buyer.name }}</p>
                </div>
              </div>
              
              <div class="mt-3" v-if="transaction.description">
                <p class="text-sm text-gray-500">Description</p>
                <p class="text-gray-700">{{ transaction.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Transaction Table -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200">
          <thead>
            <tr>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Date</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Type</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Amount</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Seller</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Buyer</th>
              <th class="py-3 px-4 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Description</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(transaction, index) in sortedTransactions" :key="`table-${index}`">
              <td class="py-3 px-4 text-sm">{{ formatDate(transaction.transaction_date) }}</td>
              <td class="py-3 px-4 text-sm">
                <span 
                  class="inline-block px-2 py-1 text-xs font-medium rounded"
                  :class="getTransactionTypeBadgeClass(transaction.transaction_type)"
                >
                  {{ formatTransactionType(transaction.transaction_type) }}
                </span>
              </td>
              <td class="py-3 px-4 text-sm font-medium">${{ formatCurrency(transaction.amount) }}</td>
              <td class="py-3 px-4 text-sm">{{ transaction.seller ? transaction.seller.name : 'N/A' }}</td>
              <td class="py-3 px-4 text-sm">{{ transaction.buyer ? transaction.buyer.name : 'N/A' }}</td>
              <td class="py-3 px-4 text-sm">{{ transaction.description || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else class="bg-gray-50 p-6 rounded-lg text-center">
      <p class="text-gray-500">No transaction records available for this property.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  propertyId: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  transactions: {
    type: Array,
    default: () => []
  }
})

// Sort transactions by date (newest first)
const sortedTransactions = computed(() => {
  if (!props.transactions || props.transactions.length === 0) return []
  
  return [...props.transactions].sort((a, b) => {
    return new Date(b.transaction_date) - new Date(a.transaction_date)
  })
})

// Get first transaction date
const firstTransactionDate = computed(() => {
  if (!props.transactions || props.transactions.length === 0) return null
  
  const dates = props.transactions.map(t => new Date(t.transaction_date))
  return new Date(Math.min(...dates))
})

// Get last transaction date
const lastTransactionDate = computed(() => {
  if (!props.transactions || props.transactions.length === 0) return null
  
  const dates = props.transactions.map(t => new Date(t.transaction_date))
  return new Date(Math.max(...dates))
})

// Calculate average transaction amount
const averageTransactionAmount = computed(() => {
  if (!props.transactions || props.transactions.length === 0) return 0
  
  const total = props.transactions.reduce((sum, transaction) => sum + Number(transaction.amount), 0)
  return total / props.transactions.length
})

// Count transaction types
const transactionTypeCount = computed(() => {
  if (!props.transactions || props.transactions.length === 0) return {}
  
  return props.transactions.reduce((counts, transaction) => {
    const type = transaction.transaction_type
    counts[type] = (counts[type] || 0) + 1
    return counts
  }, {})
})

// Format dates
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

// Format currency values
const formatCurrency = (value) => {
  if (!value) return 'N/A'
  
  return new Intl.NumberFormat('en-US', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Format transaction type
const formatTransactionType = (type) => {
  if (!type) return 'Unknown'
  
  const typeMap = {
    'sale': 'Sale',
    'refinance': 'Refinance',
    'transfer': 'Transfer',
    'foreclosure': 'Foreclosure',
    'tax_lien': 'Tax Lien',
    'construction': 'Construction',
    'renovation': 'Renovation'
  }
  
  return typeMap[type.toLowerCase()] || type
}

// Get transaction type color
const getTransactionTypeColor = (type) => {
  if (!type) return 'bg-gray-500'
  
  const colorMap = {
    'sale': 'bg-green-500',
    'refinance': 'bg-blue-500',
    'transfer': 'bg-purple-500',
    'foreclosure': 'bg-red-500',
    'tax_lien': 'bg-yellow-500',
    'construction': 'bg-indigo-500',
    'renovation': 'bg-pink-500'
  }
  
  return colorMap[type.toLowerCase()] || 'bg-gray-500'
}

// Get transaction type badge class
const getTransactionTypeBadgeClass = (type) => {
  if (!type) return 'bg-gray-100 text-gray-800'
  
  const classMap = {
    'sale': 'bg-green-100 text-green-800',
    'refinance': 'bg-blue-100 text-blue-800',
    'transfer': 'bg-purple-100 text-purple-800',
    'foreclosure': 'bg-red-100 text-red-800',
    'tax_lien': 'bg-yellow-100 text-yellow-800',
    'construction': 'bg-indigo-100 text-indigo-800',
    'renovation': 'bg-pink-100 text-pink-800'
  }
  
  return classMap[type.toLowerCase()] || 'bg-gray-100 text-gray-800'
}

// Get transaction type icon
const getTransactionTypeIcon = (type) => {
  if (!type) return '?'
  
  const iconMap = {
    'sale': '$',
    'refinance': 'R',
    'transfer': 'T',
    'foreclosure': 'F',
    'tax_lien': 'L',
    'construction': 'C',
    'renovation': 'R'
  }
  
  return iconMap[type.toLowerCase()] || '?'
}
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #4a6cf7;
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