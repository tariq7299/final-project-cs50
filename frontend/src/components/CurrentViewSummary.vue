<template >
        <!-- This will make a loading indicator appears until 'v-if="loading"' becomes 'false' (it will become false in two cases the FIRST when the app successfully fetches the data, the SECOND is when app encounters an error when fetching data! )  -->
        <div v-if="loading" class="row loading-indicator">
            <div class="col-12">
                <h3>Loading...</h3>        
            </div>
        </div>
        <div class="" v-else>

            <div class="row sector" v-show="homePage">
                <div class="col-6 d-flex justify-content-start">
                    <UserWallet walletTitle="Balance" :amount="wallet.balance"/>        
                </div>
                <div class="col-6 d-flex justify-content-end">
                    <UserWallet walletTitle="Debt" :amount="wallet.debt"/>
                </div>
                <div class="col-12 d-flex justify-content-center">
                    <UserWallet walletTitle="Credit" :amount="wallet.credit"/>
                </div>
            </div>

            <div class="row sector" v-show="peoplePage">
                <UserWallet walletTitle="Net Balance" :amount="netBalance"></UserWallet>
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
                wallet: {},
                netBalance: '',
                loading: true, // Add a loading indicator state
            }
        },
        methods: {

            // "async" and "await" keywords are necessary becasue it makes the code not proceed until it executes the line with the aawit keyword "const response = await axios.get(path);", So lets say for example you have removed 'await' keyword then the lines after "const response = await axios.get(path);"  will be executed before it !, and you don't want this to happen because "this.wallet = response.data.wallet;" actually depends on the execution of the fetch request of "const response = await axios.get(path);"
            // And if you wonder why wouldn't the lines of code in 'fetchUserWallet()' executes one by one normally ? So the answer is it can't do that !!! because "axios.get(path)" function is a asynchronous function !, and it retuns a 'promise', so we want our code to wait when it reaches it until it fetches data and THEN it can proceed executing the following lines !
            async fetchUserWallet() {
                try {
                    const apiUrl = process.env.VUE_APP_API_BASE_URL;
                    const path = apiUrl + '/user_wallet';

                    const response = await axios.get(path);

                    this.wallet = response.data.wallet;
                    this.loading = false; // Set loading to false when data is fetched
                }   catch (error) {
                    console.error('Error fetching data:', error);
                    alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
                    this.loading = false; // Set loading to false in case of an error
                }
            },
            async fetchUserNetBalance() {
                try {
                    const apiUrl = process.env.VUE_APP_API_BASE_URL;
                    const path = apiUrl + '/net_balance';

                    const response = await axios.get(path);

                    this.netBalance = response.data.net_balance;
                    this.loading = false; // Set loading to false when data is fetched
                }   catch (error) {
                    console.error('Error fetching data:', error);
                    alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
                    this.loading = false; // Set loading to false in case of an error
                }
            },
        },
        // Here we can actually remove async and await keywords !, because there is no lines od code after "await this.fetchUserWallet()" !!
        async created() {
            // To activate it only if the user navigates to home page
            if(this.$route.path === '/') {    
                await this.fetchUserWallet()
            } else if (this.$route.path === '/contacts') {
                await this.fetchUserNetBalance()
            }
        },
        computed: {
            homePage () {
                if(this.$route.path === '/') {
                    return true
                } else {
                    return false
                }
            },
            peoplePage () {
                if(this.$route.path === '/contacts') {
                    return true
                } else {
                    return false
                }
            }
        }
    }
</script>

<style scoped>
</style>