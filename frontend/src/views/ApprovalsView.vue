<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { approvalsApi, type ApprovalRequest } from '@/api/client'
import DataTable from '@/components/DataTable.vue'
import StatusBadge from '@/components/StatusBadge.vue'

const approvals = ref<ApprovalRequest[]>([])
const loading = ref(true)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'deliverable_title', label: 'Deliverable' },
  { key: 'requested_by_username', label: 'Requested By' },
  { key: 'status', label: 'Status' },
  { key: 'created_at', label: 'Created' },
]

onMounted(async () => {
  await fetchApprovals()
})

async function fetchApprovals() {
  loading.value = true
  try {
    const response = await approvalsApi.list()
    approvals.value = response.data
  } finally {
    loading.value = false
  }
}

async function approve(id: number) {
  await approvalsApi.approve(id)
  await fetchApprovals()
}

async function reject(id: number) {
  await approvalsApi.reject(id)
  await fetchApprovals()
}
</script>

<template>
  <div class="approvals-view">
    <h1>Approvals</h1>

    <DataTable :columns="columns" :data="approvals" :loading="loading">
      <template #status="{ value }">
        <StatusBadge :status="value as string" />
      </template>
      <template #created_at="{ value }">
        {{ new Date(value as string).toLocaleDateString() }}
      </template>
      <template #actions="{ row }">
        <div v-if="row.status === 'PENDING'" class="action-buttons">
          <button @click="approve(row.id as number)" class="btn-approve">Approve</button>
          <button @click="reject(row.id as number)" class="btn-reject">Reject</button>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.approvals-view h1 {
  color: #2c3e50;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-approve {
  background-color: #27ae60;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-approve:hover {
  background-color: #219a52;
}

.btn-reject {
  background-color: #e74c3c;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-reject:hover {
  background-color: #c0392b;
}
</style>
