<template>
    <div v-if="loading" class="row loading-indicator">
       <div class="col-12">
           <h3>Loading...</h3>        
       </div>
    </div>
    <div class="row" v-else>
        <div class="col-6">
            <!-- When user loads the page the app will GET the spendings years from the server and populate <select> of the years with it, and inside the fetchYearsAndEmitTimeFrame() function, there is actully a call to fetchMonthsAndEmitTimeFrame() function, that will also populate <select> of months -->
            <!-- Wheu user choose a year (@change=fetchMonthsAndEmitTimeFrame), app will GET spendings months from server, and populate <select> input of the months with it -->
            <!--Also whether the user loads the page, or he chooses a certain year and month manually, in both cases the app will 'emit' the timeFrame (selectedYear & selectedMonth) to parent component (Home.vue)   -->
            <select v-model="selectedYear" @change="fetchAndEmitRecentMonthExpenses">
                <!-- You can this disabled option if you want -->
                <!-- <option disabled value="">Select year</option> -->
                
                <!--  We wrote v-bind:value because it takes its value from data() down there-->
                <!--  'v-bind:key=index' is necessary for the loop to work, it should have like a index/id...etc for each 'year' value found in the list 'years'-->
                <option v-for="(year, index) in years" :value="year" :key="index">{{ year }}</option>
            </select>
        </div>
        <div class="col-6">
            <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
            <select v-model="selectedMonth" @change="fetchAndEmitSelectedMonthlExpenses">
                <!-- <option disabled value="">Select month</option> -->
                <option v-for="(month, index) in months" :value="month" :key="index">{{ month }}</option>
            </select>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

   export default {
       name: "MonthTimeFrame",
       data () {
           return {
               monthlyExpenses: [],
               total_monthly_expenses: '',
               years: [],
               selectedYear:'',
               months: [],
               selectedMonth: '',
               calenderDays: [],
               loading: true, // Add a loading indicator state
           }
       },
       methods: {

           // USER LOADS THE PAGE
           // This function will : 1- GET years and months from server which belongs to the current user, 2- Choose/Select most recent year and month to view its espenses 3- Emits "monthlyExpenses" and "totalMonthlyExpenses" out to parent (Home.vue)
           // This gets called only when user reloads the page only !!
           async loadAndEmitRecentMonthExpenses() {
               try {
                   const apiUrl = process.env.VUE_APP_API_BASE_URL;

                   const path = apiUrl + '/load_recent_month_expenses';

                   const response = await axios.get(path);

                   // GET past years which contain expenses
                   this.years = response.data.years;

                   // Choose/select the most recent year, by assinging it to "selectedYear"
                   this.selectedYear = this.years[0];

                   // GET past months in most recent year
                   this.months = response.data.months

                   // Choose/select the most recent month, by assinging it to "selectedMonth"
                   this.selectedMonth = this.months[0]

                   // GET the monthly expenses in the "selectedMonth" (the most recent month)
                   this.monthlyExpenses = response.data.monthly_expenses
                   
                   // GET the total monthly expenses amount which belongs to "selectedMonth" (the most recent month) 
                   this.totalMonthlyExpenses = response.data.total_monthly_expenses

                   // Finaly Emit "monthlyExpenses" and "totalMonthlyExpenses" out to parent component of Home.vue, so it will be used in another sibiling component 
                   this.emitMonthlyExpenses();

                   // After all the above is done, remove the loading indicator
                   this.loading = false;

               }   catch (error) {
                   console.error(error);
                   alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
                   this.loading = false; // Set loading to false in case of an error
               }
           },
           
           // USER HAVE CHOOSEN A YEAR
           // This function will: 1- FETCH months which belongs to the 'selectedYear', 2- Choose/Select most recent month to view its expenses 3- Emits "monthlyExpenses" and "totalMonthlyExpenses" out to parent (Home.vue)
           // This gets called only when user choose a "year" from <select> input of years
           async fetchAndEmitRecentMonthExpenses() {

               const apiUrl = process.env.VUE_APP_API_BASE_URL;
               const path = apiUrl + '/fetch_months_and_recent_month_expenses';

               const requestData = {
                   // Send to server the choosen/selected year by user "selectedYear", to get its expenses months.
                   selectedYear:this.selectedYear
               };

               // Perform asynchronous operation
               axios
                   .post(path, requestData)

                   .then((response) => {
                   // GET past months which belongs to the "selectedYear" (the year the user have choosen)
                   this.months = response.data.months

                   // Choose/select the most recent month, by assinging it to "selectedMonth" which belongs to the "selectedYear" (the year the user have choosen) 
                   this.selectedMonth = this.months[0]

                   // GET the monthly expenses in the "selectedMonth" (the most recent month) which belongs to the "selectedYear" (the year the user have choosen)
                   this.monthlyExpenses = response.data.monthly_expenses

                   // GET the total monthly expenses amount which belongs to "selectedMonth" (the most recent month) which belongs to the "selectedYear" (the year the user have choosen)
                   this.totalMonthlyExpenses = response.data.total_monthly_expenses

                   // Finaly Emit "monthlyExpenses" and "totalMonthlyExpenses" out to parent component of Home.vue, so it will be used in another sibiling component 
                   this.emitMonthlyExpenses()

                   // After all the above is done, remove the loading indicator
                   this.loading = false;

               })
               .catch((error) => {
                   if (error.response) {
                       console.error(error);
                       // The request was made, and the server responded with a non-2xx status code
                       // Handle the error based on the HTTP status code and error message
                       const status = error.response.status;
                       const message = error.response.data.error_message;
                       alert(`Error! Status: ${status}, Message: ${message}`);
                       this.loading = false; // Set loading to false in case of an error
                   } else if (error.request) {
                       console.error(error);
                       // The request was made, but no response was received
                       alert('Error! No response received from the server. Please try again or contact support for assistance.');
                       this.loading = false; // Set loading to false in case of an error
                   } else {
                       console.error(error);
                       // Something else happened while setting up the request
                       alert(`Oops! Something went wrong while fetch your expenses. Please try again or contact support for assistance.`);
                       this.loading = false; // Set loading to false in case of an error
                   }
               });
           },
               
           // USER HAVE CHOOSEN A MONTH
           // This function will:  1- FETCH the monthly spendings for the selected month 
           async fetchAndEmitSelectedMonthlExpenses() {

               const apiUrl = process.env.VUE_APP_API_BASE_URL;
               const path = apiUrl + '/fetch_selected_month_expenses';
               // Prepare the request data
               const requestData = {

                   // Send to server the choosen/selected year by user "selectedYear", to get its expenses months.
                   selectedYear: this.selectedYear,

                   // Send to server the choosen/selected month by user "selectedMonth", to get its expenses.
                   selectedMonth: this.selectedMonth,
               };

               axios
                   .post(path, requestData)

                   .then((response) => {

                       // Update component data based on the response

                       // // GET the monthly expenses in the "selectedMonth" (selected by user) which belongs to the "selectedYear" (selected by user)
                       this.monthlyExpenses = response.data.monthly_expenses;

                       // // // GET the total monthly expenses in the "selectedMonth" (selected by user) which belongs to the "selectedYear" (selected by user)
                       this.totalMonthlyExpenses = response.data.total_monthly_expenses;

                       // Finaly Emit "monthlyExpenses" and "totalMonthlyExpenses" out to parent component of Home.vue, so it will be used in another sibiling component
                       this.emitMonthlyExpenses();

                       // After all the above is done, remove the loading indicator
                       this.loading = false;

                   })
                   .catch((error) => {
                       if (error.response) {
                           console.error(error);
                           // The request was made, and the server responded with a non-2xx status code
                           // Handle the error based on the HTTP status code and error message
                           const status = error.response.status;
                           const message = error.response.data.error_message;
                           alert(`Error! Status: ${status}, Message: ${message}`);
                           this.loading = false; // Set loading to false in case of an error
                       } else if (error.request) {
                           console.error(error);
                           // The request was made, but no response was received
                           alert('Error! No response received from the server. Please try again or contact support for assistance.');
                           this.loading = false; // Set loading to false in case of an error
                       } else {
                           console.error(error);
                           // Something else happened while setting up the request
                           alert(`Oops! Something went wrong while fetch your expenses. Please try again or contact support for assistance.`);
                           this.loading = false; // Set loading to false in case of an error
                       }
                   });
           },

           // THis gets called when user loads the page, or chooses a year or use chooses a month 
           // Emits "monthlyExpenses" and "totalMonthlyExpenses" out to parent component of Home.vue, so it will be used in another sibiling component 
           emitMonthlyExpenses () {
               const monthlyExpenses = {monthlyExpenses : this.monthlyExpenses, totalMonthlyExpenses : this.totalMonthlyExpenses}

               this.$emit('userChoseMonthTimeFrame', monthlyExpenses)
           },
       },
       mounted() {
           // Call loadAndEmitRecentMonthExpenses() function when user loads the page !, this will get the expenses of the most recent month.
           this.loadAndEmitRecentMonthExpenses()

       }
   }
</script>

<style>

</style>