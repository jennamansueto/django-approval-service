<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { deliverablesApi, clientsApi, type Deliverable, type Client } from '@/api/client'
import DataTable from '@/components/DataTable.vue'
import StatusBadge from '@/components/StatusBadge.vue'

const deliverables = ref<Deliverable[]>([])
const clients = ref<Client[]>([])
const loading = ref(true)
const showForm = ref(false)

const newDeliverable = ref({
  title: '',
  description: '',
  client: 0,
})

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'title', label: 'Title' },
  { key: 'client_name', label: 'Client' },
  { key: 'status', label: 'Status' },
  { key: 'created_by_username', label: 'Created By' },
]

onMounted(async () => {
  await Promise.all([fetchDeliverables(), fetchClients()])
})

async function fetchDeliverables() {
  loading.value = true
  try {
    const response = await deliverablesApi.list()
    deliverables.value = response.data
  } finally {
    loading.value = false
  }
}

async function fetchClients() {
  const response = await clientsApi.list()
  clients.value = response.data
}

async function createDeliverable() {
  if (!newDeliverable.value.title || !newDeliverable.value.client) return
  await deliverablesApi.create(newDeliverable.value)
  newDeliverable.value = { title: '', description: '', client: 0 }
  showForm.value = false
  await fetchDeliverables()
}

async function submitDeliverable(id: number) {
  await deliverablesApi.submit(id)
  await fetchDeliverables()
}
</script>

<template>
  <div class="deliverables-view">
    <div class="header">
      <h1>Deliverables</h1>
      <button @click="showForm = !showForm" class="btn-primary">
        {{ showForm ? 'Cancel' : 'New Deliverable' }}
      </button>
    </div>

    <div v-if="showForm" class="form-card">
      <form @submit.prevent="createDeliverable" class="create-form">
        <div class="form-group">
          <label>Title</label>
          <input v-model="newDeliverable.title" type="text" required />
        </div>
        <div class="form-group">
          <label>Client</label>
          <select v-model="newDeliverable.client" required>
            <option value="0" disabled>Select client</option>
            <option v-for="c in clients" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="newDeliverable.description" rows="3"></textarea>
        </div>
        <button type="submit" class="btn-primary">Create</button>
      </form>
    </div>

    <DataTable :columns="columns" :data="deliverables" :loading="loading">
      <template #status="{ value }">
        <StatusBadge :status="value as string" />
      </template>
      <template #actions="{ row }">
        <button
          v-if="row.status === 'DRAFT'"
          @click="submitDeliverable(row.id as number)"
          class="btn-small"
        >
          Submit
        </button>
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.deliverables-view h1 {
  color: #2c3e50;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-small {
  background-color: #27ae60;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-small:hover {
  background-color: #219a52;
}

.form-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
