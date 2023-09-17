<template>
    <div class="contact-history-container">

        <Header class="sector" pageTitle="Dealings History"></Header>
  
        <div class="contact-info">
            <div class="info-row">
                <p>Name:</p>
                <p>{{ contactName }}</p>
            </div>
            <div class="info-row">
                <p>Phone:</p>
                <p>{{ contactPhone }}</p>
            </div>
            <div class="info-row">
                <UserWallet walletTitle="Contact Net Balance" :amount="contactNetBalance"></UserWallet>
            </div>
        </div>

        <div class="contact-history">
            <Days :groupedByDay="groupedTransactionsByDay"></Days>
            <!-- <h1>{{ coonsol.log(groupedTransactionsByDay) }}</h1>
            <h1>{{ coonsol.table(groupedTransactionsByDay) }}</h1> -->
            <!-- <div v-for="(transaction, index) in transactions" :key="index">
                <p>{{transaction.date}}</p>
                <p>{{transaction.amount}}</p>
            </div> -->
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

<style>

</style>