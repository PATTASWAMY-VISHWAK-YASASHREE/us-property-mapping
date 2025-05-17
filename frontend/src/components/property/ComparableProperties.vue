<template>
  <div class="comparable-properties">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Comparable Properties</h2>
    
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="spinner"></div>
    </div>
    
    <div v-else-if="comparables && comparables.length > 0">
      <!-- Comparison Summary -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">Comparison Summary</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p class="text-sm text-gray-500">Average Price</p>
            <p class="text-xl font-semibold">${{ formatCurrency(averagePrice) }}</p>
            <p class="text-sm" :class="priceComparisonClass">
              {{ priceComparison }}
            </p>
          </div>
          
          <div>
            <p class="text-sm text-gray-500">Average Size</p>
            <p class="text-xl font-semibold">{{ formatNumber(averageSize) }} sq ft</p>
            <p class="text-sm" :class="sizeComparisonClass">
              {{ sizeComparison }}
            </p>
          </div>
          
          <div>
            <p class="text-sm text-gray-500">Average Price/sq ft</p>
            <p class="text-xl font-semibold">${{ formatCurrency(averagePricePerSqFt) }}</p>
            <p class="text-sm" :class="pricePerSqFtComparisonClass">
              {{ pricePerSqFtComparison }}
            </p>
          </div>
          
          <div>
            <p class="text-sm text-gray-500">Distance Range</p>
            <p class="text-xl font-semibold">{{ minDistance }} - {{ maxDistance }} mi</p>
            <p class="text-sm text-gray-500">{{ comparables.length }} properties</p>
          </div>
        </div>
      </div>
      
      <!-- Comparable Properties Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="(property, index) in comparables" 
          :key="index"
          class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
        >
          <!-- Property Image -->
          <div class="h-48 overflow-hidden">
            <img 
              v-if="property.imageUrl" 
              :src="property.imageUrl" 
              :alt="property.address"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center">
              <span class="text-gray-500">No image</span>
            </div>
          </div>
          
          <!-- Property Details -->
          <div class="p-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-1">{{ property.address }}</h4>
            <p class="text-gray-600 mb-3">{{ property.city }}, {{ property.state }} {{ property.zip_code }}</p>
            
            <div class="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p class="text-sm text-gray-500">Price</p>
                <p class="font-medium">${{ formatCurrency(property.price) }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Distance</p>
                <p class="font-medium">{{ property.distance }} mi</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Size</p>
                <p class="font-medium">{{ formatNumber(property.square_feet) }} sq ft</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Price/sq ft</p>
                <p class="font-medium">${{ calculatePricePerSqFt(property) }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Beds</p>
                <p class="font-medium">{{ property.bedrooms }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">Baths</p>
                <p class="font-medium">{{ property.bathrooms }}</p>
              </div>
            </div>
            
            <div class="flex justify-between items-center">
              <span 
                class="inline-block px-2 py-1 text-xs font-medium rounded"
                :class="getSimilarityClass(property.similarity_score)"
              >
                {{ getSimilarityLabel(property.similarity_score) }}
              </span>
              
              <button 
                @click="viewProperty(property.id)"
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Map View -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Map View</h3>
        <div class="h-96 bg-gray-200 rounded-lg">
          <!-- Map component would go here -->
          <div class="w-full h-full flex items-center justify-center">
            <span class="text-gray-500">Map loading...</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="bg-gray-50 p-6 rounded-lg text-center">
      <p class="text-gray-500">No comparable properties available for this property.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  propertyId: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  comparables: {
    type: Array,
    default: () => []
  },
  currentProperty: {
    type: Object,
    default: () => ({})
  }
})

const router = useRouter()

// Calculate average price of comparable properties
const averagePrice = computed(() => {
  if (!props.comparables || props.comparables.length === 0) return 0
  
  const total = props.comparables.reduce((sum, property) => sum + Number(property.price), 0)
  return total / props.comparables.length
})

// Calculate average size of comparable properties
const averageSize = computed(() => {
  if (!props.comparables || props.comparables.length === 0) return 0
  
  const total = props.comparables.reduce((sum, property) => sum + Number(property.square_feet), 0)
  return total / props.comparables.length
})

// Calculate average price per square foot
const averagePricePerSqFt = computed(() => {
  if (!props.comparables || props.comparables.length === 0) return 0
  
  const pricesPerSqFt = props.comparables.map(property => 
    Number(property.price) / Number(property.square_feet)
  )
  
  const total = pricesPerSqFt.reduce((sum, price) => sum + price, 0)
  return total / pricesPerSqFt.length
})

// Calculate min and max distances
const minDistance = computed(() => {
  if (!props.comparables || props.comparables.length === 0) return 0
  
  return Math.min(...props.comparables.map(p => p.distance))
})

const maxDistance = computed(() => {
  if (!props.comparables || props.comparables.length === 0) return 0
  
  return Math.max(...props.comparables.map(p => p.distance))
})

// Compare current property to comparables
const priceComparison = computed(() => {
  if (!props.currentProperty || !props.currentProperty.current_value) return ''
  
  const diff = props.currentProperty.current_value - averagePrice.value
  const percentage = (diff / averagePrice.value) * 100
  
  if (Math.abs(percentage) < 1) return 'Similar to comparables'
  
  return percentage > 0 
    ? `${percentage.toFixed(1)}% higher than average`
    : `${Math.abs(percentage).toFixed(1)}% lower than average`
})

const priceComparisonClass = computed(() => {
  if (!props.currentProperty || !props.currentProperty.current_value) return 'text-gray-500'
  
  const diff = props.currentProperty.current_value - averagePrice.value
  
  if (Math.abs(diff) < averagePrice.value * 0.01) return 'text-gray-500'
  
  return diff > 0 ? 'text-red-600' : 'text-green-600'
})

const sizeComparison = computed(() => {
  if (!props.currentProperty || !props.currentProperty.square_feet) return ''
  
  const diff = props.currentProperty.square_feet - averageSize.value
  const percentage = (diff / averageSize.value) * 100
  
  if (Math.abs(percentage) < 1) return 'Similar to comparables'
  
  return percentage > 0 
    ? `${percentage.toFixed(1)}% larger than average`
    : `${Math.abs(percentage).toFixed(1)}% smaller than average`
})

const sizeComparisonClass = computed(() => {
  if (!props.currentProperty || !props.currentProperty.square_feet) return 'text-gray-500'
  
  const diff = props.currentProperty.square_feet - averageSize.value
  
  if (Math.abs(diff) < averageSize.value * 0.01) return 'text-gray-500'
  
  return diff > 0 ? 'text-green-600' : 'text-gray-500'
})

const pricePerSqFtComparison = computed(() => {
  if (!props.currentProperty || !props.currentProperty.current_value || !props.currentProperty.square_feet) return ''
  
  const currentPricePerSqFt = props.currentProperty.current_value / props.currentProperty.square_feet
  const diff = currentPricePerSqFt - averagePricePerSqFt.value
  const percentage = (diff / averagePricePerSqFt.value) * 100
  
  if (Math.abs(percentage) < 1) return 'Similar to comparables'
  
  return percentage > 0 
    ? `${percentage.toFixed(1)}% higher than average`
    : `${Math.abs(percentage).toFixed(1)}% lower than average`
})

const pricePerSqFtComparisonClass = computed(() => {
  if (!props.currentProperty || !props.currentProperty.current_value || !props.currentProperty.square_feet) return 'text-gray-500'
  
  const currentPricePerSqFt = props.currentProperty.current_value / props.currentProperty.square_feet
  const diff = currentPricePerSqFt - averagePricePerSqFt.value
  
  if (Math.abs(diff) < averagePricePerSqFt.value * 0.01) return 'text-gray-500'
  
  return diff > 0 ? 'text-red-600' : 'text-green-600'
})

// Format currency values
const formatCurrency = (value) => {
  if (!value) return 'N/A'
  
  return new Intl.NumberFormat('en-US', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Format numbers with commas
const formatNumber = (value) => {
  if (!value) return 'N/A'
  
  return new Intl.NumberFormat('en-US').format(value)
}

// Calculate price per square foot for a property
const calculatePricePerSqFt = (property) => {
  if (!property.price || !property.square_feet) return 'N/A'
  
  const pricePerSqFt = property.price / property.square_feet
  return pricePerSqFt.toFixed(0)
}

// Get similarity class based on score
const getSimilarityClass = (score) => {
  if (!score) return 'bg-gray-100 text-gray-800'
  
  if (score >= 90) return 'bg-green-100 text-green-800'
  if (score >= 75) return 'bg-blue-100 text-blue-800'
  if (score >= 60) return 'bg-yellow-100 text-yellow-800'
  return 'bg-orange-100 text-orange-800'
}

// Get similarity label based on score
const getSimilarityLabel = (score) => {
  if (!score) return 'Unknown'
  
  if (score >= 90) return 'Very Similar'
  if (score >= 75) return 'Similar'
  if (score >= 60) return 'Somewhat Similar'
  return 'Less Similar'
}

// Navigate to property details page
const viewProperty = (propertyId) => {
  router.push(`/property/${propertyId}`)
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