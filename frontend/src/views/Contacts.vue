<template>

  <div class="contacts-view-container">

    <CurrentViewSummary></CurrentViewSummary>
    
    <div class="sticky-header">
        
        <Header class="sector" pageTitle="Dealings History"></Header>

        <div class=" sector view-by-container">

            <div class= "view-by sector">

                <input type="radio" class="radio-input" value="option3" name="view-by" id="view-by-default" checked>
                <label class="radio-label" for="view-by-default"><span>Default </span>View<span></span></label>

                <input type="radio" class="radio-input" value="option1" name="view-by" id="view-by-month">
                <label class="radio-label" for="view-by-month"><span>Month </span>View<span></span></label>

                <input type="radio" class="radio-input" value="option2" name="view-by" id="view-by-day" >
                <label class="radio-label" for="view-by-day"><span>Day </span>View<span></span></label>

                <input type="radio" class="radio-input" value="option4" name="view-by" id="view-by-custom" >
                <label class="radio-label" for="view-by-custom"><span>Custom </span>View<span></span></label>

            </div>
            
        </div>
        
        <div class="search-bar sector">
            <input name="search-for-people" id="search-for-people" placeholder="Search for a person..." type="text" v-model="searchedContact">
        </div>        
    </div>

    <div class="transactions">
        
        <div class="transaction" v-for="(contact, index) in filteredList" :key="index">
            <div class="contact-info" >
                <p class="name">{{ contact.contact_name }}</p>
                <p class="phone">{{contact.contact_phone}}</p>
            </div>
            
            <router-link :to="{ name: 'contactHistory', params: {contactName: contact.contact_name, contactPhone: contact.contact_phone, contactNetBalance: contact.transations_net_balance}}"><v-btn class="contact-net-btn"><span class="contact-net-balance" :style="colorNetBalance(contact.transations_net_balance)">{{ Math.abs(contact.transations_net_balance)}}</span></v-btn></router-link> 
        </div>

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

                const response = await axios.get(path, { withCredentials: true });

                // GET years and months 
                this.transactions = response.data.transactions
                
                // After all the above is done, remove the loading indicator
                this.loading = false;

            }   catch (error) {
                console.error(error);
                alert(`Oops! Something went wrong. Please try again or contact support for assistance. Error message: ${error}`);
                this.loading = false; // Set loading to false in case of an error
            }
        },
        colorNetBalance (amount) {
            return  amount > 0 ? {'color': 'GREEN'} : {'color': 'RED'};
        }

    },
    created() {
        this.fetchTransactions()
    }

}

</script>

<style scoped>

 .contacts-view-container {
    width: 90vw;
    max-width: 800px;
    margin: auto;
}


.transaction {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.contact-info P {
    margin: 0;
    text-align: left;
}
.contact-info .name {
    font-weight: 600; 
}
.contact-info .phone {
    font-size: 0.75em;
}

.transactions {
    display: flex;
    flex-direction: column;
    gap: 30px;
    padding: 1rem;
}

.search-bar {
  display: flex;
  align-items: center;
  border-radius: 5px;
  padding: 5px;
  background-color: #fff;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

#search-for-people {
  flex: 1;
  border: none;
  outline: none;
  padding: 8px;
  font-size: 16px;
}

.contact-net-btn {
    border-radius: 18px;
    font-weight: 600;
    background-color: var(--secondary);
}

.contact-net-balance::after {
    content: ' >';
    font-weight: 900;
    font-size: 1.2em;
    color: black;
}

@media (max-width: 450px) and (orientation: portrait) {

    .radio-label {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
}

</style>
