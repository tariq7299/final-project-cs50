<template>
    <div v-if="loading" class="row loading-indicator">
       <div class="col-12">
           <h3>Loading...</h3>        
       </div>
    </div>
    <div class="row" v-else>

        <div class="col-5 text-start">
            <h4>{{ selectedYear }}</h4>
        </div>
        <div class="col-5 text-start">
            <h4>{{ selectedMonth }}</h4>
        </div>
        <div class="col-2">

            <Button @btnClicked="toggelChooseTimeFrame"></Button>
        </div>

        <div class="col-6">
            <ChooseTimeFrame @userChoseMonthTimeFrame="extractYearAndMonth" v-show="showChooseTimeFrame"> </ChooseTimeFrame>
        </div>

        
    </div>
</template>

<script>
import axios from 'axios'
import Button from '@/components/Button.vue';
import ChooseTimeFrame from '@/components/ChooseTimeFrame.vue';

   export default {
       name: "MonthTimeFrame",
       components: {
        Button,
        ChooseTimeFrame,
       },
       data () {
           return {
               selectedYear:'',
               selectedMonth: '',
               showChooseTimeFrame: false,
               loading: false, // Add a loading indicator state
           }
       },
       methods: {
        extractYearAndMonth (monthlyExpenses) {
            this.selectedYear =  monthlyExpenses.selectedYear;
            this.selectedMonth = monthlyExpenses.selectedMonth;
            this.loading = false

            this.$emit('userChoseMonthTimeFrame', monthlyExpenses)
        },
           toggelChooseTimeFrame () {
                this.showChooseTimeFrame = !this.showChooseTimeFrame
            }
       },
       mounted() {
       }
   }
</script>

<style>

</style>