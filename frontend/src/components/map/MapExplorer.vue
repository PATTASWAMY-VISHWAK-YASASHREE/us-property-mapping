<template>
  <div class="map-explorer">
    <!-- Search and Filter Panel -->
    <div class="search-filter-panel" :class="{ 'panel-collapsed': isPanelCollapsed }">
      <div class="panel-header">
        <h2 class="panel-title">Property Explorer</h2>
        <button @click="togglePanel" class="panel-toggle-btn">
          <i :class="isPanelCollapsed ? 'expand-icon' : 'collapse-icon'"></i>
        </button>
      </div>
      
      <div v-if="!isPanelCollapsed" class="panel-content">
        <!-- Search Bar -->
        <div class="search-container">
          <SearchBar @search="handleSearch" />
        </div>
        
        <!-- Filter Controls -->
        <div class="filter-section">
          <h3 class="section-title">Filters</h3>
          
          <!-- Property Type Filter -->
          <div class="filter-group">
            <label class="filter-label">Property Type</label>
            <div class="checkbox-group">
              <label v-for="type in propertyTypes" :key="type" class="checkbox-label">
                <input 
                  type="checkbox" 
                  :value="type" 
                  v-model="filters.propertyType"
                  @change="applyFilters"
                />
                {{ type }}
              </label>
            </div>
          </div>
          
          <!-- Price Range Filter -->
          <div class="filter-group">
            <label class="filter-label">Price Range</label>
            <div class="range-inputs">
              <div class="input-group">
                <span class="currency-symbol">$</span>
                <input 
                  type="number" 
                  v-model.number="filters.minValue" 
                  placeholder="Min"
                  @change="applyFilters"
                />
              </div>
              <span class="range-separator">to</span>
              <div class="input-group">
                <span class="currency-symbol">$</span>
                <input 
                  type="number" 
                  v-model.number="filters.maxValue" 
                  placeholder="Max"
                  @change="applyFilters"
                />
              </div>
            </div>
          </div>
          
          <!-- Bedrooms Filter -->
          <div class="filter-group">
            <label class="filter-label">Bedrooms</label>
            <div class="range-inputs">
              <input 
                type="number" 
                v-model.number="filters.minBedrooms" 
                placeholder="Min"
                min="0"
                @change="applyFilters"
              />
              <span class="range-separator">to</span>
              <input 
                type="number" 
                v-model.number="filters.maxBedrooms" 
                placeholder="Max"
                min="0"
                @change="applyFilters"
              />
            </div>
          </div>
          
          <!-- Bathrooms Filter -->
          <div class="filter-group">
            <label class="filter-label">Bathrooms</label>
            <div class="range-inputs">
              <input 
                type="number" 
                v-model.number="filters.minBathrooms" 
                placeholder="Min"
                min="0"
                step="0.5"
                @change="applyFilters"
              />
              <span class="range-separator">to</span>
              <input 
                type="number" 
                v-model.number="filters.maxBathrooms" 
                placeholder="Max"
                min="0"
                step="0.5"
                @change="applyFilters"
              />
            </div>
          </div>
          
          <!-- Year Built Filter -->
          <div class="filter-group">
            <label class="filter-label">Year Built</label>
            <div class="range-inputs">
              <input 
                type="number" 
                v-model.number="filters.yearBuiltMin" 
                placeholder="Min"
                min="1800"
                max="2023"
                @change="applyFilters"
              />
              <span class="range-separator">to</span>
              <input 
                type="number" 
                v-model.number="filters.yearBuiltMax" 
                placeholder="Max"
                min="1800"
                max="2023"
                @change="applyFilters"
              />
            </div>
          </div>
          
          <!-- Filter Actions -->
          <div class="filter-actions">
            <button @click="resetFilters" class="reset-btn">Reset Filters</button>
            <button @click="saveCurrentSearch" class="save-btn">Save Search</button>
          </div>
        </div>
        
        <!-- Search Results Summary -->
        <div class="results-summary">
          <p v-if="loading">Loading properties...</p>
          <p v-else-if="filteredProperties.length === 0">No properties found</p>
          <p v-else>{{ filteredProperties.length }} properties found</p>
        </div>
        
        <!-- Property List -->
        <div class="property-list">
          <div 
            v-for="property in filteredProperties" 
            :key="property.id || property.address"
            class="property-card"
            :class="{ 'selected': selectedProperty && (selectedProperty.id === property.id || selectedProperty.address === property.address) }"
            @click="selectProperty(property)"
          >
            <div class="property-image">
              <img :src="property.imageUrl || 'https://via.placeholder.com/150'" :alt="property.address" />
            </div>
            <div class="property-info">
              <h4 class="property-address">{{ property.address }}</h4>
              <p class="property-price">${{ formatNumber(property.price || extractNumericValue(property.value)) }}</p>
              <div class="property-details">
                <span v-if="property.bedrooms">{{ property.bedrooms }} bd</span>
                <span v-if="property.bedrooms && property.bathrooms">•</span>
                <span v-if="property.bathrooms">{{ property.bathrooms }} ba</span>
                <span v-if="(property.bedrooms || property.bathrooms) && property.squareFootage">•</span>
                <span v-if="property.squareFootage">{{ formatNumber(property.squareFootage) }} sqft</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Map Container -->
    <div class="map-container">
      <PropertyMap 
        :properties="filteredProperties"
        :selected-property="selectedProperty"
        :height="'100%'"
        @property-selected="selectProperty"
      />
    </div>
    
    <!-- Property Detail Panel -->
    <div v-if="selectedProperty" class="property-detail-panel">
      <div class="panel-header">
        <h3>Property Details</h3>
        <button @click="closePropertyDetail" class="close-btn">×</button>
      </div>
      
      <div class="panel-content">
        <div class="property-image">
          <img :src="selectedProperty.imageUrl || 'https://via.placeholder.com/300x200'" :alt="selectedProperty.address" />
        </div>
        
        <h3 class="property-address">{{ selectedProperty.address }}</h3>
        <p class="property-price">${{ formatNumber(selectedProperty.price || extractNumericValue(selectedProperty.value)) }}</p>
        
        <div class="property-specs">
          <div class="spec-item" v-if="selectedProperty.bedrooms">
            <i class="bed-icon"></i>
            <span>{{ selectedProperty.bedrooms }} Bedrooms</span>
          </div>
          <div class="spec-item" v-if="selectedProperty.bathrooms">
            <i class="bath-icon"></i>
            <span>{{ selectedProperty.bathrooms }} Bathrooms</span>
          </div>
          <div class="spec-item" v-if="selectedProperty.squareFootage">
            <i class="area-icon"></i>
            <span>{{ formatNumber(selectedProperty.squareFootage) }} sq ft</span>
          </div>
          <div class="spec-item" v-if="selectedProperty.yearBuilt">
            <i class="year-icon"></i>
            <span>Built in {{ selectedProperty.yearBuilt }}</span>
          </div>
        </div>
        
        <div class="property-description" v-if="selectedProperty.description">
          <h4>Description</h4>
          <p>{{ selectedProperty.description }}</p>
        </div>
        
        <div class="property-history" v-if="selectedProperty.history && selectedProperty.history.length > 0">
          <h4>Value History</h4>
          <div class="history-chart">
            <!-- Placeholder for chart -->
            <div class="history-bars">
              <div 
                v-for="(item, index) in selectedProperty.history" 
                :key="index"
                class="history-bar"
                :style="{ height: calculateBarHeight(item.value) }"
              >
                <div class="bar-value">${{ formatShortValue(extractNumericValue(item.value)) }}</div>
                <div class="bar-year">{{ item.year }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="nearby-properties" v-if="selectedProperty.nearbyProperties && selectedProperty.nearbyProperties.length > 0">
          <h4>Nearby Properties</h4>
          <div class="nearby-list">
            <div v-for="(nearby, index) in selectedProperty.nearbyProperties" :key="index" class="nearby-item">
              <div class="nearby-info">
                <div class="nearby-address">{{ nearby.address }}</div>
                <div class="nearby-value">${{ formatShortValue(extractNumericValue(nearby.value)) }}</div>
              </div>
              <div class="nearby-distance">{{ nearby.distance }}</div>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <button class="view-details-btn">View Full Details</button>
          <button class="contact-btn">Contact Agent</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { usePropertyStore } from '@/stores/property';
import PropertyMap from './PropertyMap.vue';
import SearchBar from '../search/SearchBar.vue';
import { useToast } from 'vue-toastification';

// Store
const propertyStore = usePropertyStore();
const toast = useToast();

// State
const isPanelCollapsed = ref(false);
const selectedProperty = ref(null);
const searchQuery = ref('');
const loading = ref(false);
const properties = ref([]);
const filters = ref({
  propertyType: [],
  minValue: null,
  maxValue: null,
  minBedrooms: null,
  maxBedrooms: null,
  minBathrooms: null,
  maxBathrooms: null,
  yearBuiltMin: null,
  yearBuiltMax: null
});

// Property types for filter
const propertyTypes = ['Residential', 'Commercial', 'Industrial', 'Land', 'Multi-Family'];

// Computed properties
const filteredProperties = computed(() => {
  if (!properties.value.length) return [];
  
  return properties.value.filter(property => {
    // Apply filters
    if (filters.value.propertyType.length > 0 && 
        !filters.value.propertyType.includes(property.type)) {
      return false;
    }
    
    const propertyValue = property.price || extractNumericValue(property.value) || 0;
    
    if (filters.value.minValue && propertyValue < filters.value.minValue) {
      return false;
    }
    
    if (filters.value.maxValue && propertyValue > filters.value.maxValue) {
      return false;
    }
    
    if (filters.value.minBedrooms && property.bedrooms < filters.value.minBedrooms) {
      return false;
    }
    
    if (filters.value.maxBedrooms && property.bedrooms > filters.value.maxBedrooms) {
      return false;
    }
    
    if (filters.value.minBathrooms && property.bathrooms < filters.value.minBathrooms) {
      return false;
    }
    
    if (filters.value.maxBathrooms && property.bathrooms > filters.value.maxBathrooms) {
      return false;
    }
    
    if (filters.value.yearBuiltMin && property.yearBuilt < filters.value.yearBuiltMin) {
      return false;
    }
    
    if (filters.value.yearBuiltMax && property.yearBuilt > filters.value.yearBuiltMax) {
      return false;
    }
    
    return true;
  });
});

// Methods
const togglePanel = () => {
  isPanelCollapsed.value = !isPanelCollapsed.value;
};

const handleSearch = (query) => {
  searchQuery.value = query;
  fetchProperties(query);
};

const selectProperty = (property) => {
  selectedProperty.value = property;
  propertyStore.addToRecentlyViewed(property);
};

const closePropertyDetail = () => {
  selectedProperty.value = null;
};

const applyFilters = () => {
  propertyStore.updateSearchFilters(filters.value);
};

const resetFilters = () => {
  filters.value = {
    propertyType: [],
    minValue: null,
    maxValue: null,
    minBedrooms: null,
    maxBedrooms: null,
    minBathrooms: null,
    maxBathrooms: null,
    yearBuiltMin: null,
    yearBuiltMax: null
  };
  propertyStore.resetSearchFilters();
};

const saveCurrentSearch = () => {
  // Implement save search functionality
  const searchName = prompt('Enter a name for this search:');
  if (searchName) {
    propertyStore.saveSearch(searchName, searchQuery.value, filters.value)
      .then(() => {
        toast.success('Search saved successfully');
      })
      .catch(error => {
        toast.error('Failed to save search');
      });
  }
};

const fetchProperties = async (query = '') => {
  loading.value = true;
  try {
    if (query) {
      const results = await propertyStore.searchProperties(query);
      properties.value = results;
    } else {
      const results = await propertyStore.fetchProperties();
      properties.value = results;
    }
  } catch (error) {
    console.error('Error fetching properties:', error);
    toast.error('Failed to fetch properties');
    properties.value = [];
  } finally {
    loading.value = false;
  }
};

// Helper functions
const formatNumber = (num) => {
  if (!num) return '0';
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const formatShortValue = (value) => {
  if (!value) return '0';
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M';
  } else if (value >= 1000) {
    return (value / 1000).toFixed(0) + 'K';
  }
  return value.toString();
};

const extractNumericValue = (valueString) => {
  if (!valueString) return 0;
  if (typeof valueString === 'number') return valueString;
  
  // Remove $ and commas, then parse as float
  const numericValue = parseFloat(valueString.replace(/[$,]/g, ''));
  return isNaN(numericValue) ? 0 : numericValue;
};

const calculateBarHeight = (value) => {
  const numericValue = extractNumericValue(value);
  // Calculate percentage height based on max value in history
  if (!selectedProperty.value || !selectedProperty.value.history) return '0%';
  
  const maxValue = Math.max(...selectedProperty.value.history.map(item => extractNumericValue(item.value)));
  const percentage = (numericValue / maxValue) * 100;
  return `${percentage}%`;
};

// Lifecycle hooks
onMounted(async () => {
  await fetchProperties();
});

// Watch for changes in property store
watch(() => propertyStore.properties, (newProperties) => {
  if (newProperties.length > 0) {
    properties.value = newProperties;
  }
});
</script>

<style scoped>
.map-explorer {
  display: grid;
  grid-template-columns: 350px 1fr;
  grid-template-rows: 1fr;
  height: 100vh;
  position: relative;
}

.search-filter-panel {
  background-color: white;
  border-right: 1px solid #e2e8f0;
  overflow-y: auto;
  transition: width 0.3s ease;
  grid-column: 1;
  grid-row: 1;
  z-index: 10;
}

.panel-collapsed {
  width: 50px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f7fafc;
  position: sticky;
  top: 0;
  z-index: 5;
}

.panel-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.panel-toggle-btn {
  background: none;
  border: none;
  color: #4a5568;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.expand-icon, .collapse-icon {
  width: 20px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.expand-icon {
  background-image: url('@/assets/icons/expand.svg');
}

.collapse-icon {
  background-image: url('@/assets/icons/collapse.svg');
}

.panel-content {
  padding: 1rem;
}

.search-container {
  margin-bottom: 1.5rem;
}

.filter-section {
  margin-bottom: 1.5rem;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
}

.filter-group {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #edf2f7;
}

.filter-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #4a5568;
  cursor: pointer;
  margin-right: 1rem;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.range-separator {
  color: #718096;
  font-size: 0.875rem;
}

.input-group {
  position: relative;
  flex: 1;
}

.currency-symbol {
  position: absolute;
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: #718096;
}

input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  padding-left: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

input[type="number"]:focus {
  outline: none;
  border-color: #4a6cf7;
  box-shadow: 0 0 0 1px #4a6cf7;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.reset-btn, .save-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-btn {
  background-color: #edf2f7;
  color: #4a5568;
  border: none;
}

.reset-btn:hover {
  background-color: #e2e8f0;
}

.save-btn {
  background-color: #4a6cf7;
  color: white;
  border: none;
}

.save-btn:hover {
  background-color: #3a5ce5;
}

.results-summary {
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.property-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 500px;
  overflow-y: auto;
}

.property-card {
  display: flex;
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.property-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.property-card.selected {
  border: 2px solid #4a6cf7;
}

.property-image {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.property-info {
  padding: 0.75rem;
  flex-grow: 1;
}

.property-address {
  margin: 0 0 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.property-price {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #4a6cf7;
}

.property-details {
  font-size: 0.75rem;
  color: #718096;
}

.map-container {
  grid-column: 2;
  grid-row: 1;
  height: 100%;
}

.property-detail-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 400px;
  height: 100%;
  background-color: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 20;
  overflow-y: auto;
}

.property-detail-panel .panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f7fafc;
}

.property-detail-panel .panel-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #4a5568;
  cursor: pointer;
}

.property-detail-panel .panel-content {
  padding: 1.5rem;
}

.property-detail-panel .property-image {
  width: 100%;
  height: 200px;
  margin-bottom: 1.5rem;
  border-radius: 0.5rem;
  overflow: hidden;
}

.property-specs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.spec-item {
  display: flex;
  align-items: center;
}

.spec-item i {
  width: 24px;
  height: 24px;
  margin-right: 0.5rem;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.bed-icon {
  background-image: url('@/assets/icons/bed.svg');
}

.bath-icon {
  background-image: url('@/assets/icons/bath.svg');
}

.area-icon {
  background-image: url('@/assets/icons/area.svg');
}

.year-icon {
  background-image: url('@/assets/icons/calendar.svg');
}

.property-description {
  margin-bottom: 1.5rem;
}

.property-description h4, .property-history h4, .nearby-properties h4 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
}

.property-description p {
  margin: 0;
  font-size: 0.875rem;
  color: #4a5568;
  line-height: 1.5;
}

.property-history {
  margin-bottom: 1.5rem;
}

.history-chart {
  height: 150px;
  margin-top: 1rem;
}

.history-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 100%;
}

.history-bar {
  width: 40px;
  background-color: #4a6cf7;
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 20px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  font-weight: 500;
  color: #4a5568;
}

.bar-year {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: #718096;
}

.nearby-properties {
  margin-bottom: 1.5rem;
}

.nearby-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.nearby-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: #f7fafc;
  border-radius: 0.25rem;
}

.nearby-address {
  font-size: 0.875rem;
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.nearby-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a6cf7;
}

.nearby-distance {
  font-size: 0.75rem;
  color: #718096;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.view-details-btn, .contact-btn {
  flex: 1;
  padding: 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s;
}

.view-details-btn {
  background-color: #4a6cf7;
  color: white;
  border: none;
}

.view-details-btn:hover {
  background-color: #3a5ce5;
}

.contact-btn {
  background-color: white;
  color: #4a6cf7;
  border: 1px solid #4a6cf7;
}

.contact-btn:hover {
  background-color: #ebf4ff;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .map-explorer {
    grid-template-columns: 300px 1fr;
  }
  
  .property-detail-panel {
    width: 350px;
  }
}

@media (max-width: 768px) {
  .map-explorer {
    grid-template-columns: 1fr;
    grid-template-rows: 50% 50%;
  }
  
  .search-filter-panel {
    grid-column: 1;
    grid-row: 1;
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .map-container {
    grid-column: 1;
    grid-row: 2;
  }
  
  .property-detail-panel {
    width: 100%;
    height: 50%;
    top: 50%;
  }
}
</style>