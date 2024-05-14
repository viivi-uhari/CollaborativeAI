<template>
  <div ref="displayArea" class="flex flex-grow-1 flex-column align-content-between h-full">
    <div ref="titleArea" class="taskview-header">
      <h1>{{ task.title }}</h1>
      <p>{{ task.description }}</p>
      <div v-if="currentInteraction.objective">
        The current Objective is: {{ currentInteraction.objective }}
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
          <ProgressSpinner v-if="currentInteraction.isLoading" />
          AI Calculating...
        </div>
        <router-link to="rating"><Button label="Finish" /></router-link>
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

import { defineComponent } from 'vue'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import { useResizeObserver } from '@vueuse/core'
import ProgressSpinner from 'primevue/progressspinner'

export default defineComponent({
  name: 'TaskView',
  components: {
    Button,
    ConversationDisplay,
    ScrollPanel,
    InputField,
    TaskInterface,
    ProgressSpinner
  },
  data() {
    return {
      taskObjective: '',
      scrollpaneMax: 300
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
      console.log(this.currentInteraction)
    },
    updateHeights() {
      const area = this.$refs.displayArea as HTMLElement
      const rightSideHeight = area == null ? 600 : area.offsetHeight
      const titleArea = this.$refs.titleArea as HTMLElement
      const titleHeight = titleArea == null ? 200 : titleArea.offsetHeight
      this.scrollpaneMax = rightSideHeight - titleHeight
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
