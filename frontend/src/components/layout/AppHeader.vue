<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/dashboard">
              <img class="h-8 w-auto" src="@/assets/logo.svg" alt="Wealth Map" />
            </router-link>
          </div>
          <nav class="ml-6 flex space-x-8" aria-label="Main navigation">
            <router-link 
              v-for="item in navigationItems" 
              :key="item.name"
              :to="item.href"
              :class="[
                isActive(item.href) 
                  ? 'border-blue-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
              ]"
            >
              {{ item.name }}
            </router-link>
          </nav>
        </div>
        
        <div class="flex items-center">
          <div class="flex-shrink-0 relative">
            <SearchBar />
          </div>
          
          <div class="ml-4 flex items-center md:ml-6">
            <button 
              type="button" 
              class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span class="sr-only">View notifications</span>
              <BellIcon class="h-6 w-6" aria-hidden="true" />
            </button>

            <!-- Profile dropdown -->
            <div class="ml-3 relative">
              <div>
                <button 
                  @click="isProfileMenuOpen = !isProfileMenuOpen"
                  type="button" 
                  class="max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500" 
                  id="user-menu-button" 
                  aria-expanded="false" 
                  aria-haspopup="true"
                >
                  <span class="sr-only">Open user menu</span>
                  <img class="h-8 w-8 rounded-full" :src="userAvatarUrl" alt="" />
                </button>
              </div>

              <div 
                v-if="isProfileMenuOpen"
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none" 
                role="menu" 
                aria-orientation="vertical" 
                aria-labelledby="user-menu-button" 
                tabindex="-1"
              >
                <router-link 
                  v-for="item in profileMenuItems" 
                  :key="item.name"
                  :to="item.href"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1" 
                  @click="isProfileMenuOpen = false"
                >
                  {{ item.name }}
                </router-link>
                <a 
                  href="#" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1" 
                  @click="handleLogout"
                >
                  Sign out
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SearchBar from '@/components/search/SearchBar.vue'
import { BellIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const authStore = useAuthStore()
const isProfileMenuOpen = ref(false)

// Navigation items
const navigationItems = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Map', href: '/map' },
  { name: 'Reports', href: '/reports' },
  { name: 'Search', href: '/search' }
]

// Profile menu items
const profileMenuItems = computed(() => {
  const items = [
    { name: 'Your Profile', href: '/profile' }
  ]
  
  // Add admin link if user is admin
  if (authStore.isAdmin) {
    items.push({ name: 'Admin Dashboard', href: '/admin' })
  }
  
  return items
})

// User avatar URL (placeholder for now)
const userAvatarUrl = computed(() => {
  return 'https://ui-avatars.com/api/?name=' + encodeURIComponent(authStore.userName || 'User')
})

// Check if route is active
function isActive(path) {
  return route.path === path || route.path.startsWith(`${path}/`)
}

// Handle logout
function handleLogout() {
  isProfileMenuOpen.value = false
  authStore.logout()
}
</script>