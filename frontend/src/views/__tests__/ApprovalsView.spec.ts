import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ApprovalsView from '../ApprovalsView.vue'

vi.mock('@/api/client', () => ({
  approvalsApi: {
    list: vi.fn().mockResolvedValue({ data: [] }),
    approve: vi.fn().mockResolvedValue({ data: {} }),
    reject: vi.fn().mockResolvedValue({ data: {} }),
  },
}))

describe('ApprovalsView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders the approvals title', () => {
    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: ['DataTable', 'StatusBadge'],
      },
    })
    expect(wrapper.find('h1').text()).toBe('Approvals')
  })

  it('renders the DataTable component', () => {
    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: {
          DataTable: true,
          StatusBadge: true,
        },
      },
    })
    expect(wrapper.findComponent({ name: 'DataTable' }).exists()).toBe(true)
  })

  it('calls approvalsApi.list on mount', async () => {
    const { approvalsApi } = await import('@/api/client')
    mount(ApprovalsView, {
      global: {
        stubs: ['DataTable', 'StatusBadge'],
      },
    })
    expect(approvalsApi.list).toHaveBeenCalled()
  })

  it('renders approve and reject buttons for pending approvals', async () => {
    const { approvalsApi } = await import('@/api/client')
    vi.mocked(approvalsApi.list).mockResolvedValue({
      data: [
        {
          id: 1,
          deliverable: 1,
          deliverable_title: 'Test Deliverable',
          requested_by: 1,
          requested_by_username: 'testuser',
          status: 'PENDING',
          created_at: '2026-01-27T00:00:00Z',
          decided_at: null,
        },
      ],
    })

    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: {
          DataTable: {
            template: `
              <div>
                <slot name="actions" :row="{ id: 1, status: 'PENDING' }"></slot>
              </div>
            `,
          },
          StatusBadge: true,
        },
      },
    })

    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.btn-approve').exists()).toBe(true)
    expect(wrapper.find('.btn-reject').exists()).toBe(true)
    expect(wrapper.find('.btn-approve').text()).toBe('Approve')
    expect(wrapper.find('.btn-reject').text()).toBe('Reject')
  })

  it('does not render action buttons for non-pending approvals', async () => {
    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: {
          DataTable: {
            template: `
              <div>
                <slot name="actions" :row="{ id: 1, status: 'APPROVED' }"></slot>
              </div>
            `,
          },
          StatusBadge: true,
        },
      },
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.find('.btn-approve').exists()).toBe(false)
    expect(wrapper.find('.btn-reject').exists()).toBe(false)
  })

  it('calls approvalsApi.approve when approve button is clicked', async () => {
    const { approvalsApi } = await import('@/api/client')
    vi.mocked(approvalsApi.list).mockResolvedValue({ data: [] })
    vi.mocked(approvalsApi.approve).mockResolvedValue({ data: {} })

    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: {
          DataTable: {
            template: `
              <div>
                <slot name="actions" :row="{ id: 1, status: 'PENDING' }"></slot>
              </div>
            `,
          },
          StatusBadge: true,
        },
      },
    })

    await wrapper.vm.$nextTick()

    await wrapper.find('.btn-approve').trigger('click')
    await wrapper.vm.$nextTick()

    expect(approvalsApi.approve).toHaveBeenCalledWith(1)
  })

  it('calls approvalsApi.reject when reject button is clicked', async () => {
    const { approvalsApi } = await import('@/api/client')
    vi.mocked(approvalsApi.list).mockResolvedValue({ data: [] })
    vi.mocked(approvalsApi.reject).mockResolvedValue({ data: {} })

    const wrapper = mount(ApprovalsView, {
      global: {
        stubs: {
          DataTable: {
            template: `
              <div>
                <slot name="actions" :row="{ id: 1, status: 'PENDING' }"></slot>
              </div>
            `,
          },
          StatusBadge: true,
        },
      },
    })

    await wrapper.vm.$nextTick()

    await wrapper.find('.btn-reject').trigger('click')
    await wrapper.vm.$nextTick()

    expect(approvalsApi.reject).toHaveBeenCalledWith(1)
  })
})
