import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => user.value !== null)
  const userRole = computed(() => user.value?.role ?? null)

  async function login(username: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(username, password)
      user.value = response.data
      return true
    } catch (e) {
      error.value = 'Invalid credentials'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
    }
  }

  async function fetchUser() {
    try {
      const response = await authApi.me()
      user.value = response.data
    } catch {
      user.value = null
    }
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    userRole,
    login,
    logout,
    fetchUser,
  }
})
