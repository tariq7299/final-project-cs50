import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router/routes.js'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

createApp(App)
    .use(router)
    .mount('#app')

    
