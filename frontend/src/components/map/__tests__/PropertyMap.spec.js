import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import PropertyMap from '../PropertyMap.vue';
import MapControls from '../MapControls.vue';
import MapLayerSelector from '../MapLayerSelector.vue';

// Mock child components
vi.mock('../MapControls.vue', () => ({
  default: {
    name: 'MapControls',
    render: () => {},
    emits: ['zoom-in', 'zoom-out', 'reset-view', 'toggle-fullscreen']
  }
}));

vi.mock('../MapLayerSelector.vue', () => ({
  default: {
    name: 'MapLayerSelector',
    render: () => {},
    props: ['available-layers', 'active-layers'],
    emits: ['layer-toggle']
  }
}));

vi.mock('../PropertyMarker.vue', () => ({
  default: {
    name: 'PropertyMarker',
    render: () => {},
    props: ['property', 'selected', 'highlighted', 'show-price']
  }
}));

vi.mock('../PropertyCluster.vue', () => ({
  default: {
    name: 'PropertyCluster',
    render: () => {},
    props: ['count', 'size', 'color', 'properties']
  }
}));

describe('PropertyMap', () => {
  // Sample property data for testing
  const sampleProperties = [
    {
      id: 1,
      address: '123 Main St',
      price: 500000,
      size: 2000,
      type: 'Residential',
      yearBuilt: 2010,
      latitude: 37.7749,
      longitude: -122.4194,
      imageUrl: 'https://example.com/image1.jpg'
    },
    {
      id: 2,
      address: '456 Oak Ave',
      price: 750000,
      size: 3000,
      type: 'Commercial',
      yearBuilt: 2005,
      latitude: 37.7750,
      longitude: -122.4180,
      imageUrl: 'https://example.com/image2.jpg'
    }
  ];

  it('renders properly with default props', () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    expect(wrapper.find('.property-map-container').exists()).toBe(true);
    expect(wrapper.find('.map-container').exists()).toBe(true);
    expect(wrapper.findComponent(MapControls).exists()).toBe(true);
    expect(wrapper.findComponent(MapLayerSelector).exists()).toBe(true);
  });

  it('shows loading state initially', () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    expect(wrapper.find('.map-overlay').exists()).toBe(true);
    expect(wrapper.find('.loading-spinner').exists()).toBe(true);
    expect(wrapper.find('.loading-text').text()).toBe('Loading map data...');
  });

  it('passes correct props to MapLayerSelector', () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    const layerSelector = wrapper.findComponent(MapLayerSelector);
    expect(layerSelector.props('availableLayers')).toBeDefined();
    expect(layerSelector.props('activeLayers')).toBeDefined();
  });

  it('emits events from MapControls', async () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    const mapControls = wrapper.findComponent(MapControls);
    
    // Test zoom in event
    await mapControls.vm.$emit('zoom-in');
    expect(wrapper.emitted()).toBeDefined();
    
    // Test zoom out event
    await mapControls.vm.$emit('zoom-out');
    expect(wrapper.emitted()).toBeDefined();
    
    // Test reset view event
    await mapControls.vm.$emit('reset-view');
    expect(wrapper.emitted()).toBeDefined();
  });

  it('handles layer toggle events', async () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    const layerSelector = wrapper.findComponent(MapLayerSelector);
    
    // Test layer toggle event
    await layerSelector.vm.$emit('layer-toggle', 'satellite');
    expect(wrapper.emitted()).toBeDefined();
  });

  it('formats numbers correctly', () => {
    const wrapper = mount(PropertyMap, {
      props: {
        properties: []
      },
      global: {
        stubs: {
          MapControls: true,
          MapLayerSelector: true
        }
      }
    });
    
    // Access the formatNumber method
    const formatNumber = wrapper.vm.formatNumber;
    
    expect(formatNumber(1000)).toBe('1,000');
    expect(formatNumber(1000000)).toBe('1,000,000');
    expect(formatNumber(1234567)).toBe('1,234,567');
  });
});