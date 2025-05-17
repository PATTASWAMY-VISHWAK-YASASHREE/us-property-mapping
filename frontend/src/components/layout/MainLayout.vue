<template>
  <div class="main-layout">
    <Sidebar class="sidebar" />
    <div class="content-wrapper">
      <Header class="header" />
      <main class="main-content">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue';
import Header from './Header.vue';
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f7fafc;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  background-color: #2d3748;
  color: white;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 64px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 5;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
  }
  
  .header {
    position: sticky;
    top: 0;
  }
}
</style>