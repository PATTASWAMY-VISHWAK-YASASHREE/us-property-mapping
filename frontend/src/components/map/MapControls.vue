<template>
  <div class="map-controls">
    <div class="control-group">
      <button 
        @click="$emit('zoom-in')" 
        class="control-button"
        title="Zoom In"
      >
        <i class="icon zoom-in-icon"></i>
      </button>
      <button 
        @click="$emit('zoom-out')" 
        class="control-button"
        title="Zoom Out"
      >
        <i class="icon zoom-out-icon"></i>
      </button>
    </div>
    
    <div class="control-group">
      <button 
        @click="$emit('reset-view')" 
        class="control-button"
        title="Reset View"
      >
        <i class="icon reset-icon"></i>
      </button>
      <button 
        @click="$emit('toggle-fullscreen')" 
        class="control-button"
        title="Toggle Fullscreen"
      >
        <i class="icon fullscreen-icon"></i>
      </button>
    </div>
    
    <div class="control-group">
      <button 
        @click="toggleMeasureTool" 
        class="control-button"
        :class="{ active: isMeasureActive }"
        title="Measure Distance"
      >
        <i class="icon measure-icon"></i>
      </button>
      <button 
        @click="toggleDrawTool" 
        class="control-button"
        :class="{ active: isDrawActive }"
        title="Draw Area"
      >
        <i class="icon draw-icon"></i>
      </button>
    </div>
    
    <div class="control-group">
      <button 
        @click="toggleLocationTracking" 
        class="control-button"
        :class="{ active: isLocationTrackingActive }"
        title="My Location"
      >
        <i class="icon location-icon"></i>
      </button>
      <button 
        @click="toggleStreetView" 
        class="control-button"
        :class="{ active: isStreetViewActive }"
        title="Street View"
      >
        <i class="icon street-view-icon"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Define emits
const emit = defineEmits(['zoom-in', 'zoom-out', 'reset-view', 'toggle-fullscreen', 'toggle-measure', 'toggle-draw', 'toggle-location', 'toggle-street-view']);

// State
const isMeasureActive = ref(false);
const isDrawActive = ref(false);
const isLocationTrackingActive = ref(false);
const isStreetViewActive = ref(false);

// Methods
const toggleMeasureTool = () => {
  isMeasureActive.value = !isMeasureActive.value;
  
  // Deactivate other tools
  if (isMeasureActive.value) {
    isDrawActive.value = false;
    isStreetViewActive.value = false;
  }
  
  emit('toggle-measure', isMeasureActive.value);
};

const toggleDrawTool = () => {
  isDrawActive.value = !isDrawActive.value;
  
  // Deactivate other tools
  if (isDrawActive.value) {
    isMeasureActive.value = false;
    isStreetViewActive.value = false;
  }
  
  emit('toggle-draw', isDrawActive.value);
};

const toggleLocationTracking = () => {
  isLocationTrackingActive.value = !isLocationTrackingActive.value;
  emit('toggle-location', isLocationTrackingActive.value);
};

const toggleStreetView = () => {
  isStreetViewActive.value = !isStreetViewActive.value;
  
  // Deactivate other tools
  if (isStreetViewActive.value) {
    isMeasureActive.value = false;
    isDrawActive.value = false;
  }
  
  emit('toggle-street-view', isStreetViewActive.value);
};
</script>

<style scoped>
.map-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 5;
}

.control-group {
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.control-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: white;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s;
}

.control-button:not(:last-child) {
  border-bottom: 1px solid #f0f0f0;
}

.control-button:hover {
  background-color: #f7fafc;
}

.control-button.active {
  background-color: #ebf4ff;
  color: #4a6cf7;
}

.icon {
  width: 20px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.zoom-in-icon {
  background-image: url('@/assets/icons/zoom-in.svg');
}

.zoom-out-icon {
  background-image: url('@/assets/icons/zoom-out.svg');
}

.reset-icon {
  background-image: url('@/assets/icons/reset.svg');
}

.fullscreen-icon {
  background-image: url('@/assets/icons/fullscreen.svg');
}

.measure-icon {
  background-image: url('@/assets/icons/measure.svg');
}

.draw-icon {
  background-image: url('@/assets/icons/draw.svg');
}

.location-icon {
  background-image: url('@/assets/icons/location.svg');
}

.street-view-icon {
  background-image: url('@/assets/icons/street-view.svg');
}

@media (max-width: 768px) {
  .map-controls {
    flex-direction: row;
    bottom: 20px;
    top: auto;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .control-group {
    flex-direction: row;
  }
  
  .control-button:not(:last-child) {
    border-bottom: none;
    border-right: 1px solid #f0f0f0;
  }
}
</style>