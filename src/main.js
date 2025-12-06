import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// Global mode styles (dark / colorblind)
import './styles/modes.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
