<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useTaskStore } from './stores'

onMounted(() => {
  const taskStore = useTaskStore()
  taskStore.updateTasks()
})
</script>

<template>
  <RouterView class="h-screen" />
</template>

<style scoped></style>
