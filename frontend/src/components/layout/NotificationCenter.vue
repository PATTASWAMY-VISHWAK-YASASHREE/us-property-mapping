<template>
  <div class="notification-center">
    <button 
      @click="toggleNotifications" 
      class="notification-button"
      :class="{ 'has-unread': hasUnreadNotifications }"
    >
      <i class="icon bell-icon"></i>
      <span v-if="hasUnreadNotifications" class="notification-badge">{{ unreadCount }}</span>
    </button>
    
    <div v-if="isOpen" class="notifications-panel">
      <div class="notifications-header">
        <h3>Notifications</h3>
        <div class="header-actions">
          <button 
            v-if="hasUnreadNotifications" 
            @click="markAllAsRead" 
            class="mark-all-read"
          >
            Mark all as read
          </button>
          <button @click="toggleNotifications" class="close-button">
            <i class="icon close-icon"></i>
          </button>
        </div>
      </div>
      
      <div class="notifications-tabs">
        <button 
          @click="activeTab = 'all'" 
          :class="{ active: activeTab === 'all' }"
          class="tab-button"
        >
          All
        </button>
        <button 
          @click="activeTab = 'unread'" 
          :class="{ active: activeTab === 'unread' }"
          class="tab-button"
        >
          Unread
        </button>
      </div>
      
      <div class="notifications-list">
        <div v-if="filteredNotifications.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <p>No notifications to display</p>
        </div>
        
        <template v-else>
          <div 
            v-for="notification in filteredNotifications" 
            :key="notification.id"
            class="notification-item"
            :class="{ unread: !notification.read }"
          >
            <div class="notification-icon" :class="notification.type">
              <i :class="getIconClass(notification.type)"></i>
            </div>
            <div class="notification-content">
              <div class="notification-message" v-html="notification.message"></div>
              <div class="notification-meta">
                <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
                <button 
                  v-if="!notification.read" 
                  @click="markAsRead(notification.id)" 
                  class="mark-read"
                >
                  Mark as read
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
      
      <div class="notifications-footer">
        <router-link to="/notifications" class="view-all">
          View all notifications
        </router-link>
        <router-link to="/settings/notifications" class="settings-link">
          Notification settings
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// State
const isOpen = ref(false);
const activeTab = ref('all');
const notifications = ref([]);

// Mock notifications data
const mockNotifications = [
  {
    id: 1,
    type: 'info',
    message: 'New property added to your watchlist: <strong>123 Main St</strong>',
    timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
    read: false
  },
  {
    id: 2,
    type: 'success',
    message: 'Your report <strong>Q2 Market Analysis</strong> has been generated',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    read: false
  },
  {
    id: 3,
    type: 'warning',
    message: 'Property value alert: <strong>456 Oak Ave</strong> has decreased by 5%',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5), // 5 hours ago
    read: true
  },
  {
    id: 4,
    type: 'error',
    message: 'Failed to sync data with external service',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
    read: true
  },
  {
    id: 5,
    type: 'info',
    message: 'System maintenance scheduled for tomorrow at 2:00 AM',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 48), // 2 days ago
    read: true
  }
];

// Load notifications
onMounted(() => {
  // In a real app, you would fetch notifications from an API
  notifications.value = mockNotifications;
  
  // Add event listener to close panel when clicking outside
  document.addEventListener('click', handleOutsideClick);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick);
});

// Computed properties
const hasUnreadNotifications = computed(() => {
  return notifications.value.some(notification => !notification.read);
});

const unreadCount = computed(() => {
  return notifications.value.filter(notification => !notification.read).length;
});

const filteredNotifications = computed(() => {
  if (activeTab.value === 'unread') {
    return notifications.value.filter(notification => !notification.read);
  }
  return notifications.value;
});

// Methods
const toggleNotifications = () => {
  isOpen.value = !isOpen.value;
};

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id);
  if (notification) {
    notification.read = true;
  }
};

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true;
  });
};

const handleOutsideClick = (event) => {
  const notificationCenter = event.target.closest('.notification-center');
  if (!notificationCenter && isOpen.value) {
    isOpen.value = false;
  }
};

const getIconClass = (type) => {
  const iconMap = {
    info: 'info-icon',
    success: 'success-icon',
    warning: 'warning-icon',
    error: 'error-icon'
  };
  return iconMap[type] || 'info-icon';
};

const formatTime = (timestamp) => {
  const now = new Date();
  const diff = now - timestamp;
  
  // Less than a minute
  if (diff < 60000) {
    return 'Just now';
  }
  
  // Less than an hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000);
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  }
  
  // Less than a day
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  }
  
  // Less than a week
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000);
    return `${days} day${days > 1 ? 's' : ''} ago`;
  }
  
  // Format as date
  return timestamp.toLocaleDateString();
};
</script>

<style scoped>
.notification-center {
  position: relative;
}

.notification-button {
  position: relative;
  background: none;
  border: none;
  color: #4a5568;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 40px;
  height: 40px;
}

.notification-button:hover {
  background-color: #f7fafc;
}

.notification-button.has-unread {
  color: #4a6cf7;
}

.bell-icon {
  background-image: url('@/assets/icons/bell.svg');
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #e53e3e;
  color: white;
  font-size: 0.75rem;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notifications-panel {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 360px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  z-index: 100;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.notifications-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
}

.header-actions {
  display: flex;
  align-items: center;
}

.mark-all-read {
  background: none;
  border: none;
  color: #4a6cf7;
  font-size: 0.75rem;
  cursor: pointer;
  margin-right: 0.5rem;
}

.close-button {
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-icon {
  background-image: url('@/assets/icons/close.svg');
}

.notifications-tabs {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
}

.tab-button {
  flex: 1;
  background: none;
  border: none;
  padding: 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
  color: #718096;
  border-bottom: 2px solid transparent;
}

.tab-button.active {
  color: #4a6cf7;
  border-bottom-color: #4a6cf7;
  font-weight: 500;
}

.notifications-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #a0aec0;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.notification-item {
  display: flex;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f7fafc;
  transition: background-color 0.2s;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background-color: #f7fafc;
}

.notification-item.unread {
  background-color: #ebf4ff;
}

.notification-item.unread:hover {
  background-color: #e6f0fd;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.notification-icon.info {
  background-color: #ebf8ff;
  color: #3182ce;
}

.notification-icon.success {
  background-color: #f0fff4;
  color: #38a169;
}

.notification-icon.warning {
  background-color: #fffaf0;
  color: #dd6b20;
}

.notification-icon.error {
  background-color: #fff5f5;
  color: #e53e3e;
}

.notification-content {
  flex: 1;
}

.notification-message {
  font-size: 0.875rem;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.notification-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.notification-time {
  color: #a0aec0;
}

.mark-read {
  background: none;
  border: none;
  color: #4a6cf7;
  cursor: pointer;
  padding: 0;
  font-size: 0.75rem;
}

.notifications-footer {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-top: 1px solid #e2e8f0;
  font-size: 0.75rem;
}

.view-all, .settings-link {
  color: #4a6cf7;
  text-decoration: none;
}

.view-all:hover, .settings-link:hover {
  text-decoration: underline;
}

/* Icon classes */
.info-icon {
  background-image: url('@/assets/icons/info.svg');
}

.success-icon {
  background-image: url('@/assets/icons/check.svg');
}

.warning-icon {
  background-image: url('@/assets/icons/warning.svg');
}

.error-icon {
  background-image: url('@/assets/icons/error.svg');
}
</style>