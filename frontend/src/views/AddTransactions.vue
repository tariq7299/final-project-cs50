<template>
    <div class="add-transactions">

        <Header class="sector" pageTitle="Add Transactions"></Header>

        <v-form @submit.prevent="addExpense" v-model="valid" class="formTest">
    
        <!-- 
            "@click:clear" : This becasue the clear symbol of the v-text-field doesn't clear the input of user, so i had to manually clear it by @click event 
            I couldn't set "label:'Date'", and I had to use v-binf on it :label="formattedDate", because if I used the latter method "label" will block ':value="formattedDate"' from appearing in the input field !
        -->
        <v-text-field class="expense-input"  :value="formattedDate" clearable prepend-icon="mdi-calendar" placeholder="For example : 2023-02-07" @click:clear="selectedDate = null" @keydown.delete="handleDelete" :label="formattedDate"> 

            <!-- 
            I have used v-model="menu" and :close-on-content-click="false" in order to prevent the datePicker from disappearing after I click on a date, as this is the default behavior of 'v-menu' nested elements. However, this default behavior is interfering with the functionality of the datepicker.
            -->
            <v-menu activator="parent" v-model="menu" :close-on-content-click="false" height="550" class="veutify-menu">

            <!--@click:save="menu = false" @click:cancel="menu = false" : Are used to a make v-menu closes only when I press 'OK' or 'CANCEL'   -->
            <v-date-picker v-model="selectedDate" @click:save="menu = false" @click:cancel="menu = false"></v-date-picker>

            </v-menu>

        </v-text-field >

            <v-text-field v-model="amountSpent" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
            autofocus label="Deal Amount" required prepend-icon="mdi-cash" class="expense-input">
            </v-text-field>
            
            <v-select v-model="selectedCategory" name="category" id="category" label="Category" prepend-icon="mdi-notification-clear-all" :items="categories" class="expense-input" required>
                <!-- <option v-for="(category, index) in categories" :value="category" :key="index">{{ category }}</option> -->
            </v-select>

            <v-text-field v-model="expenseNote" name="expense-note" id="expense-note" placeholder="Type a note"
            label="Note" required prepend-icon="mdi-note" class="expense-input">
            </v-text-field>

            <v-btn class="" type="submit" id="button">Add Expense</v-btn>
            
        </v-form>
    </div>
</template>

<script>
    import Header from './../components/Header'
    import axios from 'axios'

    // Some important notes about that JS file found inside !
    import './../../public/passive-event-notoriousBug.js';

    // import { FunctionalCalendar } from 'vue-functional-calendar';
    import { VDatePicker } from 'vuetify/labs/VDatePicker'
    import { format } from 'date-fns';

    export default {
        name: 'AddTransactions',
        components: {
            Header,
    },
    data () {
          return {
              months: '',
              days: '',
              selectedMonth: '',
              selectedDay: '',
              amountSpent:'',
              categories: [],
              selectedCategory: '',
              calendarData: {},
              expenseNote: '',
              selectedDate: null,
              menu: false,
          }
      },

}
</script>

<style>

</style>