<script setup lang="ts">
import Message from 'primevue/message'
import { computed } from 'vue'
import ConversationItem from './ConversationItem.vue'

import type { DisplayMessage } from '@/stores/types'
import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'

const props = defineProps({
  conversation: Array<DisplayMessage>,
  userInitials: { type: String, default: 'You' },
  modelName: { type: String, default: 'AI' }
})
const emit = defineEmits(['messagesUpdated', 'askQuestion'])
const taskStore = useTaskStore()
const { selectedTask, currentInteraction, lastInteraction } = storeToRefs(taskStore)
const ai_worked = computed(() => {
  if (currentInteraction.value && currentInteraction.value.history.length > 0 && currentInteraction.value.submissionHistory.length > 0) {
    const submissionitems = currentInteraction.value.submissionHistory.length
    const historyItems = currentInteraction.value.history.length
    console.log("Testing, whether AI Worked")
    if (currentInteraction.value.submissionHistory[submissionitems - 1].role === 'AI') {
      console.log("LAtest submission element is from AI")
      if (currentInteraction.value.history[historyItems - 1].role == 'AI') {
        console.log("Latest history element is from AI")
        return true
      }
      else{
        console.log(currentInteraction.value.history[historyItems - 1])
        return false
      }
    }
    return true
  } else {
    return true
  }
})
</script>

<template>
  <div class="chat-container">
    <ConversationItem
      v-for="(message, index) in conversation"
      class="flex m-1 message"
      :message="message"
      :userName="userInitials"
      :modelName="modelName"
      :loading="conversation ? index == conversation.length - 1 && !message.handled : false"
      :key="index"
    >
    </ConversationItem>
    <Message v-if="!ai_worked" severity="error">Latest response from AI could not be interpreted</Message>
  </div>
</template>
<style scoped>
.message {
  margin-bottom: 10px;
}
.chat-container {
  width: 100%;
  padding-right: 1rem;
}
</style>
