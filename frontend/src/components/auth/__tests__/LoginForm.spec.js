import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import LoginForm from '../LoginForm.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia, setActivePinia } from 'pinia';

// Create a mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/dashboard', name: 'Dashboard' },
    { path: '/forgot-password', name: 'ForgotPassword' },
    { path: '/register', name: 'Register' }
  ]
});

// Mock the auth store
vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({
    login: vi.fn().mockImplementation(({ email, password }) => {
      if (email === 'test@example.com' && password === 'password123') {
        return Promise.resolve();
      } else {
        return Promise.reject(new Error('Invalid credentials'));
      }
    })
  })
}));

describe('LoginForm', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia());
  });

  it('renders properly', () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [router]
      }
    });
    
    expect(wrapper.find('h2').text()).toBe('Login');
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login');
  });

  it('validates form inputs', async () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [router]
      }
    });
    
    // Try to submit with empty form
    await wrapper.find('form').trigger('submit');
    
    // Check that the form validation prevents submission
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    
    expect(emailInput.attributes('required')).toBeDefined();
    expect(passwordInput.attributes('required')).toBeDefined();
  });

  it('submits the form with valid credentials', async () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [router]
      }
    });
    
    // Fill in the form
    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('password123');
    
    // Submit the form
    await wrapper.find('form').trigger('submit');
    
    // Wait for the next tick to allow promises to resolve
    await wrapper.vm.$nextTick();
    
    // Check that the router was called to navigate to dashboard
    expect(router.currentRoute.value.path).toBe('/dashboard');
  });

  it('shows error message with invalid credentials', async () => {
    const wrapper = mount(LoginForm, {
      global: {
        plugins: [router]
      }
    });
    
    // Fill in the form with invalid credentials
    await wrapper.find('input[type="email"]').setValue('wrong@example.com');
    await wrapper.find('input[type="password"]').setValue('wrongpassword');
    
    // Submit the form
    await wrapper.find('form').trigger('submit');
    
    // Wait for the next tick to allow promises to resolve
    await wrapper.vm.$nextTick();
    
    // Check that the error message is displayed
    expect(wrapper.find('.error-message').exists()).toBe(true);
    expect(wrapper.find('.error-message').text()).toBe('Invalid credentials');
  });
});