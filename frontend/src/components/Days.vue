<template>
    <div class="row">
        
         <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
         <div v-show="homePage">
            <Day v-for="(expensesObj, date) in groupedByDay" :key="date" :dayDate="date" :expenses="expensesObj.expenses" :totalAmount="expensesObj.totalAmount"/>
         </div>

         <div v-show="contactHistoryPage">
            <Day v-for="(dailyTransactionsObj, date) in groupedByDay" :key="date" :dayDate="date" :dailyTransactions="dailyTransactionsObj.dailyTransactions" :totalAmount="dailyTransactionsObj.totalAmount"/>
         </div>

         <div></div>

     </div>
 </template>
 
 <script>
 import Day from './Day';
 
 export default {
     name: "Days",
 
     props: {
         groupedByDay: Object,
     },
     components: {
         Day
     },
     computed: {
            homePage () {
                if(this.$route.path === '/') {
                    return true
                } else {
                    return false
                }
            },
            contactHistoryPage () {
                // return this.$route.path.startsWith('/contact-history/');
                // OR
                return this.$route.name === 'contactHistory';
            }
        },

 }
 </script>
 
 <style>
 
 </style>
  