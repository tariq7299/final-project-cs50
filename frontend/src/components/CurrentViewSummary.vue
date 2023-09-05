<template>
  <div class="row">
    <div class="col-6">
        <UserFinance amountTitle="Balance" :amount="money.balance"/>        
    </div>
    <div class="col-6">
        <UserFinance amountTitle="Debt" :amount="money.moneyIOwe"/>
    </div>
    <div class="col-12">
        <UserFinance amountTitle="Credit" :amount="money.moneyOwedToMe"/>
    </div>
  </div>
</template>

<script>
    import UserFinance from './UserFinance.vue'
    import axios from 'axios'

    export default {
        name: "CurrentViewSummary",
        components: {
            UserFinance, 
        },
        data () {
            return {
                // Initialize as an empty object
                money: {}
            }
        },
        methods: {
            async fetchUserFinance() {
                // const res = await axios.get('api/userFinance')
                // const data = await res.data
                // return data
                // This is a test
                return { balance: 1000, moneyIOwe: 500, moneyOwedToMe: 200 }
            },
        },
        async created() {
            this.money = await this.fetchUserFinance() 
        }
    }
</script>

<style>

</style>