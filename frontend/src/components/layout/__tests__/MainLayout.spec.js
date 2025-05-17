import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import MainLayout from '../MainLayout.vue';
import Sidebar from '../Sidebar.vue';
import Header from '../Header.vue';

// Mock child components
vi.mock('../Sidebar.vue', () => ({
  default: {
    name: 'Sidebar',
    render: () => {}
  }
}));

vi.mock('../Header.vue', () => ({
  default: {
    name: 'Header',
    render: () => {}
  }
}));

describe('MainLayout', () => {
  it('renders properly with all components', () => {
    const wrapper = mount(MainLayout, {
      global: {
        stubs: {
          Sidebar: true,
          Header: true
        }
      },
      slots: {
        default: '<div class="test-content">Test Content</div>'
      }
    });
    
    expect(wrapper.find('.main-layout').exists()).toBe(true);
    expect(wrapper.findComponent(Sidebar).exists()).toBe(true);
    expect(wrapper.findComponent(Header).exists()).toBe(true);
    expect(wrapper.find('.main-content').exists()).toBe(true);
  });

  it('renders slot content correctly', () => {
    const wrapper = mount(MainLayout, {
      global: {
        stubs: {
          Sidebar: true,
          Header: true
        }
      },
      slots: {
        default: '<div class="test-content">Test Content</div>'
      }
    });
    
    expect(wrapper.find('.test-content').exists()).toBe(true);
    expect(wrapper.find('.test-content').text()).toBe('Test Content');
  });

  it('has the correct structure', () => {
    const wrapper = mount(MainLayout, {
      global: {
        stubs: {
          Sidebar: true,
          Header: true
        }
      }
    });
    
    // Check the structure
    const sidebar = wrapper.findComponent(Sidebar);
    const contentWrapper = wrapper.find('.content-wrapper');
    const header = wrapper.findComponent(Header);
    const mainContent = wrapper.find('.main-content');
    
    expect(sidebar.exists()).toBe(true);
    expect(contentWrapper.exists()).toBe(true);
    expect(header.exists()).toBe(true);
    expect(mainContent.exists()).toBe(true);
    
    // Check that the sidebar is a direct child of main-layout
    expect(sidebar.element.parentNode.classList.contains('main-layout')).toBe(true);
    
    // Check that the header is inside content-wrapper
    expect(header.element.parentNode.classList.contains('content-wrapper')).toBe(true);
    
    // Check that the main-content is inside content-wrapper
    expect(mainContent.element.parentNode.classList.contains('content-wrapper')).toBe(true);
  });
});