<template>
  <p>{{ dots }}</p>
</template>

<script lang="ts">
// Simple loading dots component, that can be reused indicating ChatGPT writing.
export default {
  data() {
    return {
      dots: '.'
    }
  },
  mounted() {
    this.startAnimation()
  },
  methods: {
    startAnimation() {
      setInterval(() => {
        switch (this.dots) {
          case '.':
            this.dots = '..'
            break
          case '..':
            this.dots = '...'
            break
          case '...':
            this.dots = '.'
            break
          default:
            this.dots = '.'
            break
        }
      }, 250)
    }
  }
}
</script>

<style></style>
