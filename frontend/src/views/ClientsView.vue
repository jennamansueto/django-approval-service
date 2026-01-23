<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { clientsApi, type Client } from '@/api/client'
import DataTable from '@/components/DataTable.vue'

const clients = ref<Client[]>([])
const loading = ref(true)
const newClientName = ref('')
const showForm = ref(false)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Name' },
  { key: 'created_at', label: 'Created' },
]

onMounted(async () => {
  await fetchClients()
})

async function fetchClients() {
  loading.value = true
  try {
    const response = await clientsApi.list()
    clients.value = response.data
  } finally {
    loading.value = false
  }
}

async function createClient() {
  if (!newClientName.value.trim()) return
  await clientsApi.create(newClientName.value)
  newClientName.value = ''
  showForm.value = false
  await fetchClients()
}
</script>

<template>
  <div class="clients-view">
    <div class="header">
      <h1>Clients</h1>
      <button @click="showForm = !showForm" class="btn-primary">
        {{ showForm ? 'Cancel' : 'Add Client' }}
      </button>
    </div>

    <div v-if="showForm" class="form-card">
      <form @submit.prevent="createClient" class="inline-form">
        <input
          v-model="newClientName"
          type="text"
          placeholder="Client name"
          required
        />
        <button type="submit" class="btn-primary">Create</button>
      </form>
    </div>

    <DataTable :columns="columns" :data="clients" :loading="loading">
      <template #created_at="{ value }">
        {{ new Date(value as string).toLocaleDateString() }}
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.clients-view h1 {
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

.form-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.inline-form {
  display: flex;
  gap: 12px;
}

.inline-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
