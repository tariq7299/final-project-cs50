<template>
  <div class="">
    <p >{{ walletTitle }}</p>
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

<style scoped>
p {
  margin: 0;
}
</style>