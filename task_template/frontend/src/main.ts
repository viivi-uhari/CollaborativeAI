import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Primevue imports
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'

// PrimeVue theme (will probably need to be overwritten for Aalto Look and Feel)
import 'primevue/resources/themes/lara-light-indigo/theme.css'
// Primevue core css
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'

import App from './App.vue'
import router from './router'
const pinia = createPinia()

const app = createApp(App)

app.use(pinia)
app.use(router)
app.directive('tooltip', Tooltip)
app.use(PrimeVue, { ripple: true })
app.use(ToastService)
app.mount('#app')
