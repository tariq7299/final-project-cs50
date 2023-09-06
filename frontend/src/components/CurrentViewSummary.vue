<template>
  <div class="row">
    <div class="col-6">
        <UserWallet walletTitle="Balance" :amount="wallet.balance"/>        
    </div>
    <div class="col-6">
        <UserWallet walletTitle="Debt" :amount="wallet.debt"/>
    </div>
    <div class="col-12">
        <UserWallet walletTitle="Credit" :amount="wallet.credit"/>
    </div>
  </div>
</template>

<script>
    import UserWallet from './UserWallet.vue'
    import axios from 'axios'

    export default {
        name: "CurrentViewSummary",
        components: {
            UserWallet, 
        },
        data () {
            return {
                // Initialize as an empty object
                wallet: {}
            }
        },
        methods: {
            async fetchUserWallet() {
                try {
                    const path = 'http://127.0.0.1:8083/userWallet'

                    const response = await axios.get(path);

                    this.wallet = response.data.wallet;
                }   catch (error) {
                    console.error('Error fetching data:', error);
                }
            },
        },
        async created() {
            await this.fetchUserWallet() 
        }
    }
</script>

<style>

</style>