<template>
  <div class="dashboard-container">
    <h1>Dashboard</h1>
    
    <div class="dashboard-grid">
      <!-- Recent Activities Section -->
      <div class="dashboard-card">
        <h2>Recent Activities</h2>
        <div class="card-content">
          <p v-if="recentActivities.length === 0" class="empty-state">No recent activities</p>
          <ul v-else class="activity-list">
            <li v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon">
                <i :class="getActivityIcon(activity.type)"></i>
              </div>
              <div class="activity-details">
                <span class="activity-title">{{ activity.title }}</span>
                <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Saved Searches Section -->
      <div class="dashboard-card">
        <h2>Saved Searches</h2>
        <div class="card-content">
          <p v-if="savedSearches.length === 0" class="empty-state">No saved searches</p>
          <ul v-else class="search-list">
            <li v-for="search in savedSearches" :key="search.id" class="search-item">
              <router-link :to="{ name: 'search-results', query: search.params }">
                {{ search.name }}
              </router-link>
              <div class="search-actions">
                <button @click="runSearch(search)" class="btn-icon" title="Run search">
                  <i class="icon search-icon"></i>
                </button>
                <button @click="deleteSearch(search.id)" class="btn-icon" title="Delete search">
                  <i class="icon delete-icon"></i>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Bookmarked Properties Section -->
      <div class="dashboard-card">
        <h2>Bookmarked Properties</h2>
        <div class="card-content">
          <p v-if="bookmarkedProperties.length === 0" class="empty-state">No bookmarked properties</p>
          <div v-else class="property-grid">
            <div v-for="property in bookmarkedProperties" :key="property.id" class="property-card">
              <router-link :to="{ name: 'property-details', params: { id: property.id }}">
                <div class="property-image">
                  <img :src="property.thumbnail || '/placeholder-property.jpg'" :alt="property.address">
                </div>
                <div class="property-info">
                  <h3>{{ property.address }}</h3>
                  <p class="property-price">${{ formatPrice(property.estimatedValue) }}</p>
                  <p class="property-meta">{{ property.bedrooms }} bd | {{ property.bathrooms }} ba | {{ property.squareFeet }} sqft</p>
                </div>
              </router-link>
              <button @click="removeBookmark(property.id)" class="btn-icon bookmark-btn" title="Remove bookmark">
                <i class="icon bookmark-filled-icon"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Search Section -->
      <div class="dashboard-card">
        <h2>Quick Search</h2>
        <div class="card-content">
          <form @submit.prevent="performQuickSearch" class="quick-search-form">
            <div class="form-group">
              <label for="location">Location</label>
              <input 
                type="text" 
                id="location" 
                v-model="quickSearch.location" 
                placeholder="City, ZIP, or Address"
                class="form-control"
              >
            </div>
            
            <div class="form-row">
              <div class="form-group half">
                <label for="minPrice">Min Price</label>
                <input 
                  type="number" 
                  id="minPrice" 
                  v-model="quickSearch.minPrice" 
                  placeholder="Min $"
                  class="form-control"
                >
              </div>
              <div class="form-group half">
                <label for="maxPrice">Max Price</label>
                <input 
                  type="number" 
                  id="maxPrice" 
                  v-model="quickSearch.maxPrice" 
                  placeholder="Max $"
                  class="form-control"
                >
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group third">
                <label for="beds">Beds</label>
                <select id="beds" v-model="quickSearch.beds" class="form-control">
                  <option value="">Any</option>
                  <option value="1">1+</option>
                  <option value="2">2+</option>
                  <option value="3">3+</option>
                  <option value="4">4+</option>
                  <option value="5">5+</option>
                </select>
              </div>
              <div class="form-group third">
                <label for="baths">Baths</label>
                <select id="baths" v-model="quickSearch.baths" class="form-control">
                  <option value="">Any</option>
                  <option value="1">1+</option>
                  <option value="2">2+</option>
                  <option value="3">3+</option>
                  <option value="4">4+</option>
                </select>
              </div>
              <div class="form-group third">
                <label for="propertyType">Type</label>
                <select id="propertyType" v-model="quickSearch.propertyType" class="form-control">
                  <option value="">Any</option>
                  <option value="house">House</option>
                  <option value="condo">Condo</option>
                  <option value="townhouse">Townhouse</option>
                  <option value="multi-family">Multi-family</option>
                  <option value="land">Land</option>
                </select>
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary">Search Properties</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertyStore } from '@/stores/property'

