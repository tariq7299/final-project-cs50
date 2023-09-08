<template>
    <div>
        <h4>{{ totalMonthlyExpenses }}</h4>
        <p>Total Monthly Spendings</p>
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

<style>

</style>
