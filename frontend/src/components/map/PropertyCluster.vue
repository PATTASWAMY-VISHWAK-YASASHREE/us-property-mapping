<template>
  <div class="property-cluster" :style="clusterStyle" @click="handleClick">
    <div class="cluster-count">{{ count }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  count: {
    type: Number,
    required: true
  },
  size: {
    type: Number,
    default: 40
  },
  color: {
    type: String,
    default: '#4a6cf7'
  },
  properties: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['click']);

// Compute the size based on the count
const clusterSize = computed(() => {
  // Base size
  let size = props.size;
  
  // Increase size based on count
  if (props.count > 100) {
    size += 20;
  } else if (props.count > 50) {
    size += 15;
  } else if (props.count > 20) {
    size += 10;
  } else if (props.count > 10) {
    size += 5;
  }
  
  return size;
});

// Compute the color based on the count
const clusterColor = computed(() => {
  if (props.count > 100) {
    return '#e53e3e'; // Red for large clusters
  } else if (props.count > 50) {
    return '#dd6b20'; // Orange for medium-large clusters
  } else if (props.count > 20) {
    return '#d69e2e'; // Yellow for medium clusters
  } else if (props.count > 10) {
    return '#38a169'; // Green for small-medium clusters
  }
  
  return props.color; // Default color for small clusters
});

// Compute the style for the cluster
const clusterStyle = computed(() => {
  return {
    width: `${clusterSize.value}px`,
    height: `${clusterSize.value}px`,
    backgroundColor: clusterColor.value,
    fontSize: props.count > 99 ? '12px' : '14px'
  };
});

// Handle click event
const handleClick = (event) => {
  emit('click', {
    properties: props.properties,
    event
  });
};
</script>

<style scoped>
.property-cluster {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  user-select: none;
}

.property-cluster:hover {
  transform: scale(1.05);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

.cluster-count {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
</style>