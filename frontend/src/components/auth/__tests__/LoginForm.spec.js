import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import { createTestingPinia } from '@pinia/testing';
import LoginForm from '../LoginForm.vue';
import { useAuthStore } from '@/stores/auth';

// Create a mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
    { path: '/forgot-password', component: { template: '<div>Forgot Password</div>' } },
    { path: '/register', component: { template: '<div>Register</div>' } }
  ]
});

describe('LoginForm.vue', () => {
  let wrapper;
  let authStore;
  
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    const pinia = createTestingPinia({
      createSpy: vi.fn
    });
    
    // Mount the component with dependencies
    wrapper = mount(LoginForm, {
      global: {
        plugins: [router, pinia],
      }
    });
    
    // Get the auth store with the testing pinia
    authStore = useAuthStore();
  });
  
  it('renders the login form correctly', () => {
    // Check that the component renders
    expect(wrapper.find('.login-form').exists()).toBe(true);
    expect(wrapper.find('h2').text()).toBe('Login');
    
    // Check form elements
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login');
    
    // Check links
    expect(wrapper.find('a[href="/forgot-password"]').exists()).toBe(true);
    expect(wrapper.find('a[href="/register"]').exists()).toBe(true);
  });
  
  it('updates email and password when input changes', async () => {
    // Simulate user input
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('password123');
    
    // Check that the component's data is updated
    expect(emailInput.element.value).toBe('test@example.com');
    expect(passwordInput.element.value).toBe('password123');
  });
  
  it('calls login method and redirects on successful login', async () => {
    // Mock the login method to resolve successfully
    authStore.login.mockResolvedValue();
    
    // Set form values
    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('password123');
    
    // Submit the form
    await wrapper.find('form').trigger('submit');
    
    // Check that the login method was called with correct parameters
    expect(authStore.login).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
    
    // Check that router.push was called with the correct path
    // We need to wait for the next tick for the router navigation to happen
    await router.isReady();
    expect(router.currentRoute.value.path).toBe('/dashboard');
  });
  
  it('displays error message on login failure', async () => {
    // Mock the login method to reject with an error
    const errorMessage = 'Invalid credentials';
    authStore.login.mockRejectedValue(new Error(errorMessage));
    
    // Set form values
    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('wrong-password');
    
    // Submit the form
    await wrapper.find('form').trigger('submit');
    
    // Check that the error message is displayed
    expect(wrapper.find('.error-message').exists()).toBe(true);
    expect(wrapper.find('.error-message').text()).toBe(errorMessage);
  });
  
  it('disables the submit button while loading', async () => {
    // Create a promise that we can resolve manually to control the loading state
    let resolveLogin;
    const loginPromise = new Promise(resolve => {
      resolveLogin = resolve;
    });
    
    // Mock the login method to use our controlled promise
    authStore.login.mockReturnValue(loginPromise);
    
    // Set form values and submit
    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('password123');
    
    // Submit the form but don't wait for it to complete
    const submitPromise = wrapper.find('form').trigger('submit');
    
    // Check that the button is disabled and shows loading text
    await vi.nextTick();
    const button = wrapper.find('button[type="submit"]');
    expect(button.attributes('disabled')).toBeDefined();
    expect(button.text()).toBe('Logging in...');
    
    // Resolve the login promise
    resolveLogin();
    await submitPromise;
    
    // Check that the button is enabled again
    await vi.nextTick();
    expect(button.attributes('disabled')).toBeUndefined();
    expect(button.text()).toBe('Login');
  });
});