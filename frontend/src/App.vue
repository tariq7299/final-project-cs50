<template>
  <div class="parent-container">

      <nav class="navbar sticky-top mb-2" >
        <div class="container-fluid">
            <a class="navbar-brand" href="#">GoldGardyn</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasNavbarLabel">GoldGardyn</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" :href="homeUrl">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :href="addExpensesUrl">Add Expense</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :href="contactsUrl">People</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :href="addTransaction">Add Transactions</a>
                    </li>
                   
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Dropdown
                        </a>
                        <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Action</a></li>
                        <li><a class="dropdown-item" href="#">Another action</a></li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>
                    </ul>
                    <form class="d-flex mt-3" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                    </form>
                </div>
            </div>
            
        </div>
      </nav>

    <router-view></router-view>

  </div>
</template>

<script>

  export default {
    name: 'App',
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
      }
    }
}
</script>

<style>

  /* Logo font 
  font-family: 'Playfair Display', serif; wght@600
  font-weight: 600;

  --> Main font
  font-family: Avenir, Helvetica, Arial, sans-serif;

  --> Titles font
  font-family: 'Roboto Slab', serif;
  font-weight: 300;

  --> Arabic font
  font-family: 'Tajawal', sans-serif;
  font-weight: 300
  */

  /* family=Montserrat&family=Playfair+Display:wght@600&family=Roboto+Slab:wght@300&family=Tajawal&display=swap */
  

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    
  }

  .parent-container {
    margin: auto;
    /* height: 100%; */
  }

  .navbar {
    background-color: var(--secondary);
    border-bottom: 5px solid;
    z-index: 1020;  /* This is the default value of bootstrap nav-bar */
  }

  .offcanvas-header {
    background-color: var(--secondary);

  }
  .offcanvas-body {
    background-color: var(--background);

  }

  /* I have added that class to each section of Home view, so specifing this style here makes sense becasue I want to apply that stying to every section  */
  .sector  {
    margin-bottom: 1rem;
  }

  


</style>