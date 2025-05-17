<template>
  <aside class="sidebar">
    <div class="logo-container">
      <router-link to="/" class="logo">
        <img src="@/assets/logo.svg" alt="Wealth Map" />
        <span>Wealth Map</span>
      </router-link>
    </div>
    
    <nav class="navigation">
      <ul class="nav-list">
        <li class="nav-item">
          <router-link to="/dashboard" class="nav-link">
            <i class="icon dashboard-icon"></i>
            <span>Dashboard</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/properties" class="nav-link">
            <i class="icon property-icon"></i>
            <span>Properties</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/map" class="nav-link">
            <i class="icon map-icon"></i>
            <span>Map</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/wealth-analysis" class="nav-link">
            <i class="icon analysis-icon"></i>
            <span>Wealth Analysis</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/reports" class="nav-link">
            <i class="icon reports-icon"></i>
            <span>Reports</span>
          </router-link>
        </li>
      </ul>
    </nav>
    
    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">
          <img src="@/assets/default-avatar.png" alt="User Avatar" />
        </div>
        <div class="user-details">
          <span class="user-name">{{ userName }}</span>
          <span class="user-role">{{ userRole }}</span>
        </div>
      </div>
      
      <div class="sidebar-actions">
        <button @click="toggleSidebar" class="toggle-button">
          <i class="icon collapse-icon"></i>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const isCollapsed = ref(false);

// Mock user data - in a real app, this would come from the auth store
const userName = ref('John Doe');
const userRole = ref('Administrator');

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  document.body.classList.toggle('sidebar-collapsed', isCollapsed.value);
};

onMounted(() => {
  // Check if sidebar was collapsed in previous session
  const savedState = localStorage.getItem('sidebarCollapsed');
  if (savedState === 'true') {
    isCollapsed.value = true;
    document.body.classList.add('sidebar-collapsed');
  }
});
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #2d3748;
  color: #e2e8f0;
  transition: width 0.3s ease;
}

.logo-container {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 1.25rem;
}

.logo img {
  height: 32px;
  margin-right: 0.75rem;
}

.navigation {
  flex: 1;
  padding: 1.5rem 0;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: #cbd5e0;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border-left-color: #4a6cf7;
}

.icon {
  width: 20px;
  height: 20px;
  margin-right: 0.75rem;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.dashboard-icon {
  background-image: url('@/assets/icons/dashboard.svg');
}

.property-icon {
  background-image: url('@/assets/icons/property.svg');
}

.map-icon {
  background-image: url('@/assets/icons/map.svg');
}

.analysis-icon {
  background-image: url('@/assets/icons/analysis.svg');
}

.reports-icon {
  background-image: url('@/assets/icons/reports.svg');
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  padding: 0.5rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 0.75rem;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: white;
}

.user-role {
  font-size: 0.75rem;
  color: #a0aec0;
}

.sidebar-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.toggle-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.toggle-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.collapse-icon {
  background-image: url('@/assets/icons/collapse.svg');
}

/* Responsive styles */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
  }
  
  .sidebar-footer {
    display: none;
  }
}

/* Collapsed sidebar styles */
:global(.sidebar-collapsed) .sidebar {
  width: 70px;
}

:global(.sidebar-collapsed) .logo span,
:global(.sidebar-collapsed) .nav-link span,
:global(.sidebar-collapsed) .user-details {
  display: none;
}

:global(.sidebar-collapsed) .nav-link {
  justify-content: center;
  padding: 0.75rem;
}

:global(.sidebar-collapsed) .icon {
  margin-right: 0;
}

:global(.sidebar-collapsed) .user-info {
  justify-content: center;
}

:global(.sidebar-collapsed) .user-avatar {
  margin-right: 0;
}
</style>