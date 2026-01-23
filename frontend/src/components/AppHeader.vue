<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="header">
    <div class="header-content">
      <h1 class="logo">Approval Service</h1>
      <nav class="nav">
        <router-link to="/" class="nav-link">Dashboard</router-link>
        <router-link to="/clients" class="nav-link">Clients</router-link>
        <router-link to="/deliverables" class="nav-link">Deliverables</router-link>
        <router-link to="/approvals" class="nav-link">Approvals</router-link>
      </nav>
      <div class="user-info">
        <span class="username">{{ authStore.user?.username }}</span>
        <span class="role">({{ authStore.user?.role }})</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  font-size: 1.25rem;
  font-weight: 600;
}

.nav {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #34495e;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 500;
}

.role {
  color: #bdc3c7;
  font-size: 0.875rem;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c0392b;
}
</style>
