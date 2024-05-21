<template>
  <!-- the iframe is allowed to be maximised-->
  <div class="grid m-4">
    <label for="poemText" class="col-2">Your Poem Line: </label>
    <InputText class="col-10" id="poemText" v-model="poemText" />
    <label for="comments" class="col-2">Additional comments: </label>

    <InputText id="comments" class="col-9" v-model="submissionText" />
    <Button class="col-1" label="Submit" @click="submitData" />
  </div>
</template>

<script lang="ts">
import { onMounted, ref, type PropType, nextTick } from 'vue'
import html2canvas from 'html2canvas'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

import type { TaskSubmission, DisplayMessage, SubmissionObject } from '@/stores/types'

export default {
  name: 'PoetryComponent',
  components: { Button, InputText },
  props: {
    inputData: {
      type: Object as PropType<SubmissionObject>,
      required: false
    }
  },
  data() {
    return {
      submissionText: '',
      poemText: ''
    }
  },
  emits: ['submit', 'updateHistory'],
  methods: {
    /**
     * This method is used by the game to submit the data to the task
     */
    async submitData() {
      console.log('Submitting data')
      const submission = {} as SubmissionObject
      submission.role = 'user'
      submission.poemText = this.poemText
      submission.commentText = this.submissionText
      const displayData = {} as DisplayMessage
      displayData.role = 'user'
      displayData.containsImage = false
      displayData.message = this.poemText
      displayData.role = 'user'
      displayData.handled = false
      const submissionData: TaskSubmission = {
        submission: submission,
        displayData: displayData
      }
      this.$emit('submit', submissionData)
      this.poemText = ''
      this.submissionText = ''
    }
  },
  watch: {
    async inputData(newValue: SubmissionObject) {
      if (!newValue) {
        console.log('No data provided')
        return
      }
      // Wait till the element got actually updated.
      // This will error in the Godot game and not be processed correctly.
      const displayData = {} as DisplayMessage
      displayData.containsImage = false
      displayData.message = newValue.poemText
      displayData.role = 'AI'
      displayData.handled = true
      this.$emit('updateHistory', displayData)
    }
  },
  mounted() {}
}
</script>
