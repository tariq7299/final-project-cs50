<template>
<div class="container text-center">
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <router-view></router-view>
</div>
</template>

<script>

  export default {
    name: 'App',
    components: {
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
    color: #2c3e50;
  }

</style>
