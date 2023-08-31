<template>
    <div class="row text-start">
        <div class="col-6">
            <select v-model="selectedYear" @change="fetchMonths">
                <option disabled value="">Please select one</option>
                <option v-for="year in years" :value="year.value">{{ year.label }}</option>
            </select>
        </div>
        <div class="col-6">
            <select v-model="selectedMonth" @change="fetchMonthData">
                <option disabled value="">Please select one</option>
                <option v-for="month in months" :value="month.value">{{ month.label }}</option>
            </select>
        </div>
    </div>
</template>

<script>
    export default {
        name: "MonthTimeFrame",
        data () {
            return {
                currentMonth: "",

                years: [],

                selectedYear: 'option2',

                months: [],

                selectedMonth: 'option3'
                
            }
        },
        methods: {
            fetchYears () {
                const path = 'http://127.0.0.1:5000/fetchYears'
                axios.get(path)
                    .then(response => {
                        this.years = response.data
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