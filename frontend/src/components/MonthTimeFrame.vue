<template>
    <div class="row text-start">
        <div class="col-6">
            <!-- When user loads the page the app will GET the spendings years from the server and populate <select> of the years with it, and inside the fetchYearsAndEmitTimeFrame() function, there is actully a call to fetchMonthsAndEmitTimeFrame() function, that will also populate <select> of months -->
            <!-- Wheu user choose a year (@change=fetchMonthsAndEmitTimeFrame), app will GET spendings months from server, and populate <select> input of the months with it -->
            <!--Also whether the user loads the page, or he chooses a certain year and month manually, in both cases the app will 'emit' the timeFrame (selectedYear & selectedMonth) to parent component (Home.vue)   -->
            <select v-model="selectedYear" @change="fetchMonthsAndEmitTimeFrame">
                <!-- You can this disabled option if you want -->
                <!-- <option disabled value="">Select year</option> -->
                
                <!--  We wrote v-bind:value because it takes its value from data() down there-->
                <!--  'v-bind:key=index' is necessary for the loop to work, it should have like a index/id...etc for each 'year' value found in the list 'years'-->
                <option v-for="(year, index) in years" :value="year" :key="index">{{ year }}</option>
            </select>
        </div>
        <div class="col-6">
            <!-- Wheu user choose a month (@change=emitTimeFrame), app will 'emit' TimeFrame (selectedYear & selectedMonth) to parent component (Home.vue) -->
            <select v-model="selectedMonth" @change="emitTimeFrame">
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
                years: [],
                selectedYear:'',
                months: [],
                selectedMonth: ''
            }
        },
        methods: {
            // This function will populate <select> of months, and also emits the timeFrame (selectedYear & selectedMonth)
            fetchYearsAndEmitTimeFrame () {
                const path = 'http://127.0.0.1:8081/fetchYears'
                axios.get(path)
                    .then(response => {

                        // The response is basically an Object ('response' = { data:{ years:[] } } ) and inside it there are another objects one of them is  "data" and inside "data" there are another objects one of them is 'years' and 'years' is a list [] ! 
                        this.years = response.data.years

                        // Assign the first elemnt of years[] (that will be the most recent spendings year of the current user, becasue i have ordered them as DESC) to "selectedYear"
                        this.selectedYear = this.years[0]

                        // 
                        this.fetchMonthsAndEmitTimeFrame()

                    })
                    .catch(error => {
                        console.error('Error fetching data:', error)
                    })
            },
            fetchMonthsAndEmitTimeFrame() {
            const path = 'http://127.0.0.1:8081/fetchMonths'
            axios.post(path, {
                selectedYear:this.selectedYear
            })
            .then(response => {
                this.months = response.data.months
                this.selectedMonth = this.months[0]
                this.emitTimeFrame()
            })
            .catch(err =>{
                console.log(err);
            });
          },
            //    fetch all months in the selected year
            // return months in the choosen year (months)
            emitTimeFrame () {
                const spendingTimeFrame = {year: this.selectedYear, month: this.selectedMonth}
                this.$emit('userChoseMonthTimeFrame', spendingTimeFrame)
                console.log(spendingTimeFrame)
            },
        },
        mounted() {
            // change fetchYears to fetchYear
            this.fetchYearsAndEmitTimeFrame()
            // this.emitMonthTimeFrame()

        }
    }
</script>

<style>

</style>