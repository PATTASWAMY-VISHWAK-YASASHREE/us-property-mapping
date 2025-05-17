import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import OwnerAnalysis from '../OwnerAnalysis.vue'
import { useWealthStore } from '../../../stores/wealth'

// Mock Chart.js
vi.mock('chart.js', () => {
  return {
    Chart: vi.fn().mockImplementation(() => ({
      destroy: vi.fn()
    })),
    registerables: []
  }
})

// Mock d3
vi.mock('d3', () => {
  return {
    select: vi.fn().mockReturnValue({
      selectAll: vi.fn().mockReturnValue({
        remove: vi.fn()
      }),
      append: vi.fn().mockReturnThis(),
      attr: vi.fn().mockReturnThis()
    }),
    forceSimulation: vi.fn().mockReturnValue({
      force: vi.fn().mockReturnThis(),
      on: vi.fn().mockReturnThis()
    }),
    forceLink: vi.fn(),
    forceManyBody: vi.fn().mockReturnValue({
      strength: vi.fn()
    }),
    forceCenter: vi.fn(),
    drag: vi.fn().mockReturnValue({
      on: vi.fn().mockReturnThis()
    })
  }
})

// Mock route
vi.mock('vue-router', () => ({
  useRoute: vi.fn().mockReturnValue({
    params: {
      id: '123'
    }
  })
}))

describe('OwnerAnalysis.vue', () => {
  let wrapper
  let wealthStore

  beforeEach(() => {
    // Create a test pinia instance
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })

    // Create the component with mocked store
    wrapper = mount(OwnerAnalysis, {
      global: {
        plugins: [pinia],
        stubs: ['router-link']
      }
    })

    // Get the store instance
    wealthStore = useWealthStore()
    
    // Mock store methods
    wealthStore.fetchOwnerById = vi.fn().mockResolvedValue({})
    wealthStore.fetchWealthData = vi.fn().mockResolvedValue({
      realEstate: 5000000,
      investments: 3000000,
      businessAssets: 2000000,
      otherAssets: 1000000
    })
    wealthStore.fetchWealthTrends = vi.fn().mockResolvedValue([])
    wealthStore.fetchRelatedOwners = vi.fn().mockResolvedValue([])
    
    // Mock store state
    wealthStore.currentOwner = {
      id: '123',
      name: 'John Doe',
      type: 'Individual',
      netWorth: '$10,000,000',
      address: '123 Main St, City, State',
      email: 'john@example.com',
      phone: '555-123-4567',
      taxId: '123-45-6789',
      lastUpdated: '2023-01-15'
    }
    
    wealthStore.ownerProperties = [
      {
        id: 'prop1',
        address: '123 Main St',
        type: 'Residential',
        value: '$2,500,000',
        acquisitionDate: '2020-05-10'
      },
      {
        id: 'prop2',
        address: '456 Business Ave',
        type: 'Commercial',
        value: '$4,500,000',
        acquisitionDate: '2018-11-22'
      }
    ]
    
    wealthStore.totalPropertyValue = 7000000
    wealthStore.loading = false
  })

  it('renders the owner profile section correctly', () => {
    expect(wrapper.find('h3').text()).toContain('Owner Profile')
    expect(wrapper.html()).toContain('John Doe')
    expect(wrapper.html()).toContain('Individual')
    expect(wrapper.html()).toContain('123 Main St, City, State')
    expect(wrapper.html()).toContain('john@example.com')
  })

  it('displays financial summary correctly', () => {
    expect(wrapper.html()).toContain('Net Worth')
    expect(wrapper.html()).toContain('Total Property Value')
    expect(wrapper.html()).toContain('Properties Owned')
  })

  it('renders the wealth data visualization section', () => {
    expect(wrapper.findAll('h3')[1].text()).toContain('Wealth Data Visualization')
    expect(wrapper.findAll('button').length).toBeGreaterThan(0)
  })

  it('renders the property portfolio section', () => {
    expect(wrapper.findAll('h3')[2].text()).toContain('Property Portfolio')
    expect(wrapper.find('table')).toBeTruthy()
    expect(wrapper.findAll('tr').length).toBeGreaterThan(0)
  })

  it('renders the relationship mapping section', () => {
    expect(wrapper.findAll('h3')[3].text()).toContain('Relationship Mapping')
  })

  it('calls the appropriate store methods on mount', () => {
    expect(wealthStore.fetchOwnerById).toHaveBeenCalledWith('123')
    expect(wealthStore.fetchWealthData).toHaveBeenCalledWith('123')
    expect(wealthStore.fetchWealthTrends).toHaveBeenCalledWith('123', 'yearly')
    expect(wealthStore.fetchRelatedOwners).toHaveBeenCalledWith('123')
  })

  it('formats currency correctly', async () => {
    // Access the component instance
    const formatCurrency = wrapper.vm.formatCurrency
    
    expect(formatCurrency(1000000)).toBe('$1,000,000')
    expect(formatCurrency('$1,000,000')).toBe('$1,000,000')
    expect(formatCurrency(0)).toBe('$0')
    expect(formatCurrency(null)).toBe('$0')
  })

  it('formats dates correctly', async () => {
    // Access the component instance
    const formatDate = wrapper.vm.formatDate
    
    expect(formatDate('2023-01-15')).toMatch(/Jan 15, 2023/)
    expect(formatDate(null)).toBe('N/A')
  })

  it('calculates owner initials correctly', () => {
    expect(wrapper.vm.ownerInitials).toBe('JD')
    
    // Test with different name
    wealthStore.currentOwner = { ...wealthStore.currentOwner, name: 'Jane Smith-Doe' }
    expect(wrapper.vm.ownerInitials).toBe('JS')
  })
})