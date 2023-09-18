<template>
  <div class="">
    <p class="money-header" :style="colorNetBalance">{{ amount }}</p>
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
        },
        computed: {
          colorNetBalance () {
            return this.amount.includes('-') ? {'color': 'RED'} : {'color': 'GREEN'}
          }
        }
    }
</script>

<style scoped>

  p {
    margin: 0;
    padding: 0.1rem;
  }

</style>