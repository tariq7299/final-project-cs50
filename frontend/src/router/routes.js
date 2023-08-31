import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import ChooseMonth from '../views/ChooseMonth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/chooseMonth',
    name: 'ChooseMonth',
    component: ChooseMonth,
  },
]

const router = createRouter({
    
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router