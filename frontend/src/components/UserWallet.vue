<template>
  <div class="">
    <p class="money-header">{{ amount }}</p>
    <p class="secondary-header2">{{ walletTitle }}</p>
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

<style scoped>

  p {
    margin: 0;
    padding: 0.25rem;
  }

</style>