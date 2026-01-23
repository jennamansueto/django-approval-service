<script setup lang="ts">
defineProps<{
  status: string
}>()

const statusColors: Record<string, string> = {
  DRAFT: '#95a5a6',
  SUBMITTED: '#3498db',
  PENDING: '#f39c12',
  APPROVED: '#27ae60',
  REJECTED: '#e74c3c',
  CANCELED: '#7f8c8d',
}
</script>

<template>
  <span
    class="status-badge"
    :style="{ backgroundColor: statusColors[status] || '#95a5a6' }"
  >
    {{ status }}
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}
</style>
