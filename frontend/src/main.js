import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import './registerServiceWorker'
import router from './router/routes.js'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import NavBar from "./components/NavBar.vue"

loadFonts()


const app = createApp(App)

app.use(vuetify)
app.use(router)
app.component('NavBar', NavBar)
app.mount('#app')

