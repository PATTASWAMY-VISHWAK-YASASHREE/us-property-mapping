<template>
  <div class="search-bar-container">
    <div class="relative">
      <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </div>
      
      <input
        v-model="searchQuery"
        type="text"
        class="block w-full rounded-md border-0 py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
        placeholder="Search properties, owners, addresses..."
        @keyup.enter="performSearch"
        @input="handleInput"
        @focus="showSuggestions = true"
        @blur="hideSuggestionsDelayed"
      />
      
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="absolute inset-y-0 right-0 flex items-center pr-3"
      >
        <XMarkIcon class="h-5 w-5 text-gray-400 hover:text-gray-500" aria-hidden="true" />
      </button>
    </div>
    
    <!-- Search suggestions -->
    <div
      v-if="showSuggestions && (suggestions.length > 0 || recentSearches.length > 0)"
      class="absolute z-10 mt-1 w-full rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
    >
      <div class="py-1 max-h-60 overflow-auto">
        <!-- Recent searches -->
        <div v-if="recentSearches.length > 0" class="px-3 py-1 text-xs font-semibold text-gray-500">
          Recent Searches
        </div>
        <a
          v-for="(search, index) in recentSearches"
          :key="'recent-' + index"
          href="#"
          class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          @mousedown.prevent="selectRecentSearch(search)"
        >
          <ClockIcon class="mr-2 h-4 w-4 text-gray-400" aria-hidden="true" />
          {{ search }}
        </a>
        
        <!-- Divider -->
        <div v-if="recentSearches.length > 0 && suggestions.length > 0" class="border-t border-gray-100 my-1"></div>
        
        <!-- Suggestions -->
        <div v-if="suggestions.length > 0" class="px-3 py-1 text-xs font-semibold text-gray-500">
          Suggestions
        </div>
        <a
          v-for="(suggestion, index) in suggestions"
          :key="'suggestion-' + index"
          href="#"
          class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          @mousedown.prevent="selectSuggestion(suggestion)"
        >
          <component :is="getSuggestionIcon(suggestion.type)" class="mr-2 h-4 w-4 text-gray-400" aria-hidden="true" />
          <div>
            <div>{{ suggestion.text }}</div>
            <div class="text-xs text-gray-500">{{ getSuggestionSubtext(suggestion) }}</div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertyStore } from '@/stores/property'
import { useWealthStore } from '@/stores/wealth'
import { MagnifyingGlassIcon, XMarkIcon, ClockIcon, HomeIcon, UserIcon, MapPinIcon } from '@heroicons/vue/24/outline'
import { debounce } from '@/utils/helpers'

const router = useRouter()
const propertyStore = usePropertyStore()
const wealthStore = useWealthStore()

// State
const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const recentSearches = ref([])
const isLoading = ref(false)

// Load recent searches from localStorage
onMounted(() => {
  try {
    const saved = localStorage.getItem('recentSearches')
    if (saved) {
      recentSearches.value = JSON.parse(saved)
    }
  } catch (e) {
    console.error('Failed to load recent searches:', e)
  }
})

// Debounced search function
const fetchSuggestions = debounce(async (query) => {
  if (!query || query.length < 2) {
    suggestions.value = []
    return
  }
  
  isLoading.value = true
  
  try {
    // Use Promise.all for parallel requests to improve performance
    const [propertyResults, ownerResults] = await Promise.all([
      propertyStore.searchProperties(query),
      wealthStore.searchOwners(query)
    ])
    
    // Combine and format suggestions
    // Limit results to improve rendering performance
    suggestions.value = [
      ...propertyResults.slice(0, 3).map(property => ({
        type: 'property',
        id: property.id,
        text: property.address,
        subtext: `${property.city}, ${property.state}`,
        data: property
      })),
      ...ownerResults.slice(0, 3).map(owner => ({
        type: 'owner',
        id: owner.id,
        text: owner.name,
        subtext: owner.netWorth ? `Net Worth: ${owner.netWorth}` : 'Owner',
        data: owner
      }))
    ]
  } catch (error) {
    console.error('Error fetching suggestions:', error)
    suggestions.value = []
  } finally {
    isLoading.value = false
  }
}, 300)

// Handle input changes
function handleInput() {
  if (searchQuery.value) {
    fetchSuggestions(searchQuery.value)
  } else {
    suggestions.value = []
  }
}

// Perform search
function performSearch() {
  if (!searchQuery.value) return
  
  // Add to recent searches
  addToRecentSearches(searchQuery.value)
  
  // Navigate to search results page
  router.push({
    path: '/search',
    query: { q: searchQuery.value }
  })
  
  // Clear suggestions
  suggestions.value = []
  showSuggestions.value = false
}

// Clear search
function clearSearch() {
  searchQuery.value = ''
  suggestions.value = []
}

// Select suggestion
function selectSuggestion(suggestion) {
  // Add to recent searches
  addToRecentSearches(suggestion.text)
  
  // Navigate based on suggestion type
  if (suggestion.type === 'property') {
    router.push(`/property/${suggestion.id}`)
  } else if (suggestion.type === 'owner') {
    router.push(`/owner/${suggestion.id}`)
  }
  
  // Clear search
  searchQuery.value = ''
  suggestions.value = []
  showSuggestions.value = false
}

// Select recent search
function selectRecentSearch(search) {
  searchQuery.value = search
  performSearch()
}

// Add to recent searches
function addToRecentSearches(search) {
  // Remove if already exists
  recentSearches.value = recentSearches.value.filter(item => item !== search)
  
  // Add to beginning of array
  recentSearches.value.unshift(search)
  
  // Keep only the last 5 items
  if (recentSearches.value.length > 5) {
    recentSearches.value = recentSearches.value.slice(0, 5)
  }
  
  // Save to localStorage
  try {
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value))
  } catch (e) {
    console.error('Failed to save recent searches:', e)
  }
}

// Hide suggestions with delay (to allow click events)
const hideSuggestionsDelayed = debounce(() => {
  showSuggestions.value = false
}, 200)

// Get icon for suggestion type
function getSuggestionIcon(type) {
  switch (type) {
    case 'property':
      return HomeIcon
    case 'owner':
      return UserIcon
    default:
      return MapPinIcon
  }
}

// Get subtext for suggestion
function getSuggestionSubtext(suggestion) {
  return suggestion.subtext || ''
}
</script>

<style scoped>
.search-bar-container {
  position: relative;
  width: 300px;
}

@media (max-width: 640px) {
  .search-bar-container {
    width: 100%;
  }
}
</style>