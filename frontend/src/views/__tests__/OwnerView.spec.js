import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import OwnerView from '../OwnerView.vue'
import { useWealthStore } from '../../stores/wealth'

// Mock the OwnerAnalysis component
vi.mock('../../components/wealth/OwnerAnalysis.vue', () => ({
  default: {
    name: 'OwnerAnalysis',
    template: '<div class="mock-owner-analysis">Owner Analysis Component</div>'
  }
}))

// Mock router
vi.mock('vue-router', () => ({
  useRoute: vi.fn().mockReturnValue({
    params: {
      id: '123'
    }
  })
}))

describe('OwnerView.vue', () => {
  let wrapper
  let wealthStore

  beforeEach(() => {
    // Create a test pinia instance
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })

    // Create the component with mocked store
    wrapper = mount(OwnerView, {
      global: {
        plugins: [pinia],
        stubs: ['router-link'],
        mocks: {
          $router: {
            go: vi.fn()
          }
        }
      }
    })

    // Get the store instance
    wealthStore = useWealthStore()
    
    // Mock store state
    wealthStore.currentOwner = {
      id: '123',
      name: 'John Doe',
      type: 'Individual',
      netWorth: '$10,000,000'
    }
    
    wealthStore.ownerProperties = [
      { id: 'prop1', address: '123 Main St', value: '$2,500,000' },
      { id: 'prop2', address: '456 Business Ave', value: '$4,500,000' }
    ]
    
    wealthStore.wealthData = {
      realEstate: 5000000,
      investments: 3000000,
      businessAssets: 2000000,
      otherAssets: 1000000
    }
  })

  it('renders the owner view correctly', () => {
    expect(wrapper.find('h1').text()).toBe('Owner Details')
    expect(wrapper.find('.mock-owner-analysis').exists()).toBe(true)
  })

  it('displays back and export buttons', () => {
    const buttons = wrapper.findAll('button')
    expect(buttons.length).toBe(2)
    expect(buttons[0].text()).toContain('Back')
    expect(buttons[1].text()).toBe('Export Data')
  })

  it('navigates back when back button is clicked', async () => {
    const backButton = wrapper.findAll('button')[0]
    await backButton.trigger('click')
    expect(wrapper.vm.$router.go).toHaveBeenCalledWith(-1)
  })

  it('exports owner data when export button is clicked', async () => {
    // Mock the necessary DOM APIs for the export functionality
    const mockUrl = 'mock-blob-url'
    const mockCreateObjectURL = vi.fn().mockReturnValue(mockUrl)
    const mockRevokeObjectURL = vi.fn()
    
    // Mock createElement and appendChild
    const mockAnchor = {
      href: '',
      download: '',
      click: vi.fn()
    }
    
    const originalCreateElement = document.createElement
    const originalAppendChild = document.body.appendChild
    const originalRemoveChild = document.body.removeChild
    
    // Override the methods
    document.createElement = vi.fn().mockReturnValue(mockAnchor)
    document.body.appendChild = vi.fn()
    document.body.removeChild = vi.fn()
    
    // Mock URL methods
    global.URL.createObjectURL = mockCreateObjectURL
    global.URL.revokeObjectURL = mockRevokeObjectURL
    
    // Mock Blob
    global.Blob = vi.fn().mockImplementation((content, options) => ({
      content,
      options
    }))
    
    // Trigger export
    const exportButton = wrapper.findAll('button')[1]
    await exportButton.trigger('click')
    
    // Verify the export functionality
    expect(document.createElement).toHaveBeenCalledWith('a')
    expect(mockAnchor.download).toBe('owner-123-data.json')
    expect(mockAnchor.click).toHaveBeenCalled()
    expect(mockCreateObjectURL).toHaveBeenCalled()
    expect(mockRevokeObjectURL).toHaveBeenCalledWith(mockUrl)
    
    // Restore original methods
    document.createElement = originalCreateElement
    document.body.appendChild = originalAppendChild
    document.body.removeChild = originalRemoveChild
  })
})