export default {
  name: 'DashboardView',
  setup() {
    const router = useRouter()
    const propertyStore = usePropertyStore()
    
    // Recent Activities
    const recentActivities = ref([])
    
    // Saved Searches
    const savedSearches = ref([])
    
    // Bookmarked Properties
    const bookmarkedProperties = ref([])
    
    // Quick Search
    const quickSearch = ref({
      location: '',
      minPrice: null,
      maxPrice: null,
      beds: '',
      baths: '',
      propertyType: ''
    })
    
    // Fetch data on component mount
    onMounted(async () => {
      try {
        // Fetch recent activities
        const activitiesResponse = await fetch('/api/user/activities')
        if (activitiesResponse.ok) {
          recentActivities.value = await activitiesResponse.json()
        }
        
        // Fetch saved searches
        const searchesResponse = await fetch('/api/user/saved-searches')
        if (searchesResponse.ok) {
          savedSearches.value = await searchesResponse.json()
        }
        
        // Fetch bookmarked properties
        const bookmarksResponse = await fetch('/api/user/bookmarks')
        if (bookmarksResponse.ok) {
          bookmarkedProperties.value = await bookmarksResponse.json()
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      }
    })
    
    // Helper functions
    const getActivityIcon = (type) => {
      const iconMap = {
        'search': 'search-icon',
        'view': 'eye-icon',
        'bookmark': 'bookmark-icon',
        'contact': 'message-icon',
        'report': 'document-icon'
      }
      return iconMap[type] || 'activity-icon'
    }
    
    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      
      if (diffMins < 60) {
        return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
      } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
      } else if (diffDays < 7) {
        return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
      } else {
        return date.toLocaleDateString()
      }
    }
    
    const formatPrice = (price) => {
      return price ? price.toLocaleString() : 'N/A'
    }
    
    // Action handlers
    const runSearch = (search) => {
      router.push({
        name: 'search-results',
        query: search.params
      })
    }
    
    const deleteSearch = async (searchId) => {
      try {
        const response = await fetch(`/api/user/saved-searches/${searchId}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          savedSearches.value = savedSearches.value.filter(search => search.id !== searchId)
        }
      } catch (error) {
        console.error('Error deleting saved search:', error)
      }
    }
    
    const removeBookmark = async (propertyId) => {
      try {
        const response = await fetch(`/api/user/bookmarks/${propertyId}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          bookmarkedProperties.value = bookmarkedProperties.value.filter(
            property => property.id !== propertyId
          )
        }
      } catch (error) {
        console.error('Error removing bookmark:', error)
      }
    }
    
    const performQuickSearch = () => {
      // Filter out empty values
      const query = Object.entries(quickSearch.value).reduce((acc, [key, value]) => {
        if (value !== null && value !== '') {
          acc[key] = value
        }
        return acc
      }, {})
      
      router.push({
        name: 'search-results',
        query
      })
    }
    
    return {
      recentActivities,
      savedSearches,
      bookmarkedProperties,
      quickSearch,
      getActivityIcon,
      formatTime,
      formatPrice,
      runSearch,
      deleteSearch,
      removeBookmark,
      performQuickSearch
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.dashboard-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.dashboard-card h2 {
  padding: 15px;
  margin: 0;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-size: 1.2rem;
}

.card-content {
  padding: 15px;
}

.empty-state {
  color: #6c757d;
  text-align: center;
  padding: 20px 0;
}

/* Recent Activities */
.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.activity-details {
  flex: 1;
}

.activity-title {
  display: block;
  font-weight: 500;
}

.activity-time {
  display: block;
  font-size: 0.8rem;
  color: #6c757d;
}

/* Saved Searches */
.search-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.search-item:last-child {
  border-bottom: none;
}

.search-actions {
  display: flex;
  gap: 5px;
}

/* Bookmarked Properties */
.property-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.property-card {
  position: relative;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
}

.property-image {
  height: 100px;
  overflow: hidden;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.property-info {
  padding: 10px;
}

.property-info h3 {
  margin: 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.property-price {
  font-weight: bold;
  margin: 5px 0;
}

.property-meta {
  font-size: 0.8rem;
  color: #6c757d;
  margin: 0;
}

.bookmark-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Quick Search */
.quick-search-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-row {
  display: flex;
  gap: 10px;
}

.half {
  flex: 1;
}

.third {
  flex: 1;
}

label {
  margin-bottom: 5px;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 16px;
  height: 16px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}
</style>