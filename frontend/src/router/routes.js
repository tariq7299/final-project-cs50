import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import AddExpenses from '../views/AddExpenses.vue'
import AddNewCategory from '../views/Login.vue'
import Contacts from '../views/Contacts.vue'
import AddTransactions from '../views/AddTransactions.vue'
import ContactHistory from '../views/ContactHistory.vue'
import AddNewContact from '../views/AddNewContact.vue'
import AddCategory from '../views/AddCategory.vue'
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
    path: '/login/:status?/:message?',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/addExpenses',
    name: 'addExpenses',
    component: AddExpenses,
    meta: { requiresAuth: true }
  },
  {
    path: '/add-category',
    name: 'addCategory',
    component: AddCategory,
    meta: { requiresAuth: true }
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
  // ':' means that there be a variable be placed after :, and not normal string
    // so this url is have 'GET' values inside it !
    // '?' indicates that 'currentDay' variable is optional and not required, and I put it becasue when i remove it and try to navigate to the previous url/page it outputs an error
    // 'exampleUrlParam*' the '*' indicates that 'exampleUrlParam' is a normal variable, but instead it is an iterable (like an array)
  path: '/contact-history/:contactName/:contactPhone/:contactNetBalance',
  name: 'contactHistory',
  component: ContactHistory,
  props: true,
  // meta: { requiresAuth: true }
  // props: ture ' : ' this means that the variables 'contactName' and 'currentDay' and contactNetBalance will be passed to "ContactHistory" component as 'props'
  },
]



const router = createRouter({
    
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

import { isAuthenticated } from './../auth.js' 


// This is mplemented from vue js document, and it is a better way than the one down below
// 'to' : THis represents the destination route
// 'from' : THis represents the source route
router.beforeEach(async (to, from) => {
  if (
    // make sure the user is authenticated
    !(await isAuthenticated()) &&
    // ❗️ Avoid an infinite redirect
    (to.name !== 'login') &&

    (to.meta.requiresAuth)
  ) {
    // redirect the user to the login page
    return { name: 'login' }
  } 
})

// This is an older method to the same as above, where next() where used
// router.beforeEach(async (to, from, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     if (await isAuthenticated()) {
//       next()
//     } else {
//       next('/login')
//     }
//   } else {
//     next()
//   }
// })

export default router