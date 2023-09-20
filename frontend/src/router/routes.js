import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import AddExpenses from '../views/AddExpenses.vue'
import Contacts from '../views/Contacts.vue'
import AddTransactions from '../views/AddTransactions.vue'
import ContactHistory from '../views/ContactHistory.vue'
import AddNewContact from '../views/AddNewContact.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'


const routes = [
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    // ':' means that there be a variable be placed after :, and not normal string
    // so this url is have 'GET' values inside it !
    // '?' indicates that 'currentDay' variable is optional and not required, and I put it becasue when i remove it and try to navigate to the previous url/page it outputs an error
    // 'calenderDays*' the '*' indicates that 'calenderDays' is a normal variable, but instead it is an iterable (like an array)

    path: '/addExpenses',
    name: 'addExpenses',
    component: AddExpenses,
    meta: { requiresAuth: true }
    // props: true
  },
  {
    path: '/contacts',
    name: 'contacts',
    component: Contacts,
    meta: { requiresAuth: true }
  },
  {
    path: '/add-new-contact',
  name: 'addNewContact',
  component: AddNewContact,
  meta: { requiresAuth: true }
},
{
  path: '/AddTransactions',
  name: 'transactions',
  component: AddTransactions,
  meta: { requiresAuth: true }
},
{
  path: '/contact-history/:contactName/:contactPhone/:contactNetBalance',
  name: 'contactHistory',
  component: ContactHistory,
  props: true,
  meta: { requiresAuth: true }
  // props: ture ' : ' this means that the variables 'contactName' and 'currentDay' and contactNetBalance will be passed to "ContactHistory" component as 'props'
  },
]



const router = createRouter({
    
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

import { isAuthenticated } from './../auth.js' 

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (await isAuthenticated()) {
      next()
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router