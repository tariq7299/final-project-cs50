<template>
    <div class="sector time-frame">
        <div v-if="loading" class="row loading-indicator">
           <div class="col-12">
               <h3>Loading...</h3>        
           </div>
        </div>
        <div class="" v-else>
            <div class="row">
                <div class="col text-start">
                    <p><span class="secondary-header">{{ selectedYear }} - {{ selectedMonth }}</span></p>
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
       emits: ['userChoseMonthTimeFrame'],
   }
</script>

<style scoped>
    .time-frame {
        padding-top: 1rem;
        border-top: 1px solid;
    }
    
</style>