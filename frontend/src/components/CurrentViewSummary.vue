<template >
        <!-- This will make a loading indicator appears until 'v-if="loading"' becomes 'false' (it will become false in two cases the FIRST when the app successfully fetches the data, the SECOND is when app encounters an error when fetching data! )  -->
        <div v-if="loading" class="row loading-indicator">
            <div class="col-12">
                <h3>Loading...</h3>        
            </div>
        </div>
        <div class="" v-else>

            <div class="wallet-container">
                <div class="wallet-row-1">
                    <UserWallet walletTitle="Debt" :amount="wallet.debt" class="wallet-unit debt"/>
                    <UserWallet walletTitle="Credit" :amount="wallet.credit" class="wallet-unit credit"/>
                </div>
                <div class="wallet-row-2">
                    <UserWallet walletTitle="Net Balance" :amount="wallet.netBalance" class="wallet-unit net-balance"/>        
                </div>
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

                    const response = await axios.get(path, { withCredentials: true });

                    if (response.data.userNotLogged) {
                        this.$router.push({ name: 'login' });
                        return
                    }

                    this.wallet = response.data.wallet;

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
            await this.fetchUserWallet()
        },
        computed: {
            homePage () {
                if(this.$route.path === '/') {
                    return true
                } else {
                    return false
                }
            },
            colorNetBalance () {
                return this.netBalance > 0 ? {'color': 'GREEN'} : {'color': 'RED'}
            }
        }
    }
</script>

<style scoped>

.wallet-container {
    padding:  1.5rem 1rem 1.6rem 0.5rem
}

.wallet-row-1 {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.wallet-row-2 {
    display: flex;
    align-items: center;
    justify-content: center;
}


</style>