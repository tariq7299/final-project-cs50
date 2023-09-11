<template>
    <div class="row">
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

<style scoped>

    h4 {
        font-size: large;
    }

    p {
        font-style: italic;
    }
    
    .row {
        position: relative;
        top: 5rem;
        padding-top: 1rem;
        background: var(--background);
    }
</style>
