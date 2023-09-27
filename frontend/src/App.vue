<template>
  <div class="parent-container">

    <router-view></router-view>

  </div>
</template>

<script>

  export default {
    name: 'App',
   
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
  /* 
  MEDIA QUERIES

    Phones in protrait : @media (max-width: 450px) and (orientation: portrait)

    Phones in landscape and Tablets in portrait: @media (max-width: 1023px) and (orientation: landscape) 

    Tablets in landscape: @media screen and (min-width: 1023px) and (max-width: 1200px)

    Computers: @media screen and (min-width: 1200px)


  
  */

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    
  }

  .parent-container {
    margin: auto;
    height: 100%;
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