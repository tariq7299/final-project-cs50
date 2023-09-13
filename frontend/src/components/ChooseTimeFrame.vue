<template>
    <div v-if="loading" class="row loading-indicator">
       <div class="col-12">
           <h3>Loading...</h3>        
       </div>
    </div>
    <div class="" v-else>
        <div class="container-flex">
        <div class="accordion" v-for="(year, index) in years" :key="index">

                <input class="year-input" type="radio" v-model="selectedYear" name="radio-test" :id='"radio-1" + index' :value="year" :key="index" @change="fetchAndEmitRecentMonthExpenses">
               <label class="year-label"  :for='"radio-1" + index'>{{ year }}<span class="material-symbols-outlined">
expand_less
</span></label>
                

            <div class="content" v-for="(month, index) in months" :key="index">
                <input class="month-input" type="radio" v-model="selectedMonth" name="radio-test2" :id='"radio-3" + index' :value="month" @change="fetchAndEmitSelectedMonthlExpenses">
                <label class="month-label" :for='"radio-3" + index'>{{ month }}<span class="material-symbols-outlined">check</span></label>
            </div>
        </div>
    </div>
    </div>
    
</template>

<script>
import axios from 'axios'

export default {
    name: 'ChooseTimeFrame',
    data () {
           return {
               monthlyExpenses: [],
               total_amount_of_month_expenses: '',
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
                this.totalMonthlyExpenses = response.data.total_amount_of_month_expenses

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
                this.totalMonthlyExpenses = response.data.total_amount_of_month_expenses

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
                    this.totalMonthlyExpenses = response.data.total_amount_of_month_expenses;

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
            const monthlyExpenses = {monthlyExpenses : this.monthlyExpenses, totalMonthlyExpenses : this.totalMonthlyExpenses, selectedYear: this.selectedYear, selectedMonth: this.selectedMonth}

            this.$emit('userChoseMonthTimeFrame', monthlyExpenses)
        },
       
        },
        mounted() {
            // Call loadAndEmitRecentMonthExpenses() function when user loads the page !, this will get the expenses of the most recent month.
            this.loadAndEmitRecentMonthExpenses()
    }
}

</script>

<style scoped>


    .container-flex {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .accordion {
        border-top: 1px solid #dee2e6;
        border-right: 1px solid #dee2e6;
        border-left: 1px solid #dee2e6;
        /* border-bottom: 1px solid #dee2e6; */
        border-radius: 7px;
        /* padding: 10px 0; */
        width: 80vw;
        max-width: 800px;
        display: inline-flex;
        flex-direction: column;
    }

    .year-label {
        height: 52px;
        display: inline-flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #dee2e6;
        width: 100%;
        padding: 0 20px;
        
    }

    .content {
        height: 0px;
        overflow: hidden;
        transition: height 0.5s;
        border: none;
    }
    
    .month-label {
        height: 100%;
        display: inline-flex;
        align-items: center;
        justify-content: space-between;
        /* height: 25px; */
        width: 100%;
        padding: 0 20px;
    }
    
    input[type="radio"] {
        display: none;
    }

    
    span{
        width: 30px;
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='M480-345 240-585l56-56 184 184 184-184 56 56-240 240Z'/%3E%3C/svg%3E"); */
        transition: transform 0.5s;
    }    
    
    
    .year-input[type="radio"]:checked ~ .content {
        border-bottom: 1px solid #dee2e6;
        height: 35px; /* Auto height to reveal content */
        /* overflow: auto; */
        
    }
    .year-input[type="radio"]:checked[type="radio"]:checked + .year-label span {
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='m296-345-56-56 240-240 240 240-56 56-184-184-184 184Z'/%3E%3C/svg%3E"); */
        transform: rotate(180deg);
    }
    .year-input[type="radio"]:checked[type="radio"]:checked + .year-label {
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='m296-345-56-56 240-240 240 240-56 56-184-184-184 184Z'/%3E%3C/svg%3E"); */
        background: var(--primary);
    }

    .month-input[type="radio"]:checked + .month-label {
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='m296-345-56-56 240-240 240 240-56 56-184-184-184 184Z'/%3E%3C/svg%3E"); */
        background: var(--secondary);
    }
    .month-label span {
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='m296-345-56-56 240-240 240 240-56 56-184-184-184 184Z'/%3E%3C/svg%3E"); */
        display: none;
    }
    .month-input[type="radio"]:checked + .month-label span {
        /* content: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='24' viewBox='0 -960 960 960' width='24'%3E%3Cpath d='m296-345-56-56 240-240 240 240-56 56-184-184-184 184Z'/%3E%3C/svg%3E"); */
        display: inline;
    }
   


    

</style>