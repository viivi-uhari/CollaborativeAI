<template>
  <div>
    <component
      :is="TaskComponent"
      @submit="submitData"
      @updateHistory="updateHistory"
      :inputData="inputData"
    />
  </div>
</template>

<script setup lang="ts">
import type { DisplayMessage, TaskSubmission } from '@/stores/types'
import { useTaskStore } from '@/stores'
import { onMounted, ref, defineAsyncComponent, nextTick } from 'vue'
import { storeToRefs } from 'pinia'

const props = defineProps({
  taskComponent: {
    type: String,
    required: true
  },
  inputData: {
    type: Object,
    required: false
  }
})
const TaskComponent = defineAsyncComponent(
  () => import(`./../tasks/${props.taskComponent}/Component.vue`)
)
const emits = defineEmits(['newSubmission'])
const taskStore = useTaskStore()
const { currentInteraction } = storeToRefs(taskStore)
function submitData(newData: TaskSubmission) {
  console.log('Submitting data')
  taskStore.submitUserInput(newData)
  emits('newSubmission')
}

async function updateHistory(newData: DisplayMessage) {
  currentInteraction.value.history.push(newData)
  console.log('History updated')
  await nextTick()
  emits('newSubmission')
}
</script>
