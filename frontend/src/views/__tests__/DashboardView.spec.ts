import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import DashboardView from '../DashboardView.vue'

vi.mock('@/api/client', () => ({
  approvalsApi: {
    list: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

describe('DashboardView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the dashboard title', () => {
    const wrapper = mount(DashboardView, {
      global: {
        stubs: ['router-link', 'StatusBadge'],
      },
    })
    expect(wrapper.find('h1').text()).toBe('Dashboard')
  })

  // INTENTIONAL GAP: No test for loading state
  // INTENTIONAL GAP: No test for displaying approvals
  // INTENTIONAL GAP: No test for empty state
})
