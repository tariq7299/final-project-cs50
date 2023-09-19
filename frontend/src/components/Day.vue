<template>
    <div class="days-contaiter">
        
        <!-- I have used vue binding directives "" :data-bs-target='"#" + uniqueId' "", in 'accordion' boostrap compoennet, becasue in order for each accordion to collapse and expand when you click on it, Each 'data-bs-target' property in <button> of accordion should point to a unique 'id' down in accordion body, so I have made some adjustments and apllied the v-for loop of vue to uniqlyt assing variables to each accordion !-->
            <div v-show="homePage">

                <div class="accordion" id="accordionExample">
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target='"#" + uniqueId' aria-expanded="true" aria-controls="collapseOne">
                            {{ dayDate }} - Total: {{ totalAmount }}
                        </button>
                        </h2>
                        <div :id="uniqueId" class="accordion-collapse collapse show" >
                        <div class="accordion-body">
                            <div class=" expense" v-for="expense in expenses" :key="expense.spending_id">
                                <span class="category">{{ expense.category }}</span><span class="amount">{{ expense.amount_spent }}</span> 
                            </div>
                        </div>
                        </div>
                    </div>
                    
                </div>  

            </div>

            <div v-show="contactHistoryPage">

                <div class="accordion" id="accordionExample">
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target='"#" + uniqueId' aria-expanded="true" aria-controls="collapseOne">
                            {{ dayDate }} - Total: {{ totalAmount }}
                        </button>
                        </h2>
                        <div :id="uniqueId" class="accordion-collapse collapse show" >
                        <div class="accordion-body">
                            <div class=" expense" v-for="dailyTransaction in dailyTransactions" :key="dailyTransaction.id">
                                <span class="category">{{ dailyTransaction.note }}</span><span class="amount">{{ dailyTransaction.amount }}</span> 
                            </div>
                        </div>
                        </div>
                    </div>
                    
                </div>
            </div>
        </div>

  </template>

<script>
    export default {
        name: 'Day',
        props: {
            dayDate: String,
            expenses: Array,
            totalAmount: Number,
            dailyTransactions: Array,

        },
        computed: {
            uniqueId() {
                return "collapse" + this.dayDate.substring(4, 6);
            },
            homePage () {
                if(this.$route.path === '/') {
                    return true
                } else {
                    return false
                }
            },
            contactHistoryPage () {
                return this.$route.path.startsWith('/contact-history/');
                // OR
                // return this.$route.name === 'contactHistory';
            }
        }
    }
</script>

<style scoped>
    .days-contaiter {
        margin: auto;
        padding: 5px;
    }
    .accordion-button, .accordion-body {
        background-color: var(--secondary)
    }

    .accordion-button[aria-expanded="true"] {
        background-color: var(--primary)
    }
    /* You can also use  "d-flex justify-content-between" of bootstrap*/
    .expense {
        display: flex;
        justify-content: space-between;
    }

    .category {
        font-style: italic;
        margin: 2px 0;
    }

    .amount {
        font-weight: 600;
    }
    
 

</style>

