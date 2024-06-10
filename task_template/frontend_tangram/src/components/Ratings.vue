<template>
  <div class="flex flex-column align-items-center w-full">
    <h2>Please rate your experience based on the below metric</h2>
    <h3>"Me and the AI collaborated well in this task"</h3>
    <div class="flex flex-row">
      <div
        v-for="rating in [0, 1, 2, 3, 4, 5, 6]"
        :key="rating"
        class="m-2 cursor-pointer border-circle border-solid border-2 border-900 w-2rem h-2rem flex justify-content-center align-items-center"
        :class="`${colors[rating]}`"
        @click="setRating(rating)"
      >
        {{ rating + 1 }}
      </div>
    </div>
  </div>
</template>

<script>
import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'

export default {
  data() {
    return {
      currentRating: 0,
      colors: ['bg-red-700', 'bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-teal-500', 'bg-green-300', 'bg-green-500']
    }
  },
  methods: {
    setRating(rating) {
      this.currentRating = rating
      this.taskStore.finishTask(rating)
      this.$router.push({ name: 'task' })
    }
  },
  setup() {
    const taskStore = useTaskStore()
    const { selectedTask, currentInteraction, lastInteraction } = storeToRefs(taskStore)
    return { selectedTask, currentInteraction, lastInteraction, taskStore }
  }
}
</script>
