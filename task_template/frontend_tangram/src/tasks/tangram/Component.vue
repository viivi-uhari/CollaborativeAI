<template>
  <!-- the iframe is allowed to be maximised-->
  <iframe
    width="1000px"
    height="562px"
    ref="iframe"
    frameborder="0"
    allowfullscreen="true"
    id="game_drop"
    allowtransparency="true"
    allow="autoplay; fullscreen *; geolocation; microphone; camera; midi; monetization; xr-spatial-tracking; gamepad; gyroscope; accelerometer; xr; cross-origin-isolated"
    mozallowfullscreen="true"
    msallowfullscreen="true"
    scrolling="no"
    webkitallowfullscreen="true"
  />
  <InputField
    v-model:inputText="submissionText"
    :isLoading="false"
    :allowText="true"
    @submit="submitData"
  />
</template>

<script lang="ts">
import { onMounted, ref, type PropType, nextTick } from 'vue'
import type { TangramGame } from './types'
import type { TaskSubmission, DisplayMessage, SubmissionObject } from '@/stores/types'
import InputField from '@/components/InputField.vue'
import html2canvas from 'html2canvas'

export default {
  name: 'TangramComponent',
  components: { InputField },
  props: {
    inputData: {
      type: Object as PropType<SubmissionObject>,
      required: false
    }
  },
  emits: ['submit', 'updateHistory'],
  setup(props) {
    const iframe = ref<HTMLIFrameElement | null>(null)
    const aiMessage = ref<DisplayMessage | null>(null)
    const setData = ref<Function | null>(null)
    const getData = ref<Function | null>(null)
    const tangramData = ref<TangramGame | null>(null)
    const submissionText = ref<string>('')
    return {
      iframe,
      tangramData,
      submissionText,
      aiMessage
    }
  },
  methods: {
    /**
     * This method is used by the game to submit the data to the task
     */

    async submitData() {
      console.log('Calling submit Data!')
      const submissionData = {} as TaskSubmission
      const displayData = {} as DisplayMessage
      displayData.containsImage = true
      displayData.message = this.submissionText
      displayData.role = 'user'
      displayData.handled = false
      // take a screenshot of the game
      if (this.iframe && this.iframe.contentDocument) {
        const canvas = await html2canvas(this.iframe.contentDocument.body)
        const imgData = canvas.toDataURL()
        displayData.imageURL = imgData
      }
      submissionData.displayData = displayData
      const submission = {} as SubmissionObject
      submission.role = 'user'
      submission.data = {
        message: this.submissionText,
        image: displayData.imageURL,
        tangramData: 'Irrelevant'
      }
      submissionData.submission = submission
      console.log('Emitting data')
      this.$emit('submit', submissionData)
      this.submissionText = ''
    },

    // build the ai Message
    async buildHistory() {
      if (this.aiMessage == null) {
        console.error('No AI message to build history')
        return
      }
      // take a new screenshot, with what is in the tangram after the AI's move
      if (this.iframe && this.iframe.contentDocument) {
        console.log('Taking Sreenshot of AI Move')
        const canvas = await html2canvas(this.iframe.contentDocument.body)
        const imgData = canvas.toDataURL()
        this.aiMessage.imageURL = imgData
      }
      this.$emit('updateHistory', this.aiMessage)
      // reset the aiMessage
      this.aiMessage = null
    },
    async frameLoaded() {
      console.log('Frame loaded')
    }
  },
  watch: {
    async inputData(newValue) {
      if (!newValue) {
        console.log('No data provided')
        return
      }
      // Wait till the element got actually updated.
      await nextTick()
      try {
        const displayData = {} as DisplayMessage
        displayData.containsImage = false
        displayData.message = newValue.data.tangram
        displayData.role = 'AI'
        displayData.handled = true
        this.aiMessage = displayData
        this.$emit('updateHistory', this.aiMessage)
      } catch {
        // This will error in the Godot game and not be processed correctly.
        const displayData = {} as DisplayMessage
        displayData.containsImage = false
        displayData.message = `The data returned by the AI was unexpected. The message was: ${newValue.data}`
        displayData.role = 'AI'
        displayData.handled = true
        this.aiMessage = displayData
        this.$emit('updateHistory', this.aiMessage)
        return
      }
    }
  },
  mounted() {
    if (this.iframe) {
      console.log('There is an iframe')
      const iframeContent = this.iframe.contentWindow as any
      this.iframe.src = '/godot_games/tangram/tangram.html'
      nextTick()
      console.log(iframeContent.taskLoaded)
    }
  }
}
</script>
