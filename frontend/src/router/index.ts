import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ClientsView from '@/views/ClientsView.vue'
import DeliverablesView from '@/views/DeliverablesView.vue'
import ApprovalsView from '@/views/ApprovalsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true },
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/clients',
      name: 'clients',
      component: ClientsView,
    },
    {
      path: '/deliverables',
      name: 'deliverables',
      component: DeliverablesView,
    },
    {
      path: '/approvals',
      name: 'approvals',
      component: ApprovalsView,
    },
  ],
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  // Try to fetch user if not already loaded
  if (!authStore.user && !authStore.loading) {
    await authStore.fetchUser()
  }
  
  // Allow public routes
  if (to.meta.public) {
    // Redirect to dashboard if already logged in
    if (authStore.isAuthenticated && to.name === 'login') {
      return next({ name: 'dashboard' })
    }
    return next()
  }
  
  // Redirect to login if not authenticated
  if (!authStore.isAuthenticated) {
    return next({ name: 'login' })
  }
  
  next()
})

export default router
