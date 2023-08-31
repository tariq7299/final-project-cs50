<template>
    <div class="row text-start">
        <div class="col-12">
            <router-link to="/chooseMonth"> <h2>{{ currentMonth }}</h2> </router-link>

            
        </div>
    </div>
</template>

<script>
    export default {
        name: "MonthTimeFrame",
        data () {
            return {
                currentMonth: "",
            }
        },
        methods: {
            fetchCurrentMonth() {
                var date = new Date();
                // 'default' is the value of default time zone info (user’s language, region, and cultural preferences), that is stored in the browsers
                var month = date.toLocaleString('default', { month: 'short' });
                var year = date.getFullYear();
                var currentMonth = (month + ' ' + year)
                return currentMonth
            },
        },
        mounted() {
            this.currentMonth = this.fetchCurrentMonth() 
        }
    }
</script>

<style>

</style>