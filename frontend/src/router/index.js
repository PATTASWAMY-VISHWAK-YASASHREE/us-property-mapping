import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Lazy-loaded components for better performance
const HomeView = () => import('../views/HomeView.vue')
const LoginView = () => import('../views/auth/LoginView.vue')
const RegisterView = () => import('../views/auth/RegisterView.vue')
const ForgotPasswordView = () => import('../views/auth/ForgotPasswordView.vue')
const DashboardView = () => import('../views/DashboardView.vue')
const MapView = () => import('../views/MapView.vue')
const PropertyView = () => import('../views/PropertyView.vue')
const OwnerView = () => import('../views/OwnerView.vue')
const SearchResultsView = () => import('../views/SearchResultsView.vue')
const ReportsView = () => import('../views/ReportsView.vue')
const ProfileView = () => import('../views/ProfileView.vue')
const AdminView = () => import('../views/admin/AdminView.vue')
const CompanyManagementView = () => import('../views/admin/CompanyManagementView.vue')
const UserManagementView = () => import('../views/admin/UserManagementView.vue')
const NotFoundView = () => import('../views/NotFoundView.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/map',
    name: 'map',
    component: MapView,
    meta: { requiresAuth: true }
  },
  {
    path: '/property/:id',
    name: 'property',
    component: PropertyView,
    meta: { requiresAuth: true }
  },
  {
    path: '/owner/:id',
    name: 'owner',
    component: OwnerView,
    meta: { requiresAuth: true }
  },
  {
    path: '/search',
    name: 'search',
    component: SearchResultsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/companies',
    name: 'company-management',
    component: CompanyManagementView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'user-management',
    component: UserManagementView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  
  // Check if route requires authentication
  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } 
  // Check if route requires admin role
  else if (requiresAdmin && !authStore.isAdmin) {
    next({ name: 'dashboard' })
  } 
  // If user is already logged in and tries to access login/register pages
  else if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'dashboard' })
  } 
  // Otherwise proceed normally
  else {
    next()
  }
})

export default router