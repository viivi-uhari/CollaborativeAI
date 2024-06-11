<template>
  <div ref="displayArea" class="flex flex-grow-1 flex-column align-content-between h-full">
    <div ref="titleArea" class="taskview-header">
      <h1>{{ task.title }}</h1>
      <p>{{ task.description }}</p>
      <div v-if="currentInteraction.objective">
        Our current THEME is: {{ currentInteraction.objective }}
      </div>
      <InputField
        v-else
        v-model:inputText="taskObjective"
        :isLoading="false"
        :allowText="true"
        @submit="finishedObjective()"
      />
    </div>

    <div v-if="currentInteraction.objective">
      <ScrollPanel ref="chatpanel" :style="{ height: scrollpaneMax + 'px' }">
        <ConversationDisplay :conversation="currentInteraction.history" />
        <TaskInterface
          v-show="!currentInteraction.isLoading"
          @newSubmission="scrollToBottom"
          :task-component="task.id"
          :input-data="lastInteraction"
        ></TaskInterface>
        <div v-if="currentInteraction.isLoading" class="flex justify-center">
          AI Calculating...
          <ProgressSpinner v-if="currentInteraction.isLoading" />
        </div>
        <Button v-if="!showRatings" @click="() => (showRatings = true)" label="Finish" />
        <Ratings v-else @submitRating="submitRating" />
      </ScrollPanel>
    </div>
  </div>
</template>

<script lang="ts">
import ScrollPanel from 'primevue/scrollpanel'
import Button from 'primevue/button'
import ConversationDisplay from '@/components/ConversationDisplay.vue'
import InputField from '@/components/InputField.vue'
import TaskInterface from '@/components/TaskInterface.vue'
import Ratings from '@/components/Ratings.vue'

import { defineComponent } from 'vue'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { useResizeObserver } from '@vueuse/core'
import ProgressSpinner from 'primevue/progressspinner'

import type { TaskSubmission, DisplayMessage, SubmissionObject } from '@/stores/types'

export default defineComponent({
  name: 'TaskView',
  components: {
    Button,
    ConversationDisplay,
    ScrollPanel,
    InputField,
    TaskInterface,
    ProgressSpinner,
    Ratings
  },
  data() {
    return {
      taskObjective: '',
      scrollpaneMax: 300,
      showRatings: false
    }
  },
  setup() {
    const taskStore = useTaskStore()
    const { task, currentInteraction, lastInteraction } = storeToRefs(taskStore)
    return { task, currentInteraction, lastInteraction, taskStore }
  },
  methods: {
    async scrollToBottom(): Promise<void> {
      const scrollPaneRef = this.$refs.chatpanel as any //Ref<ScrollPanel>;
      const content = scrollPaneRef.$el.querySelector('.p-scrollpanel-content')
      if (!content) return
      // set the position of the scrollpane.
      content.scrollTop = content.scrollHeight
    },
    finishedObjective() {
      this.taskStore.startTask()
      this.taskStore.setObjective(this.taskObjective)
      const submission = {} as SubmissionObject
      submission.role = 'user'
      submission.poemText = ''
      submission.commentText = 'You start'
      const displayData = {} as DisplayMessage
      displayData.role = 'user'
      displayData.containsImage = false
      displayData.message = ''
      displayData.role = 'user'
      displayData.handled = false
      const start: TaskSubmission = {
        submission: submission,
        displayData: displayData
      }
      this.taskStore.submitUserInput(start)
    },
    updateHeights() {
      const area = this.$refs.displayArea as HTMLElement
      const rightSideHeight = area == null ? 600 : area.offsetHeight
      const titleArea = this.$refs.titleArea as HTMLElement
      const titleHeight = titleArea == null ? 200 : titleArea.offsetHeight
      this.scrollpaneMax = rightSideHeight - titleHeight
    },
    submitRating(rating: number) {
      this.taskStore.finishTask(rating)
      this.showRatings = false
      this.$router.push({ name: 'task' })
    }
  },
  mounted() {
    const rhs = this.$refs.displayArea as HTMLDivElement
    useResizeObserver(rhs, (entries: any) => {
      this.updateHeights()
    })
    this.updateHeights()
  }
})
</script>
