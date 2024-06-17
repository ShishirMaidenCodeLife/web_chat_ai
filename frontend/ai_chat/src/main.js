import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
 
createApp(App).mount('#app')

axios.interceptors.request.use((config) => {
    config.baseURL = 'http://localhost:8000'
    // config.headers['leel'] = 'ram'
    config.url = config.url.replace('https://', 'http://')
    return config
})
