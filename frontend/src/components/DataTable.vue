<script setup lang="ts">
defineProps<{
  columns: { key: string; label: string }[]
  data: Record<string, unknown>[]
  loading?: boolean
}>()
</script>

<template>
  <div class="table-container">
    <div v-if="loading" class="loading">Loading...</div>
    <table v-else class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
          <slot name="header-actions"><th></th></slot>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td v-for="col in columns" :key="col.key">
            <slot :name="col.key" :value="row[col.key]" :row="row">
              {{ row[col.key] }}
            </slot>
          </td>
          <td>
            <slot name="actions" :row="row"></slot>
          </td>
        </tr>
        <tr v-if="data.length === 0">
          <td :colspan="columns.length + 1" class="empty">No data available</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading {
  padding: 40px;
  text-align: center;
  color: #7f8c8d;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.data-table tr:hover {
  background-color: #f8f9fa;
}

.empty {
  text-align: center;
  color: #7f8c8d;
  padding: 40px;
}
</style>
