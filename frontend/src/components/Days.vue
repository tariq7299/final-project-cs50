<template>
    <div class="row">
         <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
         
         <Day v-for="(expensesObj, date) in groupedExpensesByDay" :key="date" :dayDate="date" :expenses="expensesObj.expenses" :totalAmount="expensesObj.totalAmount"/>
         
     </div>
 </template>
 
 <script>
 import Day from './Day';
 
 export default {
     name: "Days",
 
     props: {
         groupedExpensesByDay: Object,
     },
     components: {
         Day
     }
 }
 </script>
 
 <style>
 
 </style>
 
