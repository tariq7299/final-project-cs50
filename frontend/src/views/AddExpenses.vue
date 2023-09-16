
<template>
    <div class="row">
      <v-text-field color="success" :value="formattedDate" clearable prepend-icon="mdi-calendar" placeholder="For example : 2023-02-07" @click:clear="selectedDate = null" @keydown.delete="handleDelete" class="my-text-field">
        <v-menu activator="parent" v-model="menu" :close-on-content-click="false" height="550">
          <v-date-picker v-model="selectedDate" @click:save="menu = false" @click:cancel="menu = false"></v-date-picker>
        </v-menu>
      </v-text-field>
    <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
    <form @submit.prevent="addExpense">
        <div class="col">
            <!-- <h1>{{ calenderDays }}</h1> -->
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
        <div class="col">
            <label for="amount-spent">Amount</label>
            <input v-model="amountSpent" name="amount-spent" id="amount_spent" placeholder="Enter Amount"
            autofocus>
        </div>
        <div class="col">
            <label for="category">Category</label>
            <select v-model="selectedCategory" name="category" id="category">
                <option v-for="(category, index) in categories" :value="category" :key="index">{{ category }}</option>
            </select>
        </div>
        <div class="col">
            <button class="btn btn-dark" type="submit" id="button">Add</button>
        </div>
    </form>
  </div>

</template>

<script>
import axios from 'axios'
// import { FunctionalCalendar } from 'vue-functional-calendar';
import { VDatePicker } from 'vuetify/labs/VDatePicker'
import format from 'date-fns/format'

export default {
    name: 'AddExpense',
    data () {
        return {
            months: '',
            days: '',
            selectedMonth: '',
            selectedDay: '',
            amountSpent:'',
            categories: '',
            selectedCategory: '',
            calendarData: {},
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
    const formattedDate0 = this.selectedDate ? format(this.selectedDate , 'MMM EEEE, yyyy') : '' 
    return formattedDate0
  }
},
    created() {
        this.fetchYearsAndMonths()
    },

}
</script>

<style>

</style>