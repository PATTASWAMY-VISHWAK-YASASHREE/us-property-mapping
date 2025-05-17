<template>
  <header class="header">
    <div class="header-container">
      <div class="header-left">
        <button @click="toggleSidebar" class="menu-toggle">
          <i class="icon menu-icon"></i>
        </button>
        <div class="breadcrumbs">
          <router-link to="/" class="breadcrumb-item">Home</router-link>
          <span v-if="currentRoute.meta.breadcrumbs" class="breadcrumb-separator">/</span>
          <template v-for="(crumb, index) in currentRoute.meta.breadcrumbs" :key="index">
            <router-link 
              v-if="crumb.to" 
              :to="crumb.to" 
              class="breadcrumb-item"
            >
              {{ crumb.text }}
            </router-link>
            <span v-else class="breadcrumb-item current">{{ crumb.text }}</span>
            <span 
              v-if="index < currentRoute.meta.breadcrumbs.length - 1" 
              class="breadcrumb-separator"
            >/</span>
          </template>
        </div>
      </div>
      
      <div class="header-right">
        <div class="search-container">
          <input 
            type="text" 
            placeholder="Search..." 
            class="search-input" 
            @focus="isSearchFocused = true"
            @blur="onSearchBlur"
            v-model="searchQuery"
          />
          <button class="search-button">
            <i class="icon search-icon"></i>
          </button>
          <div v-if="isSearchFocused && searchQuery" class="search-results">
            <div class="search-results-header">
              <span>Search Results</span>
              <button @click="clearSearch" class="clear-search">Clear</button>
            </div>
            <div class="search-results-content">
              <div v-if="isSearching" class="searching-indicator">
                Searching...
              </div>
              <div v-else-if="searchResults.length === 0" class="no-results">
                No results found for "{{ searchQuery }}"
              </div>
              <ul v-else class="results-list">
                <li v-for="result in searchResults" :key="result.id" class="result-item">
                  <router-link :to="result.link" class="result-link">
                    <div class="result-title">{{ result.title }}</div>
                    <div class="result-description">{{ result.description }}</div>
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <NotificationCenter />
        <UserMenu />
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import NotificationCenter from './NotificationCenter.vue';
import UserMenu from './UserMenu.vue';

const route = useRoute();
const currentRoute = computed(() => route);

const isSearchFocused = ref(false);
const searchQuery = ref('');
const isSearching = ref(false);
const searchResults = ref([]);

// Mock search results
const mockResults = [
  { 
    id: 1, 
    title: 'Property #1234', 
    description: '123 Main St, San Francisco, CA', 
    link: '/properties/1234' 
  },
  { 
    id: 2, 
    title: 'Wealth Analysis Report', 
    description: 'Q2 2023 Analysis for Downtown Area', 
    link: '/reports/wealth-analysis-q2-2023' 
  },
  { 
    id: 3, 
    title: 'Market Trends', 
    description: 'Current market trends in residential properties', 
    link: '/market-trends' 
  }
];

// Watch for changes in search query
watch(searchQuery, (newQuery) => {
  if (newQuery.length > 2) {
    performSearch(newQuery);
  } else {
    searchResults.value = [];
  }
});

// Simulate search functionality
const performSearch = (query) => {
  isSearching.value = true;
  
  // Simulate API delay
  setTimeout(() => {
    // Filter mock results based on query
    searchResults.value = mockResults.filter(result => 
      result.title.toLowerCase().includes(query.toLowerCase()) || 
      result.description.toLowerCase().includes(query.toLowerCase())
    );
    
    isSearching.value = false;
  }, 500);
};

const onSearchBlur = () => {
  // Small delay to allow clicking on search results
  setTimeout(() => {
    isSearchFocused.value = false;
  }, 200);
};

const clearSearch = () => {
  searchQuery.value = '';
  searchResults.value = [];
};

// Toggle sidebar (emits event to parent component)
const toggleSidebar = () => {
  document.body.classList.toggle('sidebar-collapsed');
};
</script>

<style scoped>
.header {
  height: 64px;
  background-color: white;
  border-bottom: 1px solid #e2e8f0;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 1.5rem;
}

.header-left {
  display: flex;
  align-items: center;
}

.menu-toggle {
  background: none;
  border: none;
  color: #4a5568;
  cursor: pointer;
  padding: 0.5rem;
  margin-right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.menu-toggle:hover {
  background-color: #f7fafc;
}

.icon {
  width: 20px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.menu-icon {
  background-image: url('@/assets/icons/menu.svg');
}

.search-icon {
  background-image: url('@/assets/icons/search.svg');
}

.breadcrumbs {
  display: flex;
  align-items: center;
}

.breadcrumb-item {
  color: #4a5568;
  text-decoration: none;
  font-size: 0.875rem;
}

.breadcrumb-item:not(.current):hover {
  color: #4a6cf7;
  text-decoration: underline;
}

.breadcrumb-item.current {
  color: #718096;
}

.breadcrumb-separator {
  margin: 0 0.5rem;
  color: #cbd5e0;
}

.header-right {
  display: flex;
  align-items: center;
}

.search-container {
  position: relative;
  margin-right: 1rem;
}

.search-input {
  width: 240px;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.875rem;
  transition: width 0.3s, box-shadow 0.3s;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
  width: 300px;
}

.search-button {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 0.25rem;
}

.search-results {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  width: 350px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.search-results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  font-weight: 500;
  color: #4a5568;
}

.clear-search {
  background: none;
  border: none;
  color: #4a6cf7;
  font-size: 0.75rem;
  cursor: pointer;
}

.search-results-content {
  max-height: 300px;
  overflow-y: auto;
}

.searching-indicator, .no-results {
  padding: 1rem;
  text-align: center;
  color: #718096;
  font-size: 0.875rem;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.result-item {
  border-bottom: 1px solid #f7fafc;
}

.result-item:last-child {
  border-bottom: none;
}

.result-link {
  display: block;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: inherit;
}

.result-link:hover {
  background-color: #f7fafc;
}

.result-title {
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.result-description {
  font-size: 0.75rem;
  color: #718096;
}

@media (max-width: 768px) {
  .breadcrumbs {
    display: none;
  }
  
  .search-input {
    width: 180px;
  }
  
  .search-input:focus {
    width: 220px;
  }
  
  .search-results {
    width: 280px;
  }
}
</style>