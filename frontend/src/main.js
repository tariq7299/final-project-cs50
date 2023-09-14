import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router/routes.js'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
// import FunctionalCalendar from 'vue-functional-calendar';
// Vue.use(FunctionalCalendar, {
//     dayNames: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
// });
createApp(App)
    .use(router)
    .mount('#app')

    
