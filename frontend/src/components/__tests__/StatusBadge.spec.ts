import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StatusBadge from '../StatusBadge.vue'

describe('StatusBadge', () => {
  it('renders the status text', () => {
    const wrapper = mount(StatusBadge, {
      props: { status: 'APPROVED' },
    })
    expect(wrapper.text()).toBe('APPROVED')
  })

  it('applies correct color for APPROVED status', () => {
    const wrapper = mount(StatusBadge, {
      props: { status: 'APPROVED' },
    })
    expect(wrapper.attributes('style')).toContain('background-color: #27ae60')
  })

  it('applies correct color for REJECTED status', () => {
    const wrapper = mount(StatusBadge, {
      props: { status: 'REJECTED' },
    })
    expect(wrapper.attributes('style')).toContain('background-color: #e74c3c')
  })

  // INTENTIONAL GAP: No test for PENDING status
  // INTENTIONAL GAP: No test for unknown status fallback
})
