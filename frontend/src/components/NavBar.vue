<template>
  <nav class="navbar sticky-top mb-2" >
    <div class="container-fluid">
        <a class="navbar-brand" :href="homeUrl">GoldGardyn</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="offcanvasNavbarLabel">GoldGardyn</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body" v-if="isAuthentic">
                <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" :href="homeUrl">Expenses</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" :href="contactsUrl">People</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" :href="addExpensesUrl">Add Expense</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" :href="addTransaction">Add Transactions</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" @click="logout" href="#">Logout</a>
                </li>
                </ul>
            </div>
            <div class="offcanvas-body" v-else>
                <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                <li class="nav-item">
                    <a class="nav-link" :href="registerUrl">Register</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" :href="loginUrl">Login</a>
                </li>
                </ul>
                
            </div>
        </div>
        
    </div>
  </nav>
</template>

<script>
import axios from 'axios'
import { isAuthenticated } from './../auth';

    export default {
    name: 'NavBar',
    data() {
      return{
        isAuthentic: false
      }
    },
    computed: {
      homeUrl() {
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        const path =  frontendUrl + '/';
        return path
      },
      addExpensesUrl(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/addExpenses';
      },
      contactsUrl(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/contacts';
      },
      addTransaction(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/AddTransactions';
      },
      registerUrl(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/register';
      },
      loginUrl(){
        const frontendUrl = process.env.FORNTEND_BASE_URL;
        return frontendUrl + '/login';
      },
    },
    methods: {
      
      async logout(){
        try {
                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/logout';

                const response = await axios.get(path, { withCredentials: true });
                
                // 
                if (response.data.success) {

                  this.$router.push({ name: 'login' })
                  alert("You Have Successfully Logged Out")
                  return
                }

            }   catch (error) {
                console.error(error);
                alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
            }
        },

    },
    async created() {
      console.log("isAthuth", isAuthenticated())
      return this.isAuthentic = await isAuthenticated()

    }
}
</script>

<style>

</style>