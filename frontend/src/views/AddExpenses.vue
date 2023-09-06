
<template>

  <div class="row">
    <!-- .prevent modifier is used to prevent the default behavior of the form submission, which is to reload the page. -->
    <form @submit.prevent="addExpense">
        <div class="col">
            <!-- <h1>{{ calenderDays }}</h1> -->
            <label for="day">Month</label>
            <select v-model="selectedMonth" name="month" id="month" @change="clearSlectedDay">
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
            selectedCategory: ''
        }
    },
    methods: {
        async  fetchYearsAndMonths () {
            try {
                    const path = 'http://127.0.0.1:8083/addExpenses'

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
            addExpense() {
            const path = 'http://127.0.0.1:8083/addExpenses';

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

        clearSlectedDay () {
            this.selectedDay = ''
        }
            
    },
    created() {
        this.fetchYearsAndMonths()
    }
}
</script>

<style>

</style>