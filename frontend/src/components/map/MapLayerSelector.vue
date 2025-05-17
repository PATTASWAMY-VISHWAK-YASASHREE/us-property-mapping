<template>
  <div class="map-layer-selector">
    <button @click="toggleLayerPanel" class="layer-toggle-button">
      <i class="icon layers-icon"></i>
      <span class="button-text">Layers</span>
    </button>
    
    <div v-if="isOpen" class="layer-panel">
      <div class="panel-header">
        <h3>Map Layers</h3>
        <button @click="toggleLayerPanel" class="close-button">
          <i class="icon close-icon"></i>
        </button>
      </div>
      
      <div class="layer-groups">
        <div class="layer-group">
          <h4>Base Maps</h4>
          <div class="layer-options">
            <div 
              v-for="layer in baseMaps" 
              :key="layer.id"
              class="layer-option"
            >
              <label :for="layer.id" class="layer-label">
                <input 
                  type="radio" 
                  :id="layer.id" 
                  name="baseMap" 
                  :value="layer.id" 
                  :checked="layer.id === activeBaseMap"
                  @change="setBaseMap(layer.id)"
                />
                <span class="layer-name">{{ layer.name }}</span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="layer-group">
          <h4>Data Layers</h4>
          <div class="layer-options">
            <div 
              v-for="layer in dataLayers" 
              :key="layer.id"
              class="layer-option"
            >
              <label :for="layer.id" class="layer-label">
                <input 
                  type="checkbox" 
                  :id="layer.id" 
                  :checked="isLayerActive(layer.id)"
                  @change="toggleLayer(layer.id)"
                />
                <span class="layer-name">{{ layer.name }}</span>
              </label>
              <div v-if="layer.hasOpacity" class="layer-opacity">
                <input 
                  type="range" 
                  :min="0" 
                  :max="100" 
                  :value="getLayerOpacity(layer.id)" 
                  @input="setLayerOpacity(layer.id, $event.target.value)"
                />
                <span class="opacity-value">{{ getLayerOpacity(layer.id) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="panel-footer">
        <button @click="resetLayers" class="reset-button">Reset to Default</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  availableLayers: {
    type: Array,
    default: () => []
  },
  activeLayers: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['layer-toggle', 'base-map-change', 'layer-opacity-change', 'reset']);

const isOpen = ref(false);
const activeBaseMap = ref('standard');
const layerOpacity = ref({});

// Predefined base maps
const baseMaps = [
  { id: 'standard', name: 'Standard' },
  { id: 'satellite', name: 'Satellite' },
  { id: 'terrain', name: 'Terrain' },
  { id: 'dark', name: 'Dark Mode' }
];

// Computed data layers from props
const dataLayers = computed(() => {
  return props.availableLayers.map(layer => ({
    ...layer,
    hasOpacity: ['wealth-heatmap', 'property-values', 'demographics'].includes(layer.id)
  }));
});

// Check if a layer is active
const isLayerActive = (layerId) => {
  return props.activeLayers.includes(layerId);
};

// Get layer opacity (default to 100%)
const getLayerOpacity = (layerId) => {
  return layerOpacity.value[layerId] || 100;
};

// Toggle the layer panel
const toggleLayerPanel = () => {
  isOpen.value = !isOpen.value;
};

// Toggle a data layer
const toggleLayer = (layerId) => {
  emit('layer-toggle', layerId);
};

// Set the base map
const setBaseMap = (mapId) => {
  activeBaseMap.value = mapId;
  emit('base-map-change', mapId);
};

// Set layer opacity
const setLayerOpacity = (layerId, value) => {
  const opacity = parseInt(value, 10);
  layerOpacity.value = {
    ...layerOpacity.value,
    [layerId]: opacity
  };
  emit('layer-opacity-change', { layerId, opacity });
};

// Reset layers to default
const resetLayers = () => {
  activeBaseMap.value = 'standard';
  layerOpacity.value = {};
  emit('reset');
};
</script>

<style scoped>
.map-layer-selector {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 5;
}

.layer-toggle-button {
  display: flex;
  align-items: center;
  background-color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s;
}

.layer-toggle-button:hover {
  background-color: #f7fafc;
}

.layers-icon {
  background-image: url('@/assets/icons/layers.svg');
  margin-right: 0.5rem;
}

.layer-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 280px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.panel-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
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

.layer-groups {
  padding: 1rem;
}

.layer-group {
  margin-bottom: 1.5rem;
}

.layer-group:last-child {
  margin-bottom: 0;
}

.layer-group h4 {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a5568;
}

.layer-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.layer-option {
  display: flex;
  flex-direction: column;
}

.layer-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.layer-name {
  margin-left: 0.5rem;
  font-size: 0.875rem;
  color: #2d3748;
}

.layer-opacity {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
  padding-left: 1.5rem;
}

.layer-opacity input[type="range"] {
  flex: 1;
  height: 4px;
  background-color: #e2e8f0;
  border-radius: 2px;
  appearance: none;
}

.layer-opacity input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #4a6cf7;
  cursor: pointer;
}

.opacity-value {
  margin-left: 0.5rem;
  font-size: 0.75rem;
  color: #718096;
  width: 36px;
}

.panel-footer {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.reset-button {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: #4a5568;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #f7fafc;
}

.icon {
  width: 20px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

@media (max-width: 768px) {
  .button-text {
    display: none;
  }
  
  .layer-toggle-button {
    padding: 0.75rem;
  }
  
  .layers-icon {
    margin-right: 0;
  }
  
  .layer-panel {
    width: 250px;
  }
}
</style>