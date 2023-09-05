<template>
   <div class="col-6">
        <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
        
        <SpendingsDay v-for="(spendingsObj, date) in groupedSpendings" :key="date" :date="date" :spendings="spendingsObj.spendings" :totalAmount="spendingsObj.totalAmount"/>
        
    </div>
</template>

<script>
import SpendingsDay from './SpendingsDay';

export default {
    name: "SpendingsDays",

    props: {
        groupedSpendings: Object,
    },
    components: {
        SpendingsDay
    }
}
</script>

<style>

</style>