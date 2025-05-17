<template>
  <div class="user-menu">
    <button @click="toggleMenu" class="user-button">
      <div class="user-avatar">
        <img :src="userAvatarUrl" :alt="userName" />
        <span v-if="isUserOnline" class="status-indicator online"></span>
      </div>
      <div class="user-info">
        <span class="user-name">{{ userName }}</span>
        <span class="user-role">{{ userRole }}</span>
      </div>
      <i class="icon chevron-icon" :class="{ 'rotated': isMenuOpen }"></i>
    </button>
    
    <div v-if="isMenuOpen" class="dropdown-menu">
      <div class="menu-header">
        <div class="user-avatar large">
          <img :src="userAvatarUrl" :alt="userName" />
          <span v-if="isUserOnline" class="status-indicator online"></span>
        </div>
        <div class="user-details">
          <div class="user-name">{{ userName }}</div>
          <div class="user-email">{{ userEmail }}</div>
          <div class="user-role">{{ userRole }}</div>
        </div>
      </div>
      
      <div class="menu-items">
        <router-link to="/profile" class="menu-item">
          <i class="icon profile-icon"></i>
          <span>My Profile</span>
        </router-link>
        <router-link to="/settings/account" class="menu-item">
          <i class="icon settings-icon"></i>
          <span>Account Settings</span>
        </router-link>
        <router-link to="/settings/security" class="menu-item">
          <i class="icon security-icon"></i>
          <span>Security</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin" class="menu-item">
          <i class="icon admin-icon"></i>
          <span>Admin Dashboard</span>
        </router-link>
        <div class="menu-divider"></div>
        <router-link to="/help" class="menu-item">
          <i class="icon help-icon"></i>
          <span>Help & Support</span>
        </router-link>
        <button @click="handleLogout" class="menu-item logout">
          <i class="icon logout-icon"></i>
          <span>Logout</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const isMenuOpen = ref(false);

// Mock user data - in a real app, this would come from the auth store
const userName = computed(() => authStore.userName || 'John Doe');
const userEmail = computed(() => authStore.userEmail || 'john.doe@example.com');
const userRole = computed(() => authStore.userRole || 'Administrator');
const isAdmin = computed(() => authStore.isAdmin || true);
const isUserOnline = ref(true);

// Generate avatar URL
const userAvatarUrl = computed(() => {
  // In a real app, you would use the user's actual avatar URL
  // For now, we'll use a placeholder service
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(userName.value)}&background=4a6cf7&color=fff`;
});

// Toggle dropdown menu
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Handle logout
const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

// Close menu when clicking outside
const handleOutsideClick = (event) => {
  const userMenuEl = event.target.closest('.user-menu');
  if (!userMenuEl && isMenuOpen.value) {
    isMenuOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleOutsideClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick);
});
</script>

<style scoped>
.user-menu {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-button:hover {
  background-color: #f7fafc;
}

.user-avatar {
  position: relative;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-indicator {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-indicator.online {
  background-color: #48bb78;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 0.5rem;
  display: none; /* Hidden by default on small screens */
}

.user-name {
  font-weight: 500;
  color: #2d3748;
  font-size: 0.875rem;
}

.user-role {
  font-size: 0.75rem;
  color: #718096;
}

.chevron-icon {
  background-image: url('@/assets/icons/chevron-down.svg');
  transition: transform 0.2s;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 280px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  z-index: 100;
  overflow: hidden;
}

.menu-header {
  display: flex;
  padding: 1rem;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.user-avatar.large {
  width: 48px;
  height: 48px;
}

.user-details {
  margin-left: 0.75rem;
}

.user-email {
  font-size: 0.75rem;
  color: #718096;
  margin: 0.25rem 0;
}

.menu-items {
  padding: 0.5rem 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #4a5568;
  text-decoration: none;
  transition: background-color 0.2s;
  cursor: pointer;
}

.menu-item:hover {
  background-color: #f7fafc;
}

.menu-item i {
  margin-right: 0.75rem;
}

.menu-divider {
  height: 1px;
  background-color: #e2e8f0;
  margin: 0.5rem 0;
}

.logout {
  color: #e53e3e;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-size: 1rem;
}

/* Icon classes */
.profile-icon {
  background-image: url('@/assets/icons/user.svg');
}

.settings-icon {
  background-image: url('@/assets/icons/settings.svg');
}

.security-icon {
  background-image: url('@/assets/icons/shield.svg');
}

.admin-icon {
  background-image: url('@/assets/icons/admin.svg');
}

.help-icon {
  background-image: url('@/assets/icons/help.svg');
}

.logout-icon {
  background-image: url('@/assets/icons/logout.svg');
}

/* Responsive styles */
@media (min-width: 640px) {
  .user-info {
    display: flex;
  }
}
</style>