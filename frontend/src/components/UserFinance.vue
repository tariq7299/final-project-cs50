<template>
  <div>
    <h4>{{ amountTitle }}</h4>
    <p>{{ amount }}</p>
  </div>
</template>

<script>
    export default {
        name: "UserFinance",
        props: {
            amountTitle: String,
            amount: {
                type: Number,
                default: 0
            }
            
        }
    }
</script>

<style>

</style>