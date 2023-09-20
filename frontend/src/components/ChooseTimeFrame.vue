<template>
    <div v-if="loading" class="row loading-indicator">
       <div class="col-12">
           <h3>Loading...</h3>        
       </div>
    </div>
    <div class="" v-else>
        <div class="container-flex">

            <div class='accordion ' v-for="(yearAndMonths, index) in yearsAndMonths" :key="index">

                <div class="accordion-header" @click="selectYearAndShowMonths(yearAndMonths)" :style="styleSelectedYear(yearAndMonths.year)">
                    <strong>{{ yearAndMonths.year }}</strong><span class="material-symbols-outlined expand" :style="animateExpandArrow(yearAndMonths.year)">expand_more</span>
                </div>

                <!-- 'TransitionGroup' is a veu js built in componenet, that can animate v-show  -->
                <TransitionGroup name="monthsList">
                    <div class="accordion-body" v-for="(month, index) in yearAndMonths.months" :key="index" v-show="yearAndMonths.opened" @click="fetchAndEmitSelectedMonthlExpenses(month)" :style="StyleSelectedMonth(month)">
                        {{ month }}<span class="material-symbols-outlined checkSymbol" :style="AddCheckSymbol(month)">check</span>
                    </div>
                </TransitionGroup>

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
               selectedYear:'',
               selectedMonth: '',
               loading: true, // Add a loading indicator state
            //    opened: true,
               yearsAndMonths: {},
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

                const response = await axios.get(path, { withCredentials: true });
                
                // 
                if (response.data.noExpensesFound) {

                    // Create a computed variable of v-model that will containa message to to display to user that there is no expenses

                    this.loading = false;
                    return
                }
                // GET years and months 
                this.yearsAndMonths = response.data.years_and_months
                console.log('yearsAndMonths', this.yearsAndMonths)

                // Make t
                this.yearsAndMonths[0].opened = true

                // Choose/select the most recent year, by assinging it to "selectedYear"
                this.selectedYear = this.yearsAndMonths[0].year;
                console.log('selectedYear', this.selectedYear)

                // Choose/select the most recent month, by assinging it to "selectedMonth"
                this.selectedMonth = this.yearsAndMonths[0].months[0];
                console.log('selectedMonth', this.selectedMonth)
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

        // USER HAVE CHOOSEN A MONTH
        // This function will:  1- FETCH the monthly spendings for the selected month 
        async fetchAndEmitSelectedMonthlExpenses(month) {

            this.selectedMonth = month

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
                .post(path, requestData, { withCredentials: true })

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
            selectYearAndShowMonths (yearAndMonths) {
                if (yearAndMonths.opened == true) {
                    yearAndMonths.opened = false
                }
                else {

                    this.yearsAndMonths.forEach(function (element) {
                        element.opened = false
                    });
                    yearAndMonths.opened = !yearAndMonths.opened
                }
                this.selectedYear = yearAndMonths.year
            },
            // I couldn't use "styleSelectedYear" as a computed prop, becasue 'styleSelectedYear' takes input, and I can't take input as acomputed prop
            styleSelectedYear(headerYear) {
                if (headerYear === this.selectedYear) {
                    return {'background-color': 'var(--primary)'}
                } 
            },
            animateExpandArrow (headerYear) {
                if (headerYear === this.selectedYear) {
                    return {'transform': 'rotate(180deg)'}
                } 
            },
            StyleSelectedMonth (month) {
                if (month === this.selectedMonth) {
                    return {'background-color': 'var(--accent)'}
                } 
            },
            AddCheckSymbol (month) {
                if (month === this.selectedMonth) {
                    return {'display': 'inline'}
                } 
            }
        },
        mounted() {
            // Call loadAndEmitRecentMonthExpenses() function when user loads the page !, this will get the expenses of the most recent month.
            this.loadAndEmitRecentMonthExpenses()
        },
        computed: {
            accordionClasses () {
                return {'closed': !this.opened}
            },
        }
}

</script>

<style scoped>
    .container-flex {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        padding: 10px;
    }

    .accordion {
        width: 80vw;
        max-width: 600px;
        border:1px solid #dee2e6;
        border-radius: 7px;
    }

    .accordion-header {
        width: 100%;
        display: inline-flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        border-bottom: 1px solid #dee2e6;
        cursor: pointer;
        background-color: var(--secondary)
        
    }

    .accordion-body {
        width: 100%;
        max-height: 35px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        overflow: hidden;
        cursor: pointer;
        background-color: var(--secondary)
        /* transition: 0.5s ease; */
    }

    .accordion-body p {
        height: 10px;
        /* margin-top: auto;
        margin-bottom: auto; */
    }

    
    .monthsList-enter-active, .monthsList-leave-active {
    transition: all 0.4s ease;
    }
    .monthsList-enter-from {
        max-height: 0;
        padding: 0px;
        opacity: 0;
    } 
    
    .monthsList-leave-to {
        max-height: 0;
        padding: 0px;
        opacity: 0;
    }

    .checkSymbol {
        display: none;
    }

    .expand {
        transition: transform 0.3s;
    }

</style>