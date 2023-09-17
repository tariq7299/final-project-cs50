<template>

  <div class="contacts-view-container">

    <Header class="sector" pageTitle="Dealings History"></Header>

    <CurrentViewSummary></CurrentViewSummary>

    <div class=" sector view-by-container">

                    <div class= "view-by sector">
                        <input type="radio" class="radio-input" value="option3" name="view-by" id="view-by-default" checked>
                        <label class="radio-label" for="view-by-default">Default View</label>
                        <input type="radio" class="radio-input" value="option1" name="view-by" id="view-by-month">
                        <label class="radio-label" for="view-by-month">Month View</label>
                        <input type="radio" class="radio-input" value="option2" name="view-by" id="view-by-day" >
                        <label class="radio-label" for="view-by-day">Day View</label>
                        <input type="radio" class="radio-input" value="option4" name="view-by" id="view-by-custom" >
                        <label class="radio-label" for="view-by-custom">Custom View</label>
                    </div>

                    
                </div>
                
                <div class="transactions">
                    
                <label for="search-for-people"></label>
                <input name="search-for-people" id="search-for-people" placeholder="Search for a person..." type="text" v-model="searchedContact">

                <ul class="transaction" v-for="(contact, index) in filteredList" :key="index">
                    <li class="contact-info" >
                        <p>{{ contact.contact_name }}</p>
                        <p>{{contact.contact_phone}}</p>
                    </li>
                    
                    <router-link :to="{ name: 'contactHistory', params: {contactName: contact.contact_name, contactPhone: contact.contact_phone, contactNetBalance: contact.transations_net_balance}}"><v-btn>{{contact.transations_net_balance}}</v-btn></router-link> 
                </ul>

            </div>

            <div class="router-link">
                <router-link class="bottom-fixed" to="AddTransactions" >Add Transactions<span class="material-symbols-outlined">add_box</span></router-link>
            </div>

  </div>
</template>

<script>
import axios from 'axios'

import CurrentViewSummary from '../components/CurrentViewSummary.vue';
import Header from './../components/Header';


export default {
    

    name: 'People',

    data () {
        return {
            searchedContact: '',
            transactions: [],
            contactName: '',

        }
    },

    components: {
        Header,
        CurrentViewSummary,
    },
    computed: {
        filteredList () {

                return this.transactions.filter((contactObj) => {

                    const nameMatch = contactObj.contact_name.toLowerCase().includes(this.searchedContact.toLowerCase());
                    const phoneMatch = contactObj.contact_phone.toLowerCase().includes(this.searchedContact.toLowerCase());
                    
                    // Return true if either name or phone matches the search query
                    return nameMatch || phoneMatch;

                })
            }
        },
    methods: {
        async fetchTransactions() {
            try {
                const apiUrl = process.env.VUE_APP_API_BASE_URL;

                const path = apiUrl + '/people';

                const response = await axios.get(path);

                // GET years and months 
                this.transactions = response.data.transactions
                
                // After all the above is done, remove the loading indicator
                this.loading = false;

            }   catch (error) {
                console.error(error);
                alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
                this.loading = false; // Set loading to false in case of an error
            }
        }
    },
    created() {
        this.fetchTransactions()
    }

}

</script>

<style>

 .contacts-view-container {
    width: 90vw;
    max-width: 800px;
    margin: auto;
}

#search-for-people {
    width: 100%;
    max-width: 400px;
    border: 2px solid black;
    border-radius: 10px;
}

.transaction {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.contact-info P {
    margin: 0;
}

.transactions {
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    /* align-items: center; */
    gap: 30px;
    /* overflow: scroll; */
}

/* .view-by-container {
    width: 100%;
} */

</style>
