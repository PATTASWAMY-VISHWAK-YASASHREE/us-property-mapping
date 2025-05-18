import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '../auth';
import axios from 'axios';

// Mock dependencies
vi.mock('axios');
vi.mock('vue-router', () => ({
  default: {
    push: vi.fn(),
    currentRoute: {
      value: {
        query: {}
      }
    }
  }
}));
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn()
  })
}));

// Import the mocked router
import router from '../../router';

describe('Auth Store', () => {
  let store;
  
  beforeEach(() => {
    // Create a fresh pinia instance and make it active
    const pinia = createPinia();
    setActivePinia(pinia);
    
    // Reset localStorage mock
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(null);
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {});
    vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {});
    
    // Reset axios mock
    axios.post.mockReset();
    axios.get.mockReset();
    axios.put.mockReset();
    axios.defaults = { headers: { common: {} } };
    
    // Reset router mock
    router.push.mockReset();
    
    // Create the store
    store = useAuthStore();
  });
  
  afterEach(() => {
    vi.clearAllMocks();
  });
  
  describe('Initial State', () => {
    it('should have correct initial state', () => {
      expect(store.user).toBeNull();
      expect(store.token).toBeNull();
      expect(store.loading).toBe(false);
      expect(store.error).toBeNull();
      expect(store.isAuthenticated).toBe(false);
      expect(store.isAdmin).toBe(false);
      expect(store.userRole).toBe('guest');
      expect(store.userName).toBe('');
      expect(store.userEmail).toBe('');
      expect(store.userCompany).toBeNull();
    });
    
    it('should load token from localStorage if available', () => {
      // Setup localStorage to return a token
      Storage.prototype.getItem.mockReturnValueOnce('test-token');
      
      // Create a new store instance that will use the mocked localStorage
      const newStore = useAuthStore();
      
      expect(newStore.token).toBe('test-token');
      expect(axios.defaults.headers.common['Authorization']).toBe('Bearer test-token');
    });
  });
  
  describe('Login', () => {
    it('should set token and user data on successful login', async () => {
      // Mock successful login response
      axios.post.mockResolvedValueOnce({
        data: {
          access_token: 'test-token',
          refresh_token: 'refresh-token'
        }
      });
      
      // Mock successful user profile fetch
      axios.get.mockResolvedValueOnce({
        data: {
          id: '123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'user',
          company: { id: '456', name: 'Test Company' }
        }
      });
      
      // Call login
      await store.login({ email: 'test@example.com', password: 'password123' });
      
      // Verify state changes
      expect(store.token).toBe('test-token');
      expect(store.user).toEqual({
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user',
        company: { id: '456', name: 'Test Company' }
      });
      expect(store.loading).toBe(false);
      expect(store.error).toBeNull();
      expect(store.isAuthenticated).toBe(true);
      
      // Verify localStorage was updated
      expect(localStorage.setItem).toHaveBeenCalledWith('token', 'test-token');
      
      // Verify axios header was set
      expect(axios.defaults.headers.common['Authorization']).toBe('Bearer test-token');
      
      // Verify router navigation
      expect(router.push).toHaveBeenCalledWith('/dashboard');
    });
    
    it('should handle login failure', async () => {
      // Mock failed login response
      axios.post.mockRejectedValueOnce({
        response: {
          data: {
            detail: 'Invalid credentials'
          }
        }
      });
      
      // Call login
      try {
        await store.login({ email: 'test@example.com', password: 'wrong-password' });
      } catch (e) {
        // Ignore error
      }
      
      // Verify state
      expect(store.token).toBeNull();
      expect(store.user).toBeNull();
      expect(store.loading).toBe(false);
      expect(store.error).toBe('Invalid credentials');
      expect(store.isAuthenticated).toBe(false);
      
      // Verify localStorage was not updated
      expect(localStorage.setItem).not.toHaveBeenCalled();
    });
    
    it('should redirect to requested page after login if specified', async () => {
      // Set up redirect query parameter
      router.currentRoute.value.query.redirect = '/reports';
      
      // Mock successful login response
      axios.post.mockResolvedValueOnce({
        data: {
          access_token: 'test-token',
          refresh_token: 'refresh-token'
        }
      });
      
      // Mock successful user profile fetch
      axios.get.mockResolvedValueOnce({
        data: {
          id: '123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'user'
        }
      });
      
      // Call login
      await store.login({ email: 'test@example.com', password: 'password123' });
      
      // Verify router navigation to the redirect path
      expect(router.push).toHaveBeenCalledWith('/reports');
    });
  });
  
  describe('Logout', () => {
    it('should clear auth state on logout', async () => {
      // Set up initial authenticated state
      store.token = 'test-token';
      store.user = { id: '123', email: 'test@example.com' };
      axios.defaults.headers.common['Authorization'] = 'Bearer test-token';
      
      // Mock successful logout response
      axios.post.mockResolvedValueOnce({});
      
      // Call logout
      await store.logout();
      
      // Verify state is cleared
      expect(store.token).toBeNull();
      expect(store.user).toBeNull();
      expect(store.isAuthenticated).toBe(false);
      
      // Verify localStorage was cleared
      expect(localStorage.removeItem).toHaveBeenCalledWith('token');
      
      // Verify axios header was cleared
      expect(axios.defaults.headers.common['Authorization']).toBeUndefined();
      
      // Verify router navigation
      expect(router.push).toHaveBeenCalledWith('/login');
    });
    
    it('should clear auth state even if logout API call fails', async () => {
      // Set up initial authenticated state
      store.token = 'test-token';
      store.user = { id: '123', email: 'test@example.com' };
      axios.defaults.headers.common['Authorization'] = 'Bearer test-token';
      
      // Mock failed logout response
      axios.post.mockRejectedValueOnce(new Error('Network error'));
      
      // Call logout
      await store.logout();
      
      // Verify state is still cleared despite API error
      expect(store.token).toBeNull();
      expect(store.user).toBeNull();
      expect(store.isAuthenticated).toBe(false);
      expect(localStorage.removeItem).toHaveBeenCalledWith('token');
      expect(router.push).toHaveBeenCalledWith('/login');
    });
  });
  
  describe('User Profile', () => {
    it('should fetch user profile when token is available', async () => {
      // Set up token
      store.token = 'test-token';
      
      // Mock successful profile fetch
      axios.get.mockResolvedValueOnce({
        data: {
          id: '123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'admin'
        }
      });
      
      // Call fetchUserProfile
      await store.fetchUserProfile();
      
      // Verify user data is set
      expect(store.user).toEqual({
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'admin'
      });
      expect(store.isAdmin).toBe(true);
      expect(store.userRole).toBe('admin');
      expect(store.userEmail).toBe('test@example.com');
    });
    
    it('should logout if profile fetch returns 401', async () => {
      // Set up token
      store.token = 'test-token';
      
      // Mock unauthorized response
      axios.get.mockRejectedValueOnce({
        response: {
          status: 401
        }
      });
      
      // Mock logout
      vi.spyOn(store, 'logout').mockImplementation(() => {});
      
      // Call fetchUserProfile
      await store.fetchUserProfile();
      
      // Verify logout was called
      expect(store.logout).toHaveBeenCalled();
    });
  });
  
  describe('Password Management', () => {
    it('should handle forgot password request', async () => {
      // Mock successful forgot password response
      axios.post.mockResolvedValueOnce({
        data: { message: 'Password reset email sent' }
      });
      
      // Call forgotPassword
      const result = await store.forgotPassword('test@example.com');
      
      // Verify API call
      expect(axios.post).toHaveBeenCalledWith('/api/auth/forgot-password', { email: 'test@example.com' });
      expect(result).toEqual({ message: 'Password reset email sent' });
    });
    
    it('should handle password reset', async () => {
      // Mock successful reset password response
      axios.post.mockResolvedValueOnce({
        data: { message: 'Password reset successful' }
      });
      
      // Call resetPassword
      await store.resetPassword('reset-token', 'new-password');
      
      // Verify API call
      expect(axios.post).toHaveBeenCalledWith('/api/auth/reset-password', { 
        token: 'reset-token', 
        new_password: 'new-password' 
      });
      
      // Verify navigation
      expect(router.push).toHaveBeenCalledWith('/login');
    });
    
    it('should handle change password', async () => {
      // Mock successful change password response
      axios.post.mockResolvedValueOnce({
        data: { message: 'Password changed successfully' }
      });
      
      // Call changePassword
      const passwordData = {
        current_password: 'old-password',
        new_password: 'new-password'
      };
      await store.changePassword(passwordData);
      
      // Verify API call
      expect(axios.post).toHaveBeenCalledWith('/api/auth/change-password', passwordData);
    });
  });
  
  describe('Profile Management', () => {
    it('should update user profile', async () => {
      // Mock successful profile update response
      const updatedProfile = {
        id: '123',
        email: 'test@example.com',
        name: 'Updated Name',
        role: 'user'
      };
      axios.put.mockResolvedValueOnce({
        data: updatedProfile
      });
      
      // Call updateProfile
      const profileData = { name: 'Updated Name' };
      const result = await store.updateProfile(profileData);
      
      // Verify API call
      expect(axios.put).toHaveBeenCalledWith('/api/users/me', profileData);
      
      // Verify user data is updated
      expect(store.user).toEqual(updatedProfile);
      expect(result).toEqual(updatedProfile);
    });
  });
});