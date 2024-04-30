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
    @load="frameLoaded"
  />
  <InputField
    v-model:inputText="submissionText"
    :isLoading="false"
    :allowText="false"
    @submit="fetchData"
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
    const tangramMessage = ref<string | null>(null)
    const submissionText = ref<string>('')
    return {
      iframe,
      setData,
      getData,
      tangramData,
      submissionText,
      aiMessage,
      tangramMessage
    }
  },
  methods: {
    /**
     * This method is used by the game to submit the data to the task
     */
    async fetchData() {
      console.log('Submitting data')
      const temp = this.iframe?.contentWindow as any 
      console.log(temp.setData)
      if (this.getData == null) {
        console.error('Get data has not been set properly')
        return
      } else {
        this.getData()
      }
    },
    async submitData() {
      if (this.tangramMessage == null) {
        console.error('No data to submit')
        return
      } else {
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
          tangramData: JSON.parse(this.tangramMessage)
        }
        submissionData.submission = submission
        console.log('Emitting data')
        this.$emit('submit', submissionData)
        this.tangramMessage = null
      }
    },
    /**
     * This method is used by the game to obtain the initial positions of the
     * tangram pieces
     */
    getTestData(): TangramGame {
      return {
        // replace by actual data.
        st_1: {
          id: 'st_1',
          points: [
            { x: 1, y: 0 },
            { x: 1, y: 0 },
            { x: 1, y: 0 }
          ]
        }
      }
    },
    updateDataCallback(dataCallBack: Function) {
      // Implement your logic here
      console.log('Registering update data callback')
      this.getData = dataCallBack
    },

    registerSetDataCallback(cf: Function) {
      // Implement your logic here
      console.log('Registering set data callback')
      this.setData = cf
    },
    taskLoaded() {
      // Implement your logic here
      if (this.setData != null) {
        if (this.inputData?.data) {
          this.setData(this.inputData?.data.tangram as TangramGame)
        }
      }
    },
    setTangramData(data: any) {
      console.log(data)
      this.tangramMessage = data
      this.submitData()
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
      console.log("Frame loaded")
      if (this.iframe){
      const iframeContentNew = this.iframe.contentWindow as any      
      iframeContentNew.registerSetDataCallback = this.registerSetDataCallback.bind(this)
      iframeContentNew.registerUpdateDataCallback = this.updateDataCallback.bind(this)
      iframeContentNew.setData = this.setTangramData.bind(this)
      iframeContentNew.taskLoaded = this.taskLoaded.bind(this)
      iframeContentNew.dataUpdated = this.buildHistory.bind(this)
      console.log("Functions registered")
    }
    console.log("frame loading done")
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
      console.log('Got new data! Trying to submit')
      console.log(newValue)
      const displayData = {} as DisplayMessage
      displayData.containsImage = true
      displayData.message = newValue.data.message
      displayData.role = 'AI'
      displayData.handled = false
      this.aiMessage = displayData
      if (this.setData != null) {
        this.setData(newValue.data.tangram)
        // this will trigger an update call, which will submit the data to histroy
      }
    }
  },
  mounted() {
    if (this.iframe) {
      console.log("There is an iframe")
      const iframeContent = this.iframe.contentWindow as any
      if (iframeContent) {
        console.log("There is some content in the iframe")
        iframeContent.registerSetDataCallback = this.registerSetDataCallback.bind(this)
        iframeContent.registerUpdateDataCallback = this.updateDataCallback.bind(this)
        iframeContent.setData = this.setTangramData.bind(this)
        iframeContent.taskLoaded = this.taskLoaded.bind(this)
        iframeContent.dataUpdated = this.buildHistory.bind(this)
        console.log("Data on iframe set")
      }
      console.log(iframeContent.taskLoaded)
      this.iframe.src = '/godot_games/tangram/tangram.html'
      const iframeContentNew = this.iframe.contentWindow as any      
      iframeContentNew.registerSetDataCallback = this.registerSetDataCallback.bind(this)
      iframeContentNew.registerUpdateDataCallback = this.updateDataCallback.bind(this)
      iframeContentNew.setData = this.setTangramData.bind(this)
      iframeContentNew.taskLoaded = this.taskLoaded.bind(this)
      iframeContentNew.dataUpdated = this.buildHistory.bind(this)
      console.log(iframeContentNew)
      console.log(iframeContent)
      nextTick()
      console.log(iframeContent.taskLoaded)

    }
  }
}
</script>
