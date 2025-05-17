import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { usePropertyStore } from '@/stores/property'
import PropertyView from '../PropertyView.vue'
import PropertyDetail from '@/components/property/PropertyDetail.vue'
import OwnershipHistory from '@/components/property/OwnershipHistory.vue'
import TransactionRecords from '@/components/property/TransactionRecords.vue'
import ComparableProperties from '@/components/property/ComparableProperties.vue'

// Mock vue-router
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: {
      id: '123'
    }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}))

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve())
  }
}))

// Mock vue-toastification
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn()
  })
}))

describe('PropertyView.vue', () => {
  let wrapper
  let pinia
  let propertyStore

  const mockProperty = {
    id: '123',
    address: '123 Main St',
    city: 'Anytown',
    state: 'CA',
    zip_code: '12345',
    property_type: 'residential',
    bedrooms: 3,
    bathrooms: 2,
    square_feet: 1500,
    lot_size: 5000,
    year_built: 2000,
    last_sale_date: '2020-01-01',
    last_sale_price: 500000,
    current_value: 550000,
    value_estimate_date: '2023-01-01'
  }

  beforeEach(() => {
    // Create a fresh Pinia instance for each test
    pinia = createTestingPinia({
      createSpy: vi.fn,
      stubActions: false
    })
    
    propertyStore = usePropertyStore(pinia)
    
    // Mock the store's state and actions
    propertyStore.currentProperty = mockProperty
    propertyStore.fetchPropertyById = vi.fn().mockResolvedValue(mockProperty)
    
    // Mount the component
    wrapper = mount(PropertyView, {
      global: {
        plugins: [pinia],
        stubs: {
          PropertyDetail: true,
          OwnershipHistory: true,
          TransactionRecords: true,
          ComparableProperties: true
        }
      }
    })
  })

  it('renders the property view', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('displays the property address', () => {
    expect(wrapper.text()).toContain('123 Main St')
    expect(wrapper.text()).toContain('Anytown, CA 12345')
  })

  it('fetches property data on mount', () => {
    expect(propertyStore.fetchPropertyById).toHaveBeenCalledWith('123')
  })

  it('renders the PropertyDetail component', () => {
    expect(wrapper.findComponent(PropertyDetail).exists()).toBe(true)
    expect(wrapper.findComponent(PropertyDetail).props('property')).toEqual(mockProperty)
  })

  it('renders the tab navigation', () => {
    const tabs = wrapper.findAll('button')
    expect(tabs.length).toBeGreaterThanOrEqual(3)
    expect(tabs[0].text()).toContain('Ownership History')
    expect(tabs[1].text()).toContain('Transaction Records')
    expect(tabs[2].text()).toContain('Comparable Properties')
  })

  it('changes active tab when clicked', async () => {
    const tabs = wrapper.findAll('button')
    
    // Default tab should be ownership
    expect(wrapper.findComponent(OwnershipHistory).exists()).toBe(true)
    
    // Click on transactions tab
    await tabs[1].trigger('click')
    expect(wrapper.findComponent(TransactionRecords).exists()).toBe(true)
    expect(wrapper.findComponent(OwnershipHistory).exists()).toBe(false)
    
    // Click on comparables tab
    await tabs[2].trigger('click')
    expect(wrapper.findComponent(ComparableProperties).exists()).toBe(true)
    expect(wrapper.findComponent(TransactionRecords).exists()).toBe(false)
  })

  it('shows loading state when property is loading', async () => {
    // Set loading state to true
    propertyStore.currentProperty = null
    wrapper = mount(PropertyView, {
      global: {
        plugins: [pinia],
        stubs: {
          PropertyDetail: true,
          OwnershipHistory: true,
          TransactionRecords: true,
          ComparableProperties: true
        }
      },
      data() {
        return {
          loading: true
        }
      }
    })
    
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })

  it('shows error message when there is an error', async () => {
    // Set error state
    wrapper = mount(PropertyView, {
      global: {
        plugins: [pinia],
        stubs: {
          PropertyDetail: true,
          OwnershipHistory: true,
          TransactionRecords: true,
          ComparableProperties: true
        }
      },
      data() {
        return {
          error: 'Failed to load property',
          loading: false,
          property: null
        }
      }
    })
    
    expect(wrapper.text()).toContain('Failed to load property')
  })

  it('shows bookmark and print buttons', () => {
    const buttons = wrapper.findAll('button')
    const buttonTexts = buttons.map(b => b.text())
    
    expect(buttonTexts).toContain('Bookmark')
    expect(buttonTexts).toContain('Print Report')
  })
})