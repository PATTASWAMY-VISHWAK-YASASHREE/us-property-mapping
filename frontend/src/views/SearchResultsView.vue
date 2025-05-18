<template>
  <div class="search-results-container">
    <h1>Search Results</h1>
    
    <div class="search-filters">
      <h2>Filters</h2>
      <div class="filter-controls">
        <div class="filter-group">
          <label>Result Types</label>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" v-model="searchStore.searchFilters.types" value="properties" />
              Properties
            </label>
            <label>
              <input type="checkbox" v-model="searchStore.searchFilters.types" value="owners" />
              Owners
            </label>
            <label>
              <input type="checkbox" v-model="searchStore.searchFilters.types" value="companies" />
              Companies
            </label>
          </div>
        </div>
        
        <div class="filter-group">
          <label>Value Range</label>
          <div class="range-inputs">
            <input 
              type="number" 
              v-model="searchStore.searchFilters.minValue" 
              placeholder="Min Value" 
            />
            <span>to</span>
            <input 
              type="number" 
              v-model="searchStore.searchFilters.maxValue" 
              placeholder="Max Value" 
            />
          </div>
        </div>
        
        <div class="filter-group">
          <label>Sort By</label>
          <select v-model="searchStore.searchFilters.sortBy">
            <option value="relevance">Relevance</option>
            <option value="value">Value</option>
            <option value="date">Date</option>
            <option value="name">Name</option>
          </select>
          <select v-model="searchStore.searchFilters.sortOrder">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
        
        <div class="filter-actions">
          <button @click="applyFilters" class="btn-primary">Apply Filters</button>
          <button @click="resetFilters" class="btn-secondary">Reset</button>
        </div>
      </div>
    </div>
    
    <div v-if="searchStore.loading" class="loading">
      <p>Loading results...</p>
    </div>
    
    <div v-else-if="searchStore.error" class="error">
      <p>{{ searchStore.error }}</p>
    </div>
    
    <div v-else class="search-results">
      <div v-if="!searchStore.hasResults" class="no-results">
        <p>No results found. Please try a different search term or adjust your filters.</p>
      </div>
      
      <template v-else>
        <div class="results-summary">
          <p>Found {{ searchStore.totalResults }} results</p>
        </div>
        
        <!-- Property Results -->
        <div v-if="searchStore.searchResults.properties.length > 0" class="result-section">
          <h2>Properties ({{ searchStore.searchResults.properties.length }})</h2>
          <div class="result-cards">
            <div 
              v-for="property in searchStore.searchResults.properties" 
              :key="property.id" 
              class="result-card"
              @click="viewProperty(property.id)"
            >
              <div class="card-image" v-if="property.image_url">
                <img :src="property.image_url" :alt="property.address" />
              </div>
              <div class="card-content">
                <h3>{{ property.address }}</h3>
                <p>{{ property.city }}, {{ property.state }} {{ property.zip_code }}</p>
                <p class="property-value">{{ formatCurrency(property.value) }}</p>
                <p>{{ property.property_type }} | {{ property.bedrooms }} beds | {{ property.bathrooms }} baths</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Owner Results -->
        <div v-if="searchStore.searchResults.owners.length > 0" class="result-section">
          <h2>Owners ({{ searchStore.searchResults.owners.length }})</h2>
          <div class="result-cards">
            <div 
              v-for="owner in searchStore.searchResults.owners" 
              :key="owner.id" 
              class="result-card"
              @click="viewOwner(owner.id)"
            >
              <div class="card-content">
                <h3>{{ owner.name }}</h3>
                <p>{{ owner.type === 'individual' ? 'Individual' : 'Corporate' }}</p>
                <p>{{ owner.properties_count }} properties</p>
                <p v-if="owner.net_worth">Net Worth: {{ formatCurrency(owner.net_worth) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Company Results -->
        <div v-if="searchStore.searchResults.companies.length > 0" class="result-section">
          <h2>Companies ({{ searchStore.searchResults.companies.length }})</h2>
          <div class="result-cards">
            <div 
              v-for="company in searchStore.searchResults.companies" 
              :key="company.id" 
              class="result-card"
              @click="viewCompany(company.id)"
            >
              <div class="card-content">
                <h3>{{ company.name }}</h3>
                <p>{{ company.industry }}</p>
                <p>{{ company.properties_count }} properties</p>
                <p v-if="company.market_value">Market Value: {{ formatCurrency(company.market_value) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="save-search">
          <button @click="showSaveSearchModal = true" class="btn-primary">Save This Search</button>
        </div>
      </template>
    </div>
    
    <!-- Save Search Modal -->
    <div v-if="showSaveSearchModal" class="modal">
      <div class="modal-content">
        <h2>Save Search</h2>
        <div class="form-group">
          <label for="searchName">Search Name</label>
          <input type="text" id="searchName" v-model="saveSearchName" placeholder="Enter a name for this search" />
        </div>
        <div class="modal-actions">
          <button @click="saveSearch" class="btn-primary">Save</button>
          <button @click="showSaveSearchModal = false" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSearchStore } from '../stores/search'

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()

const showSaveSearchModal = ref(false)
const saveSearchName = ref('')

onMounted(() => {
  // Get search query from URL parameters
  const query = route.query.q
  
  if (query) {
    // Perform search with the query from URL
    performSearch(query)
  }
})

function performSearch(query) {
  searchStore.search(query)
}

function applyFilters() {
  // Re-run the search with current filters
  const query = route.query.q
  if (query) {
    performSearch(query)
  }
}

function resetFilters() {
  searchStore.resetSearchFilters()
  applyFilters()
}

function viewProperty(id) {
  router.push({ name: 'property', params: { id } })
}

function viewOwner(id) {
  router.push({ name: 'owner', params: { id } })
}

function viewCompany(id) {
  router.push({ name: 'company', params: { id } })
}

function saveSearch() {
  const query = route.query.q
  if (query && saveSearchName.value) {
    searchStore.saveSearch(saveSearchName.value, query)
      .then(() => {
        showSaveSearchModal.value = false
        saveSearchName.value = ''
      })
  }
}

function formatCurrency(value) {
  if (!value) return '$0'
  
  // Convert to number if it's a string
  const numValue = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]+/g, '')) : value
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(numValue)
}
</script>

<style scoped>
.search-results-container {
  padding: 20px;
}

.search-filters {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-group {
  margin-bottom: 10px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.checkbox-group {
  display: flex;
  gap: 15px;
}

.checkbox-group label {
  font-weight: normal;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.range-inputs input {
  width: 120px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.result-section {
  margin-bottom: 30px;
}

.result-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.result-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.card-image {
  height: 180px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 15px;
}

.card-content h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.property-value {
  font-weight: bold;
  color: #2c3e50;
}

.save-search {
  margin-top: 20px;
  text-align: center;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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

.loading, .error, .no-results {
  text-align: center;
  padding: 40px 0;
}

.error {
  color: #e74c3c;
}
</style>