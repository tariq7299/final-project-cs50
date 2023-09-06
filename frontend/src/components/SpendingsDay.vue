<template>
    <div class="center">
        <ul>
            <!-- <li v-for="" >{{ date }}{{  }}</li> -->
            <li>{{ date }} - Total Amount: {{ totalAmount }}</li>
        </ul>
        <div class="center" v-for="spending in spendings" :key="spending.spending_id">
            <p>Amount: {{ spending.amount_spent }} - Category: {{ spending.category }}</p>
        </div>
    </div>
  </template>

<script>
    export default {
        name: 'SpendingsDay',
        props: {
            date: String,
            spendings: Array,
            totalAmount: Number
        }
    }
</script>

<style scoped>
    .center {
        margin: auto;
    }
</style>

