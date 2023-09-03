<template>
    <div>
        <h4>{{ total_monthly_spendings }}</h4>
        <p>Total Monthly Spendings</p>
    </div>
</template>

<script>
export default {
    name: "MonthTotal",

    props: {
        total_monthly_spendings: Number,
    }
}
</script>

<style>

</style>