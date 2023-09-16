
<template>
    <div class="row">

      <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
      <v-form @submit.prevent="addExpense" v-model="valid">

        <!-- 
            "@click:clear" : This becasue the clear symbol of the v-text-field doesn't clear the input of user, so i had to manually clear it by @click event 
            I couldn't set "label:'Date'", and I had to use v-binf on it :label="formattedDate", because if I used the latter method "label" will block ':value="formattedDate"' from appearing in the input field !
        -->
        <v-text-field class="date-input"  :value="formattedDate" clearable prepend-icon="mdi-calendar" placeholder="For example : 2023-02-07" @click:clear="selectedDate = null" @keydown.delete="handleDelete" :label="formattedDate"> 

          <!-- 
            I have used v-model="menu" and :close-on-content-click="false" in order to prevent the datePicker from disappearing after I click on a date, as this is the default behavior of 'v-menu' nested elements. However, this default behavior is interfering with the functionality of the datepicker.
           -->
          <v-menu activator="parent" v-model="menu" :close-on-content-click="false" height="550" class="veutify-menu">

            <!--@click:save="menu = false" @click:cancel="menu = false" : Are used to a make v-menu closes only when I press 'OK' or 'CANCEL'   -->
            <v-date-picker v-model="selectedDate" @click:save="menu = false" @click:cancel="menu = false"></v-date-picker>

          </v-menu>

        </v-text-field>

        <div class="col">
            <v-text-field v-model="amountSpent" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
            autofocus label="Amount Spended" required prepend-icon="mdi-calendar">
            </v-text-field>
            
          </div>
          <div class="col">
            <v-select v-model="selectedCategory" name="category" id="category" label="Category" prepend-icon="mdi-calendar" :items="categories">
              <!-- <option v-for="(category, index) in categories" :value="category" :key="index">{{ category }}</option> -->
            </v-select>
          </div>

          <div class="col">
            <v-text-field v-model="expenseNote" name="expense-note" id="expense-note" placeholder="Type a note"
            label="Note" required prepend-icon="mdi-calendar">
            </v-text-field>
          </div>

          <div class="col">
            <v-btn class="" type="submit" id="button">Add</v-btn>
          </div>
          
    </v-form>
    <div class="col">
            <label for="day">Month</label>
            <select v-model="selectedMonth" name="month" id="month" @change="fetchDaysForSelectedMonth">
                <!-- We have to JSON.parse(calenderDays) because we have JSON.strigify() it in HOME.vue-->
                <option v-for="(month, index) in months" :value="month" :key="index">{{ month }}</option>
            </select>
        </div>
        <div class="col">
            <!-- <h1>{{ calenderDays }}</h1> -->
            <label for="day">Day</label>
            <select v-model="selectedDay" name="day" id="day">
                <!-- We have to JSON.parse(calenderDays) because we have JSON.strigify() it in HOME.vue-->
                <option v-for="day in days" :value="day.day_num" :key="day.day_num">{{ day.day_name }}, {{ day.day_num }}</option>
            </select>
        </div>

  </div>

</template>

<script>
import axios from 'axios'

// Some important notes about that JS file found inside !
import './../../public/passive-event-notoriousBug.js';

// import { FunctionalCalendar } from 'vue-functional-calendar';
import { VDatePicker } from 'vuetify/labs/VDatePicker'
import { format } from 'date-fns';

export default {
    name: 'AddExpense',
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
            valid: false,
            expenseNote: '',
            selectedDate: null,
            menu: false,
        }
    },
  //   data: () => ({
  //   selectedDate: null,
  //   menu: false,
  // }),
    components: {
      VDatePicker,
    },
    methods: {

        async  fetchYearsAndMonths () {
            try {
                    const path = 'http://127.0.0.1:8083/get_calendar'

                    const response = await axios.get(path);

                    this.months = response.data.current_year_months
                    this.selectedMonth = response.data.current_month
                    this.days = response.data.days
                    this.selectedDay = response.data.current_day
                    this.categories = response.data.categories

                }   catch (error) {
                    console.error('Error fetching data:', error);
                }
            },

        fetchDaysForSelectedMonth () {
            const path = 'http://127.0.0.1:8083/get_calendar';

            axios
                .post(path, {
                    selectedMonth: this.selectedMonth,
                })
                .then((response) => {
                    // Handle success response
                    this.days = response.data.days;
                    // this.selectedDay = response.data.days[0]
                })
                .catch((error) => {
                    if (error.response) {
                        // The request was made, and the server responded with a non-2xx status code
                        // Handle the error based on the HTTP status code and error message
                        const status = error.response.status;
                        const message = error.response.data.error_message;
                        alert(`Error! Status: ${status}, Message: ${message}`);
                    } else if (error.request) {
                        // The request was made, but no response was received
                        alert('Error! No response received from the server. Please try again or contact support for assistance.');
                    } else {
                        // Something else happened while setting up the request
                        alert(`Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`);
                    }
                });
        },

        addExpense() {
            const path = 'http://127.0.0.1:8083/add_expenses';

            axios
                .post(path, {
                    selectedMonth: this.selectedMonth,
                    selectedDay: this.selectedDay,
                    amountSpent: this.amountSpent,
                    category: this.selectedCategory,
                })
                .then((response) => {
                    // Handle success response
                    const submitedAmountSpent = response.data.submitedAmountSpent;
                    const submitedCategory = response.data.submitedCategory;
                    
                    alert(`Success! ${submitedAmountSpent} has been added to your ${submitedCategory} expenses.`);
                })
                .catch((error) => {
                    if (error.response) {
                        // The request was made, and the server responded with a non-2xx status code
                        // Handle the error based on the HTTP status code and error message
                        const status = error.response.status;
                        const message = error.response.data.error_message;
                        alert(`Error! Status: ${status}, Message: ${message}`);
                    } else if (error.request) {
                        // The request was made, but no response was received
                        alert('Error! No response received from the server. Please try again or contact support for assistance.');
                    } else {
                        // Something else happened while setting up the request
                        alert(`Oops! Something went wrong while adding the expense. Please try again or contact support for assistance.`);
                    }
                });
        },
        handleDelete() {
    this.selectedDate = null;
    
  },
    },
    computed: {
  formattedDate () {
    const formattedDate = this.selectedDate ? format(this.selectedDate, 'EEEE, dd MMM, yyyy') : format(new Date(), 'EEEE, dd MMM, yyyy');
    return formattedDate
  },
  // categories () {
  //   return this.categories
  // }
},
    created() {
        this.fetchYearsAndMonths()
    },
}
</script>

<style>

.date-input {
  /* max-height: 10px;  */
  /* width: 100%;
  height: 200px;
  background-color: white;
  border: 2px solid; */
}

.veutify-menu{
  /* height: 20px; */
}
</style>