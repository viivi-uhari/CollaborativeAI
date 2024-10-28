<template>
  <div class="flex flex-column align-content-between h-screen">
    <div class="taskview-header">
      <Header />
      <h1>{{ task.title }}</h1>
      <TaskDescription />
      <div v-if="currentInteraction.objective">
        The current Objective is: {{ currentInteraction.objective }}
      </div>
      <div v-else>
        Describe what should be built with the tangram pieces
        <InputField
          v-model:inputText="taskObjective"
          :isLoading="false"
          :allowText="true"
          @submit="finishedObjective()"
        />
      </div>
    </div>

    <div v-if="currentInteraction.objective">
      <TaskInterface
        v-show="!currentInteraction.isLoading"
        :task-component="task.id"
        :input-data="lastInteraction"
      ></TaskInterface>
    </div>
    <Footer />
  </div>
</template>

<script lang="ts">
import ScrollPanel from 'primevue/scrollpanel'
import Button from 'primevue/button'
import ConversationDisplay from '@/components/ConversationDisplay.vue'
import InputField from '@/components/InputField.vue'
import TaskInterface from '@/components/TaskInterface.vue'
import Ratings from '@/components/Ratings.vue'
import Header from '@/components/Header.vue'
import TaskDescription from '@/components/TaskDescription.vue'
import Footer from '@/components/Footer.vue'

import { defineComponent } from 'vue'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
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
    ProgressSpinner,
    Ratings,
    Header,
    Footer,
    TaskDescription
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
    finishedObjective() {
      this.taskStore.startTask()
      this.taskStore.setObjective(this.taskObjective)
      console.log(this.currentInteraction)
    }
  },
  mounted() {}
})
</script>
