<template>
    <div class="row text-start">
        <div class="col-6">
            <!-- When user loads the page the app will GET the spendings years from the server and populate <select> of the years with it, and inside the fetchYearsAndEmitTimeFrame() function, there is actully a call to fetchMonthsAndEmitTimeFrame() function, that will also populate <select> of months -->
            <!-- Wheu user choose a year (@change=fetchMonthsAndEmitTimeFrame), app will GET spendings months from server, and populate <select> input of the months with it -->
            <!--Also whether the user loads the page, or he chooses a certain year and month manually, in both cases the app will 'emit' the timeFrame (selectedYear & selectedMonth) to parent component (Home.vue)   -->
            <select v-model="selectedYear" @change="fetchMonthsAndEmitRecentSpendings">
                <!-- You can this disabled option if you want -->
                <!-- <option disabled value="">Select year</option> -->
                
                <!--  We wrote v-bind:value because it takes its value from data() down there-->
                <!--  'v-bind:key=index' is necessary for the loop to work, it should have like a index/id...etc for each 'year' value found in the list 'years'-->
                <option v-for="(year, index) in years" :value="year" :key="index">{{ year }}</option>
            </select>
        </div>
        <div class="col-6">
            <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
            <select v-model="selectedMonth" @change="fetchAndEmitSelectedMonthSpendings">
                <!-- <option disabled value="">Select month</option> -->
                <option v-for="(month, index) in months" :value="month" :key="index">{{ month }}</option>
            </select>
        </div>
        <div class="col-6">
            <h1>{{ total_monthly_spendings }}</h1>
        </div>
        <div class="col-6">
            <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
            <ul v-for="dailySpending in monthSpendings" :key="dailySpending.spending_id">
                <!-- <option disabled value="">Select month</option> -->
                <li> {{ dailySpending.date }}</li>
                <li> {{ dailySpending.item_type }}</li>
                <li> {{ dailySpending.amount_spent }}</li>
            </ul>
            <ul v-for="(daily_spendings, index) in total_daily_spendings" :key="index">
                <li> {{ daily_spendings.total_daily_spending }}</li>
            </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

    export default {
        name: "MonthTimeFrame",
        data () {
            return {
                monthSpendings: [],
                total_monthly_spendings: [],
                total_daily_spendings: [],
                years: [],
                selectedYear:'',
                months: [],
                selectedMonth: '',
            }
        },
        methods: {
            // **NOTICE** ---> THERE IS ANOTHER WAY TO DO THE FOLLOWING PART OF CODE, which can be found in 'monthTimeFrame' branch

            // This function will GET spendings years[] from server which belongs to the current user
            // async fetchYears() {
            //     try {
            //         const path = 'http://127.0.0.1:8083/spendings'
            //         const response = await axios.get(path);
            //         this.years = response.data.years;
            //         this.selectedYear = this.years[0];
            //         await this.fetchMonths();
            //     }   catch (error) {
            //         console.error('Error fetching data:', error);
            //     }
            // },

            // This function will GET spendings months[] of 'selectedYear' from server which belongs to the current user
            async fetchAndEmitSelectedMonthSpendings() {
                try {
                    const path = 'http://127.0.0.1:8083/selectedMonthSpendings'

                    // Perform asynchronous operation
                    const response = await axios.post(path,{
                        selectedYear:this.selectedYear, 
                        selectedMonth:this.selectedMonth,
                    });
                    this.monthSpendings = response.data.monthSpendings
                    this.emitSpendings()
                    
                } catch (error) {
                    // Handle error
                    console.error(error);
                }
            },

            // This function will GET spendings years[] from server which belongs to the current user, and the emits timeFrame (selectedYear & selectedMonth) to parent component (Home.vue)
            // This gets called when user reloads the page only !!
            async fetchYearsAndEmitRecentSpendings() {
                try {
                    const path = 'http://127.0.0.1:8083/spendings'

                    const response = await axios.get(path);

                    this.years = response.data.years;
                    this.months = response.data.months
                    this.monthSpendings = response.data.monthSpendings
                    this.total_monthly_spendings = response.data.total_monthly_spendings
                    this.total_daily_spendings = response.data.total_daily_spendings

                    this.selectedYear = this.years[0];
                    this.selectedMonth = this.months[0]
                    console.log(this.total_daily_spendings)
                    this.emitSpendings();
                }   catch (error) {
                    console.error('Error fetching data:', error);
                }
            },

            // This function will GET spendings months[] from server which belongs to the current user, and the emits timeFrame (selectedYear & selectedMonth) to parent component (Home.vue)
            // This gets called when user choose a "year" from <select> input of years
            async fetchMonthsAndEmitRecentSpendings() {
                try {
                    const path = 'http://127.0.0.1:8083/RecentMonthSpendings'

                    // Perform asynchronous operation
                    const response = await axios.post(path,{
                        selectedYear:this.selectedYear
                    });
                    this.months = response.data.months
                    this.monthSpendings = response.data.monthSpendings

                    this.selectedMonth = this.months[0]
                    
                } catch (error) {
                    // Handle error
                    console.error(error);
                }
            },

            // THis gets called when user loads the page, or chooses a year or use chooses a month 
            emitSpendings () {
                // const monthSpendings = {monthSpendings : this.monthSpendings}
                this.$emit('userChoseMonthTimeFrame', this.monthSpendings)
            },
        },
        mounted() {
            // When user loads the page
            this.fetchYearsAndEmitRecentSpendings()

        }
    }
</script>

<style>

</style>