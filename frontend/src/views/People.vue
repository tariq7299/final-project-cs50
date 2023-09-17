<template>

  <div class="people-view-container">
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

                    <!-- 
                    <div>
                        <label for="search-for-people"></label>
                        <input name="search-for-people" id="search-for-people" placeholder="Search for a person..." type="text" v-model="searchedPerson">
                        
                        <ul>
                            <li v-for="item in filteredList" :key="item">{{ item }}</li>
                        </ul>
                    </div> -->
                    
                    <v-btn color=primary>SORT</v-btn>
                    
                </div>
                
                <div class="transactions">
                    
                <label for="search-for-people"></label>
                <input name="search-for-people" id="search-for-people" placeholder="Search for a person..." type="text" v-model="searchedPerson">

                <ul class="transaction" v-for="(person, index) in filteredList" :key="index">
                    <li class="person-info" >
                        <p>{{ person.contact_name }}</p>
                        <p>{{person.contact_phone}}</p>
                    </li>
                    <p>{{person.transations_net_balance}}</p>
                </ul>

                <!-- <div class="transaction">
                    <div class="person-info">
                        <p>Ahmed Kamal</p>
                        <p>0109033042</p>
                    </div>
                    <p>230</p>
                </div>

                <div class="transaction">
                    <div class="person-info">
                        <p>Ahmed Kamal</p>
                        <p>0109033042</p>
                    </div>
                    <p>230</p>
                </div>

                <div class="transaction">
                    <div class="person-info">
                        <p>Ahmed Kamal</p>
                        <p>0109033042</p>
                    </div>
                    <p>230</p>
                </div> -->

            </div>

            <div class="router-link">
                <router-link class="bottom-fixed" to="AddTransactions" >Add Transactions<span class="material-symbols-outlined">add_box</span></router-link>
            </div>

  </div>
</template>

<script>
import axios from 'axios'

import Button from '../components/Button.vue';
import CurrentViewSummary from '../components/CurrentViewSummary.vue';
import Header from './../components/Header';


export default {
    

    name: 'People',

    data () {
        return {
            searchedPerson: '',
            items: ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'],
            transactions: [],

        }
    },

    components: {
        Header,
        CurrentViewSummary,
        Button,
    },
    computed: {
        filteredList () {

                return this.transactions.filter((personInfoObj) => {

                    const nameMatch = personInfoObj.contact_name.toLowerCase().includes(this.searchedPerson.toLowerCase());
                    const phoneMatch = personInfoObj.contact_phone.toLowerCase().includes(this.searchedPerson.toLowerCase());
                    
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

 .people-view-container {
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

.person-info P {
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
