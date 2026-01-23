<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { approvalsApi, type ApprovalRequest } from '@/api/client'
import StatusBadge from '@/components/StatusBadge.vue'

const pendingApprovals = ref<ApprovalRequest[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await approvalsApi.list('PENDING')
    pendingApprovals.value = response.data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div class="card">
      <h2>Pending Approvals</h2>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="pendingApprovals.length === 0" class="empty">
        No pending approvals
      </div>
      <ul v-else class="approval-list">
        <li v-for="approval in pendingApprovals" :key="approval.id" class="approval-item">
          <div class="approval-info">
            <strong>{{ approval.deliverable_title }}</strong>
            <span class="meta">Requested by {{ approval.requested_by_username }}</span>
          </div>
          <StatusBadge :status="approval.status" />
        </li>
      </ul>
      <router-link to="/approvals" class="view-all">View all approvals →</router-link>
    </div>
  </div>
</template>

<style scoped>
.dashboard h1 {
  margin-bottom: 24px;
  color: #2c3e50;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card h2 {
  margin-bottom: 16px;
  color: #2c3e50;
  font-size: 1.25rem;
}

.loading, .empty {
  color: #7f8c8d;
  padding: 20px 0;
}

.approval-list {
  list-style: none;
}

.approval-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ecf0f1;
}

.approval-item:last-child {
  border-bottom: none;
}

.approval-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta {
  color: #7f8c8d;
  font-size: 0.875rem;
}

.view-all {
  display: inline-block;
  margin-top: 16px;
  color: #3498db;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}
</style>
