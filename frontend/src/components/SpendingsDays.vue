<template>
   <div class="col-6">
        <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
        
        <div :key="dailySpending.spending_id" v-for="dailySpending in monthSpendings">
            <SpendingsDay :dailySpending="dailySpending"/>
        </div>
    </div>
</template>

<script>
import SpendingsDay from './SpendingsDay';

export default {
    name: "SpendingsDays",

    props: {
        monthSpendings: Array,
    },
    components: {
        SpendingsDay
    }
}
</script>

<style>

</style>