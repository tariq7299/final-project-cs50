<template>
  <div class="">
    <h4>{{ walletTitle }}</h4>
    <p>{{ amount }}</p>
  </div>
</template>

<script>
    export default {
        name: "UserWallet",
        props: {
          walletTitle: String,
            amount: {
                type: String,
                default: "0"
            }
            
        }
    }
</script>

<style>

</style>