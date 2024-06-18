<template>
  <div class="flex w-full pt-2 pb-2 pr-2 align-items-center" v-if="message.role === 'user'">
    <Avatar :isGPT="false" :ID="userName"></Avatar>
    <div class="flex textcontainer align-items-start input">      
      <img v-if="message.containsImage" class="mr-4" width="1000" :src="message.imageURL" />
      {{ currentContent }}      
    </div>
  </div>
  <div
    v-else-if="message.role != 'system'"
    ref="messageContent"
    class="flex gptmessage w-full pt-2 pb-2 pr-2 flex-column"
  >
    <div class="flex gptmessage w-full">
      <Avatar :isGPT="true" :ID="modelName" />
      <div class="flex textcontainer align-items-center">
        <div class="flex flex-column w-full align-items-start">
          <div class="flex w-full flex-column">
            <div class="flex w-full justify-content-end align-items-start">              
              <img class="mr-4" v-if="message.containsImage" width="1000" :src="message.imageURL" />              
              <span>
                {{ currentContent }}
              </span>
            
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
  <span class="flex flex-column overflow-x-hidden" v-if="isLoading">
    <LoadingDots />
  </span>
</template>

<script lang="ts">
// Local Components
import LoadingDots from './LoadingDots.vue'
import Avatar from './Avatar.vue'

// Types
import type { DisplayMessage } from '@/stores/types'
import type { PropType } from 'vue'

// PrimeVue components
import Button from 'primevue/button'

export default {
  components: { Avatar, Button, LoadingDots },
  props: {
    message: {
      type: Object as PropType<DisplayMessage>,
      required: true
    },
    userName: {
      type: String,
      default: 'You'
    },
    modelName: {
      type: String,
      default: 'AI'
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {}
  },
  computed: {
    currentContent() {
      // either the amount up to this point OR the full Content
      return this.message.message
    }
  },
  methods: {},
  watch: {},
  updated() {}
}
</script>

<style>
/*.interaction {
  border-width: 1px;
  border-right: 2px;
  border-radius: 5px;
  border-style: solid;
}*/

.user {
  border-color: black;
  background-color: black;
  color: white;
}

.gpt {
  border-color: var(--aalto-color);
  background-color: var(--aalto-color);
  color: black;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.avatarcontainer {
  min-width: 80px;
  padding: 10px;
}
.textcontainer {
  width: calc(100% - 100px);
}

.messagecontent {
  margin: 4px;
}

p {
  align-items: left;
}

pre {
  background-color: black;
}

code {
  background-color: black;
  color: white;
  background: black;
}
.gptmessage {
  background-color: #eeeeee;
}
.input {
  margin-top: 16px;
  margin-bottom: 16px;
  white-space: pre-line;
}
.reactionButton {
  max-width: 1.5rem;
  max-height: 1.5rem;
}
.copyButtons {
  right: 0px;
  top: 0px;
}
</style>
