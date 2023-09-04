import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import AddExpense from '../views/AddExpense.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    // ':' means that there be a variable be placed after :, and not normal string
    // so this url is have 'GET' values inside it !
    // '?' indicates that 'currentDay' variable is optional and not required, and I put it becasue when i remove it and try to navigate to the previous url/page it outputs an error
    
    // 'calenderDays*' the '*' indicates that 'calenderDays' is a normal variable, but instead it is an iterable (like an array)
    path: '/addExpense/:calenderDays*/:currentDay?',
    name: 'addExpense',
    component: AddExpense,
    // props: ture : this means that the variables 'calenderDays' and 'currentDay' will be passed to "addexpense" component as 'props'
    props: true
  },
  
]

const router = createRouter({
    
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router