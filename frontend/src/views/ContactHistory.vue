<template>
    <div class="contact-history-container">

        <Header class="sector" pageTitle="Contact Dealings History"></Header>

        <div class="sticky-header">
            <div class="contact-info">
                <div class="info-row">
                    <p class="label">Name</p>
                    <p class="name">{{ contactName }}</p>
                </div>
                <div class="info-row">
                    <p class="label">Phone</p>
                    <p class="phone">{{ contactPhone }}</p>
                </div>
                <div class="sector">
                    <UserWallet walletTitle="Contact Net Balance" :amount="contactNetBalance"></UserWallet>
                </div>
            </div>
        </div>        

        <div class="contact-history">
            <Days :groupedByDay="groupedTransactionsByDay"></Days>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'

import UserWallet from '../components/UserWallet.vue';
import Header from './../components/Header';
import Days from '@/components/Days.vue';

    export default {
        name: 'ContactHistory.vue',
        data () {
            return {transactions: [],
        }
    },
        components: {
            Header,
            UserWallet,
            Days,
        },
        props: ['contactName', 'contactPhone', 'contactNetBalance'],
        methods: {
            async fetchContactHistory () {

            const apiUrl = process.env.VUE_APP_API_BASE_URL;
            const path = apiUrl + '/people';
            // Prepare the request data
            const requestData = {
                contactPhone: this.contactPhone,
            };

            axios
                .post(path, requestData)

                .then((response) => {

                    this.transactions = response.data.transactions;
                })
                .catch((error) => {
                    if (error.response) {
                        console.error(error);
                        // The request was made, and the server responded with a non-2xx status code
                        // Handle the error based on the HTTP status code and error message
                        const status = error.response.status;
                        const message = error.response.data.error_message;
                        alert(`Error! Status: ${status}, Message: ${message}`);
                    } else if (error.request) {
                        console.error(error);
                        // The request was made, but no response was received
                        alert('Error! No response received from the server. Please try again or contact support for assistance.');
                    } else {
                        console.error(error);
                        // Something else happened while setting up the request
                        alert(`Oops! Something went wrong while fetch your expenses. Please try again or contact support for assistance.`);
                    }
                });
            }
        },
        computed: {
            groupedTransactionsByDay() {
                return this.transactions.reduce((acc, dailyTransactions) => {
                if (!acc[dailyTransactions.date]) {
                    acc[dailyTransactions.date] = {
                        dailyTransactions: [],
                        totalAmount: 0
                    };
                }
                
                acc[dailyTransactions.date].dailyTransactions.push(dailyTransactions);
                acc[dailyTransactions.date].totalAmount += dailyTransactions.amount;
                return acc;
                }, {});
            }
        },
        created() {
            this.fetchContactHistory()
        }
    }   
</script>

<style scoped>

.contact-history-container {
    width: 90vw;
    max-width: 800px;
    margin: auto;
}

.contact-info {
    padding: 20px;
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: auto;
}

.info-row {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

.label{
    letter-spacing: 0.1rem;
    padding: 10px;
    background: var(--primary);
}

.name, .phone {
    font-size: 1.2em;
    font-style: italic;
    font-weight: 500;
}

.sticky-header {
        position: sticky;
        top: 3.8rem;
        background: var(--background);
        padding-top: 1rem;
        z-index: 1019;
    }

</style>