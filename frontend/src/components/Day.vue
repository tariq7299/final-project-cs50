<template>
    <div class="center">
        <ul>
            <!-- <li v-for="" >{{ dayDate }}{{  }}</li> -->
            <li>{{ dayDate }} - Total Amount: {{ totalAmount }}</li>
        </ul>
        <div class="center" v-for="expense in expenses" :key="expense.spending_id">
            <p>Amount: {{ expense.amount_spent }} - Category: {{ expense.category }}</p>
        </div>
    </div>
  </template>

<script>
    export default {
        name: 'Day',
        props: {
            dayDate: String,
            expenses: Array,
            totalAmount: Number
        }
    }
</script>

<style scoped>
    .center {
        margin: auto;
    }
</style>

