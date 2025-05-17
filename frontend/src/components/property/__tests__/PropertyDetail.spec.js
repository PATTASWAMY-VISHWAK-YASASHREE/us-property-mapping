import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PropertyDetail from '../PropertyDetail.vue'

describe('PropertyDetail.vue', () => {
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
    value_estimate_date: '2023-01-01',
    images: [
      { url: 'https://example.com/image1.jpg' },
      { url: 'https://example.com/image2.jpg' }
    ]
  }

  it('renders the property detail component', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    expect(wrapper.exists()).toBe(true)
  })

  it('displays property overview sections', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('Property Overview')
    expect(wrapper.text()).toContain('Basic Information')
    expect(wrapper.text()).toContain('Valuation')
    expect(wrapper.text()).toContain('Location')
  })

  it('displays property basic information correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('Property Type:')
    expect(wrapper.text()).toContain('residential')
    expect(wrapper.text()).toContain('Year Built:')
    expect(wrapper.text()).toContain('2000')
    expect(wrapper.text()).toContain('Bedrooms:')
    expect(wrapper.text()).toContain('3')
    expect(wrapper.text()).toContain('Bathrooms:')
    expect(wrapper.text()).toContain('2')
    expect(wrapper.text()).toContain('Square Feet:')
    expect(wrapper.text()).toContain('1,500')
    expect(wrapper.text()).toContain('Lot Size:')
    expect(wrapper.text()).toContain('5,000')
  })

  it('displays property valuation information correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('Current Value:')
    expect(wrapper.text()).toContain('$550,000')
    expect(wrapper.text()).toContain('Last Sale Price:')
    expect(wrapper.text()).toContain('$500,000')
    expect(wrapper.text()).toContain('Last Sale Date:')
  })

  it('displays property location information correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('Address:')
    expect(wrapper.text()).toContain('123 Main St')
    expect(wrapper.text()).toContain('City:')
    expect(wrapper.text()).toContain('Anytown')
    expect(wrapper.text()).toContain('State:')
    expect(wrapper.text()).toContain('CA')
    expect(wrapper.text()).toContain('Zip Code:')
    expect(wrapper.text()).toContain('12345')
  })

  it('displays property images when available', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    const images = wrapper.findAll('img')
    expect(images.length).toBe(2)
    expect(images[0].attributes('src')).toBe('https://example.com/image1.jpg')
    expect(images[1].attributes('src')).toBe('https://example.com/image2.jpg')
  })

  it('displays a placeholder when no images are available', () => {
    const propertyWithoutImages = { ...mockProperty, images: [] }
    
    const wrapper = mount(PropertyDetail, {
      props: {
        property: propertyWithoutImages,
        loading: false
      }
    })
    
    expect(wrapper.text()).toContain('No images available')
  })

  it('shows loading spinner when loading prop is true', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: true
      }
    })
    
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })

  it('formats currency values correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    // Access the component instance to test the formatCurrency method
    expect(wrapper.vm.formatCurrency(1000000)).toBe('1,000,000')
    expect(wrapper.vm.formatCurrency(1500)).toBe('1,500')
    expect(wrapper.vm.formatCurrency(null)).toBe('N/A')
  })

  it('formats number values correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    // Access the component instance to test the formatNumber method
    expect(wrapper.vm.formatNumber(1000000)).toBe('1,000,000')
    expect(wrapper.vm.formatNumber(1500)).toBe('1,500')
    expect(wrapper.vm.formatNumber(null)).toBe('N/A')
  })

  it('formats date values correctly', () => {
    const wrapper = mount(PropertyDetail, {
      props: {
        property: mockProperty,
        loading: false
      }
    })
    
    // Access the component instance to test the formatDate method
    const date = new Date('2020-01-01')
    expect(wrapper.vm.formatDate(date)).toMatch(/Jan 1, 2020/)
    expect(wrapper.vm.formatDate(null)).toBe('N/A')
  })
})