<template>
    <div>
        <p>{{ dailySpending.date }}</p>
        <p>{{ dailySpending.item_type }}</p>
        <p>{{ dailySpending.amount_spent }}</p>
    </div>
</template>

<script>
    export default {
        name: 'SpendingsDay',
        props: {
            dailySpending: Object,
        }

    }
</script>

<style>

</style>

