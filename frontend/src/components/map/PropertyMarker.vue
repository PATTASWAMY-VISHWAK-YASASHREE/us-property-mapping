<template>
  <div 
    class="property-marker" 
    :class="{ 
      'selected': selected,
      'highlighted': highlighted,
      [property.type.toLowerCase()]: true
    }"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div class="marker-icon">
      <i :class="markerIconClass"></i>
    </div>
    <div v-if="showPrice" class="marker-price">${{ formatPrice(property.price) }}</div>
    <div v-if="showTooltip" class="marker-tooltip">
      <div class="tooltip-image">
        <img :src="property.imageUrl" :alt="property.address" />
      </div>
      <div class="tooltip-content">
        <div class="tooltip-address">{{ property.address }}</div>
        <div class="tooltip-details">
          <span class="price">${{ formatPrice(property.price) }}</span>
          <span class="separator">•</span>
          <span class="type">{{ property.type }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  property: {
    type: Object,
    required: true
  },
  selected: {
    type: Boolean,
    default: false
  },
  highlighted: {
    type: Boolean,
    default: false
  },
  showPrice: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['click', 'mouseenter', 'mouseleave']);

const showTooltip = ref(false);

// Compute the marker icon class based on property type
const markerIconClass = computed(() => {
  const typeMap = {
    'residential': 'home-icon',
    'commercial': 'building-icon',
    'industrial': 'factory-icon',
    'land': 'land-icon',
    'multi-family': 'apartment-icon'
  };
  
  return typeMap[props.property.type.toLowerCase()] || 'property-icon';
});

// Format price for display
const formatPrice = (price) => {
  if (price >= 1000000) {
    return (price / 1000000).toFixed(1) + 'M';
  } else if (price >= 1000) {
    return (price / 1000).toFixed(0) + 'K';
  }
  return price.toString();
};

// Event handlers
const handleClick = (event) => {
  emit('click', {
    property: props.property,
    event
  });
};

const handleMouseEnter = (event) => {
  showTooltip.value = true;
  emit('mouseenter', {
    property: props.property,
    event
  });
};

const handleMouseLeave = (event) => {
  showTooltip.value = false;
  emit('mouseleave', {
    property: props.property,
    event
  });
};
</script>

<style scoped>
.property-marker {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #4a6cf7;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 1;
}

.property-marker:hover {
  transform: scale(1.1);
  z-index: 2;
}

.property-marker.selected {
  background-color: #e53e3e;
  transform: scale(1.2);
  z-index: 3;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
}

.property-marker.highlighted {
  animation: pulse 1.5s infinite;
}

/* Property type specific colors */
.property-marker.residential {
  background-color: #4a6cf7; /* Blue */
}

.property-marker.commercial {
  background-color: #38a169; /* Green */
}

.property-marker.industrial {
  background-color: #d69e2e; /* Yellow */
}

.property-marker.land {
  background-color: #805ad5; /* Purple */
}

.property-marker.multi-family {
  background-color: #dd6b20; /* Orange */
}

.marker-icon {
  width: 16px;
  height: 16px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.marker-price {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  color: #2d3748;
  font-size: 10px;
  font-weight: bold;
  padding: 2px 4px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
}

.marker-tooltip {
  position: absolute;
  bottom: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 10;
  pointer-events: none;
}

.marker-tooltip::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid white;
}

.tooltip-image {
  width: 100%;
  height: 100px;
  overflow: hidden;
}

.tooltip-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tooltip-content {
  padding: 8px;
}

.tooltip-address {
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tooltip-details {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.price {
  color: #4a6cf7;
  font-weight: 500;
}

.separator {
  margin: 0 4px;
  color: #cbd5e0;
}

.type {
  color: #718096;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(74, 108, 247, 0.7);
  }
  
  70% {
    transform: scale(1.1);
    box-shadow: 0 0 0 10px rgba(74, 108, 247, 0);
  }
  
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(74, 108, 247, 0);
  }
}

/* Icon classes */
.home-icon {
  background-image: url('@/assets/icons/home.svg');
}

.building-icon {
  background-image: url('@/assets/icons/building.svg');
}

.factory-icon {
  background-image: url('@/assets/icons/factory.svg');
}

.land-icon {
  background-image: url('@/assets/icons/land.svg');
}

.apartment-icon {
  background-image: url('@/assets/icons/apartment.svg');
}

.property-icon {
  background-image: url('@/assets/icons/property.svg');
}
</style>