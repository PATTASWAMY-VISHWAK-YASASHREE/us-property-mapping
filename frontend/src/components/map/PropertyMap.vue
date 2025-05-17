<template>
  <div class="property-map-container">
    <div class="map-overlay" v-if="isLoading">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading map data...</div>
    </div>
    
    <div ref="mapContainer" class="map-container"></div>
    
    <MapControls 
      @zoom-in="zoomIn"
      @zoom-out="zoomOut"
      @reset-view="resetView"
      @toggle-fullscreen="toggleFullscreen"
    />
    
    <MapLayerSelector 
      :available-layers="availableLayers"
      :active-layers="activeLayers"
      @layer-toggle="toggleLayer"
    />
    
    <div v-if="selectedProperty" class="property-info-card">
      <div class="card-header">
        <h3>{{ selectedProperty.address }}</h3>
        <button @click="closePropertyInfo" class="close-button">×</button>
      </div>
      <div class="card-body">
        <div class="property-image">
          <img :src="selectedProperty.imageUrl" :alt="selectedProperty.address" />
        </div>
        <div class="property-details">
          <div class="detail-item">
            <span class="label">Price:</span>
            <span class="value">${{ formatNumber(selectedProperty.price) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Size:</span>
            <span class="value">{{ selectedProperty.size }} sq ft</span>
          </div>
          <div class="detail-item">
            <span class="label">Type:</span>
            <span class="value">{{ selectedProperty.type }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Year Built:</span>
            <span class="value">{{ selectedProperty.yearBuilt }}</span>
          </div>
        </div>
      </div>
      <div class="card-footer">
        <router-link :to="`/properties/${selectedProperty.id}`" class="view-details-btn">
          View Details
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import MapControls from './MapControls.vue';
import MapLayerSelector from './MapLayerSelector.vue';
import PropertyMarker from './PropertyMarker.vue';
import PropertyCluster from './PropertyCluster.vue';

// Props
const props = defineProps({
  initialCenter: {
    type: Object,
    default: () => ({ lat: 37.7749, lng: -122.4194 }) // Default to San Francisco
  },
  initialZoom: {
    type: Number,
    default: 12
  },
  properties: {
    type: Array,
    default: () => []
  },
  height: {
    type: String,
    default: '600px'
  }
});

// Refs
const mapContainer = ref(null);
const map = ref(null);
const markers = ref([]);
const clusters = ref([]);
const isLoading = ref(true);
const selectedProperty = ref(null);
const isFullscreen = ref(false);

// Map layers
const availableLayers = ref([
  { id: 'satellite', name: 'Satellite', active: false },
  { id: 'traffic', name: 'Traffic', active: false },
  { id: 'transit', name: 'Transit', active: false },
  { id: 'bicycling', name: 'Bicycling', active: false },
  { id: 'wealth-heatmap', name: 'Wealth Heatmap', active: true },
  { id: 'property-values', name: 'Property Values', active: true }
]);

const activeLayers = ref(['wealth-heatmap', 'property-values']);

// Initialize map
onMounted(() => {
  // In a real application, you would initialize a map library like Google Maps, Mapbox, or Leaflet here
  initializeMap();
});

// Clean up
onBeforeUnmount(() => {
  // Clean up map instance if needed
  if (map.value) {
    // map.value.remove(); // Example for Mapbox or Leaflet
  }
});

// Watch for property changes
watch(() => props.properties, (newProperties) => {
  updateMarkers(newProperties);
}, { deep: true });

// Methods
const initializeMap = () => {
  // Simulate map initialization
  setTimeout(() => {
    // In a real app, you would initialize your map library here
    // Example for Google Maps:
    // map.value = new google.maps.Map(mapContainer.value, {
    //   center: props.initialCenter,
    //   zoom: props.initialZoom,
    //   mapTypeId: google.maps.MapTypeId.ROADMAP
    // });
    
    console.log('Map initialized');
    isLoading.value = false;
    
    // Add markers for properties
    updateMarkers(props.properties);
  }, 1000);
};

const updateMarkers = (properties) => {
  // Clear existing markers
  clearMarkers();
  
  // Add new markers
  properties.forEach(property => {
    addMarker(property);
  });
  
  // Create clusters
  createClusters();
};

const addMarker = (property) => {
  // In a real app, you would create actual map markers
  // Example for Google Maps:
  // const marker = new google.maps.Marker({
  //   position: { lat: property.latitude, lng: property.longitude },
  //   map: map.value,
  //   title: property.address
  // });
  // 
  // marker.addListener('click', () => {
  //   selectProperty(property);
  // });
  // 
  // markers.value.push(marker);
  
  console.log(`Added marker for property: ${property.address}`);
};

const clearMarkers = () => {
  // In a real app, you would remove markers from the map
  // markers.value.forEach(marker => marker.setMap(null));
  markers.value = [];
};

const createClusters = () => {
  // In a real app, you would create marker clusters
  // Example for Google Maps with MarkerClusterer:
  // const markerCluster = new MarkerClusterer(map.value, markers.value, {
  //   imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
  // });
  
  console.log('Created marker clusters');
};

const selectProperty = (property) => {
  selectedProperty.value = property;
};

const closePropertyInfo = () => {
  selectedProperty.value = null;
};

const zoomIn = () => {
  // In a real app, you would zoom in the map
  // map.value.setZoom(map.value.getZoom() + 1);
  console.log('Zoom in');
};

const zoomOut = () => {
  // In a real app, you would zoom out the map
  // map.value.setZoom(map.value.getZoom() - 1);
  console.log('Zoom out');
};

const resetView = () => {
  // In a real app, you would reset the map view
  // map.value.setCenter(props.initialCenter);
  // map.value.setZoom(props.initialZoom);
  console.log('Reset view');
};

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value;
  
  if (isFullscreen.value) {
    // Request fullscreen
    if (mapContainer.value.requestFullscreen) {
      mapContainer.value.requestFullscreen();
    } else if (mapContainer.value.mozRequestFullScreen) {
      mapContainer.value.mozRequestFullScreen();
    } else if (mapContainer.value.webkitRequestFullscreen) {
      mapContainer.value.webkitRequestFullscreen();
    } else if (mapContainer.value.msRequestFullscreen) {
      mapContainer.value.msRequestFullscreen();
    }
  } else {
    // Exit fullscreen
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  }
};

const toggleLayer = (layerId) => {
  const layerIndex = activeLayers.value.indexOf(layerId);
  
  if (layerIndex === -1) {
    // Add layer
    activeLayers.value.push(layerId);
  } else {
    // Remove layer
    activeLayers.value.splice(layerIndex, 1);
  }
  
  // Update layer visibility on the map
  updateLayerVisibility();
};

const updateLayerVisibility = () => {
  // In a real app, you would update the visibility of map layers
  // Example for Google Maps:
  // availableLayers.value.forEach(layer => {
  //   const isActive = activeLayers.value.includes(layer.id);
  //   // Update layer visibility based on isActive
  // });
  
  console.log('Updated layer visibility:', activeLayers.value);
};

// Utility functions
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
</script>

<style scoped>
.property-map-container {
  position: relative;
  width: 100%;
  height: v-bind('props.height');
  background-color: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a6cf7;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1rem;
  color: #4a5568;
}

.property-info-card {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 300px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 5;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #718096;
  cursor: pointer;
}

.card-body {
  padding: 1rem;
}

.property-image {
  width: 100%;
  height: 150px;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.property-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.75rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.value {
  font-weight: 500;
  color: #2d3748;
}

.card-footer {
  padding: 0.75rem 1rem;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.view-details-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #4a6cf7;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.view-details-btn:hover {
  background-color: #3a5ce5;
}
</style>