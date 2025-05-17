import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import MapExplorer from '../MapExplorer.vue';
import PropertyMap from '../PropertyMap.vue';
import SearchBar from '../../search/SearchBar.vue';

// Mock the store
vi.mock('@/stores/property', () => ({
  usePropertyStore: () => ({
    properties: [],
    searchResults: [],
    loading: false,
    error: null,
    searchFilters: {
      propertyType: [],
      minValue: 0,
      maxValue: null,
      minBedrooms: null,
      maxBedrooms: null,
      minBathrooms: null,
      maxBathrooms: null,
      yearBuiltMin: null,
      yearBuiltMax: null
    },
    fetchProperties: vi.fn().mockResolvedValue([]),
    searchProperties: vi.fn().mockResolvedValue([]),
    updateSearchFilters: vi.fn(),
    resetSearchFilters: vi.fn(),
    saveSearch: vi.fn().mockResolvedValue({}),
    addToRecentlyViewed: vi.fn()
  })
}));

// Mock child components
vi.mock('../PropertyMap.vue', () => ({
  default: {
    name: 'PropertyMap',
    render: () => {},
    props: ['properties', 'selected-property', 'height'],
    emits: ['property-selected']
  }
}));

vi.mock('../../search/SearchBar.vue', () => ({
  default: {
    name: 'SearchBar',
    render: () => {},
    emits: ['search']
  }
}));

// Mock vue-toastification
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn()
  })
}));

describe('MapExplorer', () => {
  // Sample property data for testing
  const sampleProperties = [
    {
      id: 1,
      address: '123 Main St',
      price: 500000,
      bedrooms: 3,
      bathrooms: 2,
      squareFootage: 2000,
      type: 'Residential',
      yearBuilt: 2010,
      coordinates: [37.7749, -122.4194],
      imageUrl: 'https://example.com/image1.jpg'
    },
    {
      id: 2,
      address: '456 Oak Ave',
      value: '$750000',
      bedrooms: 4,
      bathrooms: 3,
      squareFootage: 3000,
      type: 'Commercial',
      yearBuilt: 2005,
      coordinates: [37.7750, -122.4180],
      imageUrl: 'https://example.com/image2.jpg'
    }
  ];

  it('renders properly with default state', () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    expect(wrapper.find('.map-explorer').exists()).toBe(true);
    expect(wrapper.find('.search-filter-panel').exists()).toBe(true);
    expect(wrapper.find('.map-container').exists()).toBe(true);
    expect(wrapper.findComponent(PropertyMap).exists()).toBe(true);
    expect(wrapper.findComponent(SearchBar).exists()).toBe(true);
  });

  it('toggles panel collapse state', async () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    expect(wrapper.vm.isPanelCollapsed).toBe(false);
    
    await wrapper.find('.panel-toggle-btn').trigger('click');
    expect(wrapper.vm.isPanelCollapsed).toBe(true);
    expect(wrapper.find('.panel-collapsed').exists()).toBe(true);
    
    await wrapper.find('.panel-toggle-btn').trigger('click');
    expect(wrapper.vm.isPanelCollapsed).toBe(false);
    expect(wrapper.find('.panel-collapsed').exists()).toBe(false);
  });

  it('handles property selection', async () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    // Set some properties
    wrapper.vm.properties = sampleProperties;
    await wrapper.vm.$nextTick();
    
    // Select a property
    wrapper.vm.selectProperty(sampleProperties[0]);
    await wrapper.vm.$nextTick();
    
    expect(wrapper.vm.selectedProperty).toEqual(sampleProperties[0]);
    expect(wrapper.find('.property-detail-panel').exists()).toBe(true);
    
    // Close property details
    await wrapper.find('.close-btn').trigger('click');
    expect(wrapper.vm.selectedProperty).toBe(null);
    expect(wrapper.find('.property-detail-panel').exists()).toBe(false);
  });

  it('applies and resets filters', async () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    // Set some filters
    wrapper.vm.filters.propertyType = ['Residential'];
    wrapper.vm.filters.minValue = 100000;
    wrapper.vm.filters.maxValue = 1000000;
    wrapper.vm.applyFilters();
    
    expect(wrapper.vm.filters.propertyType).toEqual(['Residential']);
    expect(wrapper.vm.filters.minValue).toBe(100000);
    expect(wrapper.vm.filters.maxValue).toBe(1000000);
    
    // Reset filters
    wrapper.vm.resetFilters();
    
    expect(wrapper.vm.filters.propertyType).toEqual([]);
    expect(wrapper.vm.filters.minValue).toBe(null);
    expect(wrapper.vm.filters.maxValue).toBe(null);
  });

  it('formats numbers correctly', () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    expect(wrapper.vm.formatNumber(1000)).toBe('1,000');
    expect(wrapper.vm.formatNumber(1000000)).toBe('1,000,000');
    expect(wrapper.vm.formatNumber(1234567)).toBe('1,234,567');
  });

  it('extracts numeric values from string prices', () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    expect(wrapper.vm.extractNumericValue('$1,000')).toBe(1000);
    expect(wrapper.vm.extractNumericValue('$1,000,000')).toBe(1000000);
    expect(wrapper.vm.extractNumericValue(1234567)).toBe(1234567);
  });

  it('formats short values for display', () => {
    const wrapper = mount(MapExplorer, {
      global: {
        stubs: {
          PropertyMap: true,
          SearchBar: true
        }
      }
    });
    
    expect(wrapper.vm.formatShortValue(1000)).toBe('1K');
    expect(wrapper.vm.formatShortValue(1500000)).toBe('1.5M');
  });
});