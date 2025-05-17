import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createTestingPinia } from '@pinia/testing'
import DashboardView from '../DashboardView.vue'

// Mock fetch API
global.fetch = vi.fn()

// Mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/search', name: 'search-results' },
    { path: '/property/:id', name: 'property-details' }
  ]
})

describe('DashboardView', () => {
  let wrapper

  beforeEach(() => {
    // Reset mocks
    fetch.mockReset()
    
    // Mock successful API responses
    fetch.mockImplementation((url) => {
      if (url.includes('/api/user/activities')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve([
            { id: 1, type: 'search', title: 'Searched for properties in San Francisco', timestamp: new Date().toISOString() },
            { id: 2, type: 'view', title: 'Viewed 123 Main St', timestamp: new Date().toISOString() }
          ])
        })
      } else if (url.includes('/api/user/saved-searches')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve([
            { id: 1, name: 'San Francisco Houses', params: { location: 'San Francisco', propertyType: 'house' } }
          ])
        })
      } else if (url.includes('/api/user/bookmarks')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve([
            { 
              id: 1, 
              address: '123 Main St', 
              estimatedValue: 1200000, 
              bedrooms: 3, 
              bathrooms: 2, 
              squareFeet: 1800,
              thumbnail: '/img/property1.jpg'
            }
          ])
        })
      }
      
      return Promise.resolve({ ok: false })
    })
    
    // Mount component with mocks
    wrapper = mount(DashboardView, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn,
            stubActions: false
          })
        ]
      }
    })
  })

  it('renders the dashboard with all sections', () => {
    expect(wrapper.find('h1').text()).toBe('Dashboard')
    expect(wrapper.findAll('.dashboard-card')).toHaveLength(4)
    expect(wrapper.findAll('h2')[0].text()).toBe('Recent Activities')
    expect(wrapper.findAll('h2')[1].text()).toBe('Saved Searches')
    expect(wrapper.findAll('h2')[2].text()).toBe('Bookmarked Properties')
    expect(wrapper.findAll('h2')[3].text()).toBe('Quick Search')
  })

  it('displays recent activities when loaded', async () => {
    await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async operations
    
    const activityItems = wrapper.findAll('.activity-item')
    expect(activityItems).toHaveLength(2)
    expect(activityItems[0].find('.activity-title').text()).toContain('Searched for properties')
  })

  it('displays saved searches when loaded', async () => {
    await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async operations
    
    const searchItems = wrapper.findAll('.search-item')
    expect(searchItems).toHaveLength(1)
    expect(searchItems[0].text()).toContain('San Francisco Houses')
  })

  it('displays bookmarked properties when loaded', async () => {
    await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async operations
    
    const propertyCards = wrapper.findAll('.property-card')
    expect(propertyCards).toHaveLength(1)
    expect(propertyCards[0].find('h3').text()).toBe('123 Main St')
  })

  it('has a working quick search form', async () => {
    const form = wrapper.find('.quick-search-form')
    const locationInput = wrapper.find('#location')
    
    await locationInput.setValue('New York')
    await form.trigger('submit')
    
    // Check that router was called with correct query params
    expect(router.currentRoute.value.name).toBe('search-results')
    expect(router.currentRoute.value.query.location).toBe('New York')
  })
})