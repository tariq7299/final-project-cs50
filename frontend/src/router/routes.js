import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import AddExpenses from '../views/AddExpenses.vue'
import Contacts from '../views/Contacts.vue'
import AddTransactions from '../views/AddTransactions.vue'
import ContactHistory from '../views/ContactHistory.vue'
import AddNewContact from '../views/AddNewContact.vue'
import Register from '../views/Register.vue'

const routes = [
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  // {
  //   path: '/login',
  //   name: 'login',
  //   component: Login,
  // },
  // {
  //   path: '/logout',
  //   name: 'logout',
  //   component: Logout,
  // },
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

    path: '/addExpenses',
    name: 'addExpenses',
    component: AddExpenses,
    // props: ture : this means that the variables 'calenderDays' and 'currentDay' will be passed to "addexpense" component as 'props'
    // props: true
  },
{
  path: '/contacts',
  name: 'contacts',
  component: Contacts
  },
  {
  path: '/add-new-contact',
  name: 'addNewContact',
  component: AddNewContact
  },
  {
  path: '/AddTransactions',
  name: 'transactions',
  component: AddTransactions
  },
  {
  path: '/contact-history/:contactName/:contactPhone/:contactNetBalance',
  name: 'contactHistory',
  component: ContactHistory,
  props: true
  },
]

const router = createRouter({
    
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router