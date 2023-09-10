<template>
    <div class="time-frame">
        <div v-if="loading" class="row loading-indicator">
           <div class="col-12">
               <h3>Loading...</h3>        
           </div>
        </div>
        <div class="" v-else>
            <div class="row">
    
                <div class="col text-start">
                    <h4><span></span>{{ selectedYear }} - {{ selectedMonth }}</h4>
                </div>
                <div class="col text-end">
                    <Button @btnClicked="toggelChooseTimeFrame"></Button>
                </div>
            </div>
            <div class="row">
                <div class="col-6">
                    <ChooseTimeFrame @userChoseMonthTimeFrame="extractYearAndMonth" v-show="showChooseTimeFrame"> </ChooseTimeFrame>
                </div>
            </div>
                
        </div>
    </div>
</template>

<script>
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
    .time-frame {
        /* padding: 2rem 0; */
        margin: 2rem 0;
    }

</style>