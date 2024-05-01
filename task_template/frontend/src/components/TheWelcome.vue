<script setup lang="ts">
import TaskSelection from './TaskSelection.vue'
</script>

<template>
  <h1>Welcome to the Collaborative AI Arena</h1>
  <div class="flex flex-row">
    <div class="w-8">
      Welcome to the Collaborative AI Arena. This is a place where you can interact with AI models
      in real-time collaboratvely working on different tasks. To the right, you can see a list of
      tasks that you can currently work on. Once a task is completed you will be asked to give
      feedback on the model's performance. To get started, select a task from the list on the right
      and start a conversation. Have Fun!
    </div>
    <div class="w-4">
      <TaskSelection></TaskSelection>
    </div>
  </div>
</template>
