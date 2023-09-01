<template>
    <div class="row text-start">
        <div class="col-6">
            <select v-model="selectedYear" @change="fetchMonths">
                <option disabled value="">Select year</option>
                <option v-for="year in years" :value="year">{{ year }}</option>
            </select>
        </div>
        <div class="col-6">
            <select v-model="selectedMonth" @change="fetchMonthData">
                <option disabled value="">Select month</option>
                <option v-for="month in months" :value="month.value">{{ month.label }}</option>
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
                currentMonth: "",

                years: [],

                selectedYear: '',

                months: [],

                selectedMonth: ''
                
            }
        },
        methods: {
            fetchYears () {
                const path = 'http://127.0.0.1:5000/fetchYears'
                axios.get(path)
                    .then(response => {
                        this.years = response.data.years
                        console.log("response.data", response.data)
                        console.log("response.data.years", response.data.years)
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error)
                    })
            },
            fetchMonths (selectedYear) {
            //    fetch all months in the selected year
            // return months in the choosen year (months)

            },
            fetchDays (selectedMonth) {
            //    Fecth the spending days of the slectedMonth from the server
            // return (total spending in the month, days)
            },
        },
        mounted() {
            this.fetchYears()
        }
    }
</script>

<style>

</style>