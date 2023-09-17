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

                    <div>
                        <v-text-field placeholder="type name"></v-text-field>
                        
                    </div>
                    <v-btn color=primary>SORT</v-btn>
               
            </div>

            <div class="transactions">

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
                </div>

            </div>

            <div class="router-link">
                <router-link class="bottom-fixed" to="AddTransactions" >Add Transactions<span class="material-symbols-outlined">add_box</span></router-link>
            </div>

  </div>
</template>

<script>
import Button from '../components/Button.vue';
import CurrentViewSummary from '../components/CurrentViewSummary.vue';
import Header from './../components/Header';


export default {
    name: 'People',
    components: {
        Header,
        CurrentViewSummary,
        Button,
    }
}

</script>

<style>

 .people-view-container {
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
