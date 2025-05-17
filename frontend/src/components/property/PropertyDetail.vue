<template>
  <div class="property-detail bg-white rounded-lg shadow-md overflow-hidden">
    <!-- Property Images Gallery -->
    <div class="property-images relative">
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75">
        <div class="spinner"></div>
      </div>
      
      <div v-else class="flex overflow-x-auto">
        <div v-if="property.images && property.images.length > 0" class="flex">
          <img 
            v-for="(image, index) in property.images" 
            :key="index" 
            :src="image.url" 
            :alt="`${property.address} - Image ${index + 1}`"
            class="h-64 w-auto object-cover"
            @click="openImageGallery(index)"
          />
        </div>
        <div v-else class="w-full h-64 bg-gray-200 flex items-center justify-center">
          <span class="text-gray-500">No images available</span>
        </div>
      </div>
    </div>
    
    <!-- Property Overview -->
    <div class="p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Property Overview</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Basic Information -->
        <div class="bg-gray-50 p-4 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-700 mb-3">Basic Information</h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Property Type:</span>
              <span class="font-medium">{{ property.property_type || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Year Built:</span>
              <span class="font-medium">{{ property.year_built || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Bedrooms:</span>
              <span class="font-medium">{{ property.bedrooms || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Bathrooms:</span>
              <span class="font-medium">{{ property.bathrooms || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Square Feet:</span>
              <span class="font-medium">{{ formatNumber(property.square_feet) || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Lot Size:</span>
              <span class="font-medium">{{ formatNumber(property.lot_size) || 'N/A' }} sq ft</span>
            </div>
          </div>
        </div>
        
        <!-- Valuation Information -->
        <div class="bg-gray-50 p-4 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-700 mb-3">Valuation</h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Current Value:</span>
              <span class="font-medium text-green-600">${{ formatCurrency(property.current_value) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Last Sale Price:</span>
              <span class="font-medium">${{ formatCurrency(property.last_sale_price) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Last Sale Date:</span>
              <span class="font-medium">{{ formatDate(property.last_sale_date) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Value Change (1yr):</span>
              <span :class="valueChangeClass">{{ valueChange }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Estimate Date:</span>
              <span class="font-medium">{{ formatDate(property.value_estimate_date) }}</span>
            </div>
          </div>
        </div>
        
        <!-- Location Information -->
        <div class="bg-gray-50 p-4 rounded-lg">
          <h3 class="text-lg font-semibold text-gray-700 mb-3">Location</h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Address:</span>
              <span class="font-medium">{{ property.address }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">City:</span>
              <span class="font-medium">{{ property.city }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">State:</span>
              <span class="font-medium">{{ property.state }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Zip Code:</span>
              <span class="font-medium">{{ property.zip_code }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">County:</span>
              <span class="font-medium">{{ property.county || 'N/A' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">School District:</span>
              <span class="font-medium">{{ property.school_district || 'N/A' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Property Features -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Property Features</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Interior Features -->
          <div>
            <h4 class="text-lg font-medium text-gray-700 mb-2">Interior</h4>
            <ul class="list-disc list-inside space-y-1 text-gray-600">
              <li v-if="property.heating_type">Heating: {{ property.heating_type }}</li>
              <li v-if="property.cooling_type">Cooling: {{ property.cooling_type }}</li>
              <li v-if="property.basement">Basement: {{ property.basement ? 'Yes' : 'No' }}</li>
              <li v-if="property.flooring">Flooring: {{ property.flooring }}</li>
              <li v-if="property.fireplace">Fireplace: {{ property.fireplace ? 'Yes' : 'No' }}</li>
              <li v-if="property.interior_features && property.interior_features.length">
                Additional Features: {{ property.interior_features.join(', ') }}
              </li>
            </ul>
          </div>
          
          <!-- Exterior Features -->
          <div>
            <h4 class="text-lg font-medium text-gray-700 mb-2">Exterior</h4>
            <ul class="list-disc list-inside space-y-1 text-gray-600">
              <li v-if="property.construction_type">Construction: {{ property.construction_type }}</li>
              <li v-if="property.roof_type">Roof: {{ property.roof_type }}</li>
              <li v-if="property.garage_type">Garage: {{ property.garage_type }}</li>
              <li v-if="property.parking_spaces">Parking Spaces: {{ property.parking_spaces }}</li>
              <li v-if="property.pool">Pool: {{ property.pool ? 'Yes' : 'No' }}</li>
              <li v-if="property.exterior_features && property.exterior_features.length">
                Additional Features: {{ property.exterior_features.join(', ') }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- Property Description -->
      <div class="mt-8" v-if="property.description">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Description</h3>
        <p class="text-gray-600">{{ property.description }}</p>
      </div>
      
      <!-- Property Location Map -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Location</h3>
        <div class="h-64 bg-gray-200 rounded-lg">
          <!-- Map component would go here -->
          <div class="w-full h-full flex items-center justify-center">
            <span class="text-gray-500">Map loading...</span>
          </div>
        </div>
      </div>
      
      <!-- Neighborhood Information -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Neighborhood</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Schools -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h4 class="text-lg font-medium text-gray-700 mb-2">Schools</h4>
            <div v-if="property.schools && property.schools.length" class="space-y-3">
              <div v-for="(school, index) in property.schools" :key="index" class="text-sm">
                <div class="font-medium">{{ school.name }}</div>
                <div class="text-gray-600">{{ school.type }} • {{ school.distance }} miles</div>
                <div class="flex items-center mt-1">
                  <span class="text-yellow-500 mr-1">★</span>
                  <span>{{ school.rating }}/10</span>
                </div>
              </div>
            </div>
            <div v-else class="text-gray-500">No school information available</div>
          </div>
          
          <!-- Demographics -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h4 class="text-lg font-medium text-gray-700 mb-2">Demographics</h4>
            <div v-if="property.demographics" class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Population:</span>
                <span>{{ formatNumber(property.demographics.population) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Median Age:</span>
                <span>{{ property.demographics.median_age }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Median Income:</span>
                <span>${{ formatCurrency(property.demographics.median_income) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Education Level:</span>
                <span>{{ property.demographics.education_level }}</span>
              </div>
            </div>
            <div v-else class="text-gray-500">No demographic information available</div>
          </div>
          
          <!-- Points of Interest -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h4 class="text-lg font-medium text-gray-700 mb-2">Points of Interest</h4>
            <div v-if="property.points_of_interest && property.points_of_interest.length" class="space-y-2 text-sm">
              <div v-for="(poi, index) in property.points_of_interest" :key="index" class="flex justify-between">
                <span>{{ poi.name }}</span>
                <span class="text-gray-600">{{ poi.distance }} miles</span>
              </div>
            </div>
            <div v-else class="text-gray-500">No points of interest available</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  property: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
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

// Calculate value change percentage
const valueChange = computed(() => {
  if (!props.property.value_change_percent) return 'N/A'
  
  const change = props.property.value_change_percent
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(1)}%`
})

// Determine CSS class for value change
const valueChangeClass = computed(() => {
  if (!props.property.value_change_percent) return 'font-medium'
  
  return props.property.value_change_percent >= 0 
    ? 'font-medium text-green-600' 
    : 'font-medium text-red-600'
})

// Open image gallery
const openImageGallery = (index) => {
  // Implementation would depend on the gallery component used
  console.log('Open gallery at index:', index)
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