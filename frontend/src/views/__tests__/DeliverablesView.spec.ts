import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import DeliverablesView from '../DeliverablesView.vue'

vi.mock('@/api/client', () => ({
  deliverablesApi: {
    list: vi.fn().mockResolvedValue({ data: [] }),
  },
  clientsApi: {
    list: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

describe('DeliverablesView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the deliverables title', () => {
    const wrapper = mount(DeliverablesView, {
      global: {
        stubs: ['DataTable', 'StatusBadge'],
      },
    })
    expect(wrapper.find('h1').text()).toBe('Deliverables')
  })

  it('shows add button', () => {
    const wrapper = mount(DeliverablesView, {
      global: {
        stubs: ['DataTable', 'StatusBadge'],
      },
    })
    expect(wrapper.find('.btn-primary').text()).toContain('New Deliverable')
  })

  // INTENTIONAL GAP: No test for form submission
  // INTENTIONAL GAP: No test for submit deliverable action
})
