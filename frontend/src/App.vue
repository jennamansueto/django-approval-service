<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="app">
    <AppHeader v-if="authStore.isAuthenticated" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
