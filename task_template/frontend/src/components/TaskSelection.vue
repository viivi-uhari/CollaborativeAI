<script setup lang="ts">
import Listbox, { type ListboxChangeEvent } from 'primevue/listbox'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { ref } from 'vue'
const taskStore = useTaskStore()
const { tasks, selectedTask } = storeToRefs(taskStore)
const choosenTask = ref(null)
function taskSelected(event: ListboxChangeEvent) {
  console.log(choosenTask.value)
  if (choosenTask.value) {
    taskStore.selectTask(choosenTask.value)
    // Now that we have selected a Task, change to the task view
    router.push('/task')
  }
  console.log(event)
}
</script>

<template>
  <Listbox @change="taskSelected" v-model="choosenTask" :options="tasks" optionLabel="title" />
</template>
