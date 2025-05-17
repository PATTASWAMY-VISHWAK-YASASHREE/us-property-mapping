<template>
  <div class="app-container">
    <header v-if="isAuthenticated && !isFullScreenRoute">
      <AppHeader />
    </header>
    
    <main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer v-if="isAuthenticated && !isFullScreenRoute">
      <AppFooter />
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'

const route = useRoute()
const authStore = useAuthStore()

// Check if user is authenticated
const isAuthenticated = computed(() => authStore.isAuthenticated)

// Check if current route should be displayed in full screen (no header/footer)
const isFullScreenRoute = computed(() => {
  return ['/login', '/register', '/forgot-password'].includes(route.path)
})
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>