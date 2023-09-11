<template>
    <div class="sector total-expenses-container">
        <p class="money-header">{{ totalMonthlyExpenses }}</p>
        <p class="secondary-header2">Total Monthly Spendings</p>
    </div>
</template>

<script>
export default {
    name: "MonthTotal",

    props: {
        totalMonthlyExpenses: String,
    }
}
</script>

<style scoped>
.total-expenses-container {
    border-top: 1px solid;
    border-bottom: 1px solid;
}
p {
   
    margin: 0;
}


</style>
