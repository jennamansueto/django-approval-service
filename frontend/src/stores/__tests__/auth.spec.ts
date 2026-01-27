import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '../auth'

vi.mock('@/api/client', () => ({
  authApi: {
    login: vi.fn(),
    logout: vi.fn(),
    me: vi.fn(),
  },
}))

import { authApi } from '@/api/client'

const mockUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  role: 'PLANNER',
}

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('initial state', () => {
    it('should have null user initially', () => {
      const store = useAuthStore()
      expect(store.user).toBeNull()
    })

    it('should have loading as false initially', () => {
      const store = useAuthStore()
      expect(store.loading).toBe(false)
    })

    it('should have error as null initially', () => {
      const store = useAuthStore()
      expect(store.error).toBeNull()
    })

    it('should not be authenticated initially', () => {
      const store = useAuthStore()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should have null userRole initially', () => {
      const store = useAuthStore()
      expect(store.userRole).toBeNull()
    })
  })

  describe('login', () => {
    it('should set user on successful login', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })

      const store = useAuthStore()
      const result = await store.login('testuser', 'password123')

      expect(result).toBe(true)
      expect(store.user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)
      expect(store.userRole).toBe('PLANNER')
      expect(store.error).toBeNull()
    })

    it('should set loading to true during login', async () => {
      let resolveLogin: (value: unknown) => void
      const loginPromise = new Promise((resolve) => {
        resolveLogin = resolve
      })
      vi.mocked(authApi.login).mockReturnValue(loginPromise as never)

      const store = useAuthStore()
      const loginCall = store.login('testuser', 'password123')

      expect(store.loading).toBe(true)

      resolveLogin!({ data: mockUser })
      await loginCall

      expect(store.loading).toBe(false)
    })

    it('should set error on failed login', async () => {
      vi.mocked(authApi.login).mockRejectedValue(new Error('Unauthorized'))

      const store = useAuthStore()
      const result = await store.login('testuser', 'wrongpassword')

      expect(result).toBe(false)
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(store.error).toBe('Invalid credentials')
    })

    it('should set loading to false after failed login', async () => {
      vi.mocked(authApi.login).mockRejectedValue(new Error('Unauthorized'))

      const store = useAuthStore()
      await store.login('testuser', 'wrongpassword')

      expect(store.loading).toBe(false)
    })

    it('should clear previous error on new login attempt', async () => {
      vi.mocked(authApi.login).mockRejectedValueOnce(new Error('Unauthorized'))

      const store = useAuthStore()
      await store.login('testuser', 'wrongpassword')
      expect(store.error).toBe('Invalid credentials')

      vi.mocked(authApi.login).mockResolvedValueOnce({ data: mockUser })
      await store.login('testuser', 'correctpassword')
      expect(store.error).toBeNull()
    })

    it('should call authApi.login with correct credentials', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })

      const store = useAuthStore()
      await store.login('myuser', 'mypassword')

      expect(authApi.login).toHaveBeenCalledWith('myuser', 'mypassword')
    })
  })

  describe('logout', () => {
    it('should clear user on logout', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.logout).mockResolvedValue({})

      const store = useAuthStore()
      await store.login('testuser', 'password123')
      expect(store.user).toEqual(mockUser)

      await store.logout()
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should call authApi.logout', async () => {
      vi.mocked(authApi.logout).mockResolvedValue({})

      const store = useAuthStore()
      await store.logout()

      expect(authApi.logout).toHaveBeenCalled()
    })

    it('should clear user even if logout API call fails', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.logout).mockRejectedValue(new Error('Network error'))

      const store = useAuthStore()
      await store.login('testuser', 'password123')
      expect(store.user).toEqual(mockUser)

      await expect(store.logout()).rejects.toThrow('Network error')
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('fetchUser', () => {
    it('should set user when fetchUser succeeds', async () => {
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser })

      const store = useAuthStore()
      await store.fetchUser()

      expect(store.user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)
      expect(store.userRole).toBe('PLANNER')
    })

    it('should call authApi.me', async () => {
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser })

      const store = useAuthStore()
      await store.fetchUser()

      expect(authApi.me).toHaveBeenCalled()
    })

    it('should set user to null when fetchUser fails', async () => {
      vi.mocked(authApi.me).mockRejectedValue(new Error('Unauthorized'))

      const store = useAuthStore()
      await store.fetchUser()

      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should clear existing user when fetchUser fails', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.me).mockRejectedValue(new Error('Session expired'))

      const store = useAuthStore()
      await store.login('testuser', 'password123')
      expect(store.user).toEqual(mockUser)

      await store.fetchUser()
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('user state persistence', () => {
    it('should maintain user state across multiple actions', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.me).mockResolvedValue({ data: mockUser })

      const store = useAuthStore()

      await store.login('testuser', 'password123')
      expect(store.user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)

      await store.fetchUser()
      expect(store.user).toEqual(mockUser)
      expect(store.isAuthenticated).toBe(true)
    })

    it('should update user when fetchUser returns different data', async () => {
      const updatedUser = { ...mockUser, role: 'ADMIN' }
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.me).mockResolvedValue({ data: updatedUser })

      const store = useAuthStore()

      await store.login('testuser', 'password123')
      expect(store.userRole).toBe('PLANNER')

      await store.fetchUser()
      expect(store.userRole).toBe('ADMIN')
      expect(store.user).toEqual(updatedUser)
    })

    it('should correctly compute isAuthenticated based on user state', async () => {
      vi.mocked(authApi.login).mockResolvedValue({ data: mockUser })
      vi.mocked(authApi.logout).mockResolvedValue({})

      const store = useAuthStore()

      expect(store.isAuthenticated).toBe(false)

      await store.login('testuser', 'password123')
      expect(store.isAuthenticated).toBe(true)

      await store.logout()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should correctly compute userRole based on user state', async () => {
      const adminUser = { ...mockUser, role: 'ADMIN' }
      vi.mocked(authApi.login).mockResolvedValue({ data: adminUser })
      vi.mocked(authApi.logout).mockResolvedValue({})

      const store = useAuthStore()

      expect(store.userRole).toBeNull()

      await store.login('admin', 'password123')
      expect(store.userRole).toBe('ADMIN')

      await store.logout()
      expect(store.userRole).toBeNull()
    })
  })
})